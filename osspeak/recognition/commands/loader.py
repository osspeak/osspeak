from recognition.actions import library
import lark.exceptions
import os
import os.path
import xml.etree.ElementTree as ET
import copy
import operator
import collections
import log
import recognition.actions.library.stdlib
from recognition.actions import perform
import settings
from recognition.actions import variables, perform
from recognition.commands import grammar
from recognition import command_module
from recognition.rules.converter import SrgsXmlConverter
from recognition.rules import astree
from recognition import lark_parser
from communication import pubsub, topics
from common import limited_size_dict
import recognition.cache
import clargs

DEFAULT_DIRECTORY_SETTINGS = {
    'recurse': True,
    'conditions': {},
}

PRIORITY_FN = operator.attrgetter('priority')

class CommandModuleController:

    def __init__(self, module_loader):
        self.module_loader = module_loader
        self.grammars = collections.OrderedDict()
        self.map_grammar_to_commands = collections.OrderedDict()
        self.command_modules = {}
        self.active_command_modules = {}
        self.map_nodes_to_command_module = {}

    def initialize_command_modules(self):
        if clargs.get_args()['clean_cache']:
            recognition.cache.delete_cache()
        recognition.actions.library.stdlib.initialize()
        command_module_cache = recognition.cache.load_cache()
        new_cache = recognition.cache.empty_cache()
        files = self.module_loader.load_files()
        command_modules = {}
        for full_path, text in files.items():
            if full_path.endswith('.speak'):
                if text in command_module_cache['command_modules']:
                    cmd_module_json_str = command_module_cache['command_modules'][text]
                    cmd_module = recognition.cache.from_text(cmd_module_json_str)
                else:
                    try:
                        module_ir = lark_parser.parse_command_module(text)
                    except (lark.exceptions.UnexpectedCharacters, lark.exceptions.UnexpectedEOF) as e:
                        print(f'Error parsing command module {full_path}:\n{e}')
                        print('Continuing...')
                        continue
                    text_by_line = text.split('\n')
                    cmd_module = command_module.command_module_from_lark_ir(module_ir, text_by_line)
                if 'on_load' in cmd_module.functions:
                    namespace = self.get_namespace()
                    source = {'command_module': cmd_module, 'type': 'command_module_loaded'}
                    action = cmd_module.functions['on_load'].action
                    perform.perform_action_from_event(action, namespace, source)
                command_modules[full_path] = cmd_module
                cmd_module.relative_path = os.path.relpath(full_path, self.module_loader.root)
                cmd_module.absolute_path = full_path
                new_cache['command_modules'][text] = recognition.cache.to_json_string(cmd_module)
        recognition.cache.save_cache(new_cache)
        return command_modules
        
    def get_active_modules(self, current_window: str):
        active_modules = {}
        for path, cmd_module in self.command_modules.items():
            if cmd_module.is_active(current_window):
                active_modules[path] = cmd_module
        return active_modules

    def load_modules(self, current_window, initialize_modules: bool=False):
        previous_active_modules = self.sorted_command_modules(self.active_command_modules)
        if initialize_modules:
            raise NotImplementedError
        self.active_command_modules = self.get_active_modules(current_window)
        command_modules_by_ascending_priority = self.sorted_command_modules(self.active_command_modules)
        namespace = self.get_namespace()
        self.fire_activation_events(previous_active_modules, command_modules_by_ascending_priority, namespace)
        grammar_context = self.build_grammar(command_modules_by_ascending_priority.values())
        if grammar_context is not None:
            self.save_grammar(grammar_context)
            grammar_xml, grammar_id = ET.tostring(grammar_context.xml).decode('utf8'), grammar_context.uuid
            pubsub.publish(topics.LOAD_ENGINE_GRAMMAR, grammar_xml, grammar_id)

    def build_grammar(self, command_modules_by_ascending_priority) -> grammar.GrammarContext:
        named_utterances, commands, utterance_priority = self.get_active_named_utterances_and_commands(command_modules_by_ascending_priority)
        cycles = self.calculate_named_utterance_cycles(named_utterances)
        if cycles:
            s = "" if len(cycles) == 1 else "s"
            print(f'Unable to load grammar - found utterance cycle{s}')
            for cycle in cycles:
                print(' -> '.join(cycle))
            print('')
            return
        command_utterances = [cmd.utterance for cmd in commands]
        all_utterances = list(named_utterances.values()) + command_utterances
        node_ids = self.generate_node_ids(all_utterances)
        namespace = self.get_namespace()
        command_contexts = {}
        for cmd in commands:
            variable_tree = variables.RecognitionResultsTree(cmd.utterance, node_ids, named_utterances)
            command_contexts[node_ids[cmd.utterance]] = cmd, variable_tree
        grammar_xml = self.build_grammar_xml(all_utterances, node_ids, named_utterances)
        grammar_context = grammar.GrammarContext(grammar_xml, command_modules_by_ascending_priority, command_contexts, commands, namespace, named_utterances, node_ids, utterance_priority)
        return grammar_context

    def sorted_command_modules(self, command_modules):
        sorted_modules = {}
        for path in sorted(command_modules, key=lambda x: (command_modules[x].priority)):
            sorted_modules[path]  = command_modules[path]
        return sorted_modules

    def get_namespace(self):
        ns = recognition.actions.library.stdlib.namespace.copy()
        for mod in self.active_command_modules.values():
            ns.update(mod.functions)
        return ns

    def save_grammar(self, grammar):
        # remove oldest grammar if needed
        if len(self.grammars) > 4:
            self.grammars.popitem(last=False)
        self.grammars[grammar.uuid] = grammar

    def generate_node_ids(self, utterances):
        node_ids = {}
        for utterance in utterances:
            for node in utterance.walk():
                if node not in node_ids:
                    node_ids[node] = f'n{len(node_ids) + 1}'
        return node_ids

    def fire_activation_events(self, previous_active_modules, current_active_modules, namespace):
        for path, cmd_module in previous_active_modules.items():
            if path not in current_active_modules and 'on_deactivate' in cmd_module.functions:
                source = {'command_module': cmd_module, 'type': 'command_module_deactivated'}
                action = cmd_module.functions['on_deactivate'].action
                perform.perform_action_from_event(action, namespace, source)
        for path, cmd_module in current_active_modules.items():
            if path not in previous_active_modules and 'on_activate' in cmd_module.functions:
                source = {'command_module': cmd_module, 'type': 'command_module_activated'}
                action = cmd_module.functions['on_activate'].action
                perform.perform_action_from_event(action, namespace, source)

    def build_grammar_xml(self, all_active_rules, node_ids, named_rules):
        return SrgsXmlConverter(node_ids, named_rules).build_grammar(all_active_rules)

    def get_active_named_utterances_and_commands(self, command_modules_by_ascending_priority):
        named_utterances = {}
        named_utterances.update(self.special_rules())
        utterance_priority = {}
        active_commands = []
        for cmd_module in command_modules_by_ascending_priority:
            for name, utterance in cmd_module.named_utterances.items():
                utterance_priority[utterance] = cmd_module.priority
                named_utterances[name] = utterance
            for command in cmd_module.commands:
                utterance_priority[command.utterance] = cmd_module.priority
                active_commands.append(command)
        return named_utterances, active_commands, utterance_priority

    def special_rules(self):
        return {'_dictation': astree.Rule()}

    def calculate_named_utterance_cycles(self, named_utterances):
        graph = DirectedGraph()
        for name, utterance in named_utterances.items():
            for utterance_piece in utterance.walk():
                if isinstance(utterance_piece, astree.RuleReference):
                    graph.add_edge(name, utterance_piece.rule_name)
        return self.cycles_from_graph(graph)

    def cycles_from_graph(self, graph):
        nodes_with_cycles = set()
        cycles = []
        for name in graph.adjacency_list:
            cycles.extend(self.dfs(name, graph, (name,), set()))
        return cycles

    def dfs(self, node, graph, root, visited):
        visited.add(node)
        utterance_cycles = []
        adj = graph.adjacency_list[node]
        for adjacent_utterance in adj:
            path = root + (adjacent_utterance,)
            if adjacent_utterance in visited:
                utterance_cycles.append(path)
            else:
                utterance_cycles.extend(self.dfs(adjacent_utterance, graph, path, visited))
        return utterance_cycles

class StaticFileCommandModuleLoader:

    def __init__(self, root, command_module_file_pattern):
        self.root = root
        self.command_module_file_pattern = command_module_file_pattern
        self.file_cache = limited_size_dict.LimitedSizeDict(size_limit=1000)

    def load_files(self):
        directory_contents = {}
        if not os.path.isdir(self.root):
            os.makedirs(self.root)
        directory_contents = self.load_directory(self.root, DEFAULT_DIRECTORY_SETTINGS)
        return directory_contents

    def load_directory(self, path: str, parent_directory_settings):
        command_modules = {}
        directories = []
        local_settings = settings.try_load_json_file(os.path.join(path, '.osspeak.json'))
        directory_settings = {**parent_directory_settings, **local_settings}
        with os.scandir(path) as i:
            for entry in sorted(i, key=lambda x: x.name):
                if entry.name.startswith('.'):
                    continue
                if entry.is_file() and entry.name.endswith('.speak') and self.command_module_file_pattern in entry.name:
                    path = entry.path
                    file = self.file_cache.get(path, CommandModuleFile(path))
                    self.file_cache[path] = file
                    command_modules[path] = file.contents
                # read files in this directory first before recursing down
                elif entry.is_dir():
                    directories.append(entry)
            if directory_settings['recurse']:
                for direntry in directories:
                    command_modules.update(self.load_directory(direntry.path, directory_settings))
        return command_modules

class CommandModuleFile:

    def __init__(self, path):
        self.path = path
        self.last_modified = None
        self._contents = None

    @property
    def contents(self):
        last_modified = os.path.getmtime(self.path)
        if self._contents is None or last_modified > self.last_modified:
            self.last_modified = last_modified
            with open(self.path) as f:
                self._contents = f.read()
        return self._contents

class DirectedGraph:

    def __init__(self):
        self.adjacency_list = {}
        
    def add_edge(self, from_vertex, to_vertex):
        self.add_vertex(from_vertex)
        self.add_vertex(to_vertex)
        self.adjacency_list[from_vertex].add(to_vertex)

    def add_vertex(self, value):
        if value not in self.adjacency_list:
            self.adjacency_list[value] = set()