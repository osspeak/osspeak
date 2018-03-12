from profile import Profiler
import itertools
from recognition.actions import library
import uuid
import os
import copy
import re
import collections
import json
import log
import recognition.actions.library.state
from recognition.actions import perform
import settings
from recognition.actions import variables, perform
from recognition.commands import commands, grammar
from recognition.rules.converter import SrgsXmlConverter
import xml.etree.ElementTree as ET
from communication import pubsub, topics

DEFAULT_DIRECTORY_SETTINGS = {
    'recurse': True,
    'conditions': {},
}

class CommandModuleState:

    def __init__(self):
        self.grammars = collections.OrderedDict()
        self.map_grammar_to_commands = collections.OrderedDict()
        self.command_module_json = {}
        self.command_modules = {}
        self.active_command_modules = {}

    def populate(self):
        self.command_module_json = load_command_json()
        self.command_modules = load_command_modules(self.command_module_json)

async def load_modules(command_module_state, current_window, current_state, initialize=False):
    previous_active_modules = command_module_state.active_command_modules
    if initialize:
        command_module_state.populate()
        load_command_module_information(command_module_state.command_modules)
    command_module_state.active_command_modules = get_active_modules(command_module_state.command_modules, current_window, current_state)
    namespace = get_namespace(command_module_state.active_command_modules)
    fire_activation_events(command_module_state.active_command_modules, previous_active_modules, namespace)
    send_module_information_to_ui(command_module_state.command_modules)
    grammar_context = build_grammar(command_module_state.active_command_modules)
    save_grammar(grammar_context, command_module_state.grammars)
    await pubsub.publish_async(topics.LOAD_ENGINE_GRAMMAR, grammar_context)

def build_grammar(active_modules):
    named_rules, command_rules = get_active_rules(active_modules)
    all_rules = list(named_rules.values()) + command_rules
    node_ids = generate_node_ids(all_rules, named_rules)
    active_commands = get_active_commands(active_modules)
    namespace = get_namespace(active_modules)
    command_contexts = {}
    for cmd in active_commands:
        variable_tree = variables.RecognitionResultsTree(cmd.rule, node_ids, named_rules)
        command_contexts[node_ids[cmd.rule]] = {'command': cmd, 'variable_tree': variable_tree, 'namespace': namespace}
    grammar_xml = build_grammar_xml(all_rules, node_ids, named_rules)
    #grammar_id = str(uuid.uuid4())
#    save_grammar(map_grammar_to_commands, command_contexts, grammar_id)
    grammar_context = grammar.GrammarContext(grammar_xml, command_contexts, active_commands, namespace, named_rules)
    return grammar_context

def get_namespace(active_modules):
    ns = library.namespace.copy()
    for mod in active_modules.values():
        ns.update(mod.functions)
    return ns

def save_grammar(grammar, grammars):
    # remove oldest grammar if needed
    if len(grammars) > 4:
        grammars.popitem(last=False)
    grammars[grammar.uuid] = grammar

def generate_node_ids(rules, named_rule_map):
    from recognition.rules import astree
    prefix_map = {astree.GroupingNode: 'g', astree.Rule: 'r', astree.WordNode: 'w'}
    node_ids = {}
    for rule in rules:
        for node_info in rule.walk(rules=named_rule_map):
            node = node_info['node']
            if node not in node_ids:
                prefix = prefix_map.get(type(node), 'n')
                node_ids[node] = f'{prefix}{len(node_ids) + 1}'
    return node_ids

def fire_activation_events(active_modules, previous_active_modules, namespace):
    previous_names, current_names = set(previous_active_modules), set(active_modules)
    for deactivated_name in previous_names - current_names:
        cmd_module = previous_active_modules[deactivated_name]
        if 'deactivate' in cmd_module.events:
            action = cmd_module.events['deactivate']
            perform.perform_action_from_event(action, namespace)
    for activated_name in current_names - previous_names:
        cmd_module = active_modules[activated_name]
        if 'activate' in cmd_module.events:
            action = cmd_module.events['activate']
            perform.perform_action_from_event(action, namespace)

def load_command_json():
    json_module_objects = {}
    command_dir = settings.settings['command_directory']
    if not os.path.isdir(command_dir):
        os.makedirs(command_dir)
    json_module_objects = load_json_directory(command_dir, DEFAULT_DIRECTORY_SETTINGS)
    return json_module_objects

def load_json_directory(path, parent_directory_settings):
    command_modules = {}
    directories = []
    local_settings = settings.try_load_json_file(os.path.join(path, '.osspeak.json'))
    directory_settings = {**parent_directory_settings, **local_settings}
    with os.scandir(path) as i:
        for entry in sorted(i, key=lambda x: x.name):
            if entry.name.startswith('.'):
                continue
            if entry.is_file() and entry.name.endswith('.json'):
                command_modules[entry.path] = load_command_module_file(entry.path)
            # read files in this directory first before recursing down
            elif entry.is_dir():
                directories.append(entry)
        if directory_settings['recurse']:
            for direntry in directories:
                command_modules.update(load_json_directory(direntry.path, directory_settings))
    return command_modules

def load_command_module_file(path):
    with open(path) as f:
        try:
            module_config = json.load(f)
        except json.decoder.JSONDecodeError as e:
            module_config = {'Error': str(e)}
            log.logger.warning(f"JSON error loading command module '{path}':\n{e}")
    return module_config

def load_command_modules(command_module_json):
    return {path: commands.CommandModule(config, path) for path, config in command_module_json.items()}

def load_initial_user_state(command_modules):
    recognition.actions.library.state.USER_DEFINED_STATE = {}
    for path, cmd_module in command_modules.items():
        recognition.actions.library.state.USER_DEFINED_STATE.update(cmd_module.initial_state)

def get_active_modules(command_modules, current_window, current_state):
    active_modules = {}
    for path, cmd_module in command_modules.items():
        if is_command_module_active(cmd_module, current_window, current_state):
            active_modules[path] = cmd_module
    return active_modules

def is_command_module_active(cmd_module, current_window, current_state):
    title_filter = cmd_module.conditions.get('title', '')
    current_window_matches = re.search(title_filter, current_window, flags=re.IGNORECASE)
    return current_window_matches and cmd_module.is_state_active(current_state)

def load_command_module_information(command_modules):
    import_modules(command_modules)
    load_functions(command_modules)
    load_rules(command_modules)
    load_commands(command_modules)
    load_events(command_modules)

def import_modules(command_modules):
    for cmd_module in command_modules.values():
        cmd_module.import_modules()

def load_functions(command_modules):
    for cmd_module in command_modules.values():
        cmd_module.define_functions()
    for cmd_module in command_modules.values():
        cmd_module.set_function_actions()

def load_rules(command_modules):
    for cmd_module in command_modules.values():
        cmd_module.load_rules()

def load_commands(command_modules):
    for cmd_module in command_modules.values():
        cmd_module.load_commands()

def load_events(command_modules):
    for cmd_module in command_modules.values():
        cmd_module.load_events()

def build_grammar_xml(all_active_rules, node_ids, named_rule_map):
    return SrgsXmlConverter(node_ids, named_rule_map).build_grammar(all_active_rules)

def get_active_rules(active_modules):
    rules = {}
    command_rules = []
    for cmd_module in active_modules.values():
        rules.update(cmd_module.rules)
        command_rules.extend(cmd.rule for cmd in cmd_module.commands)
    return rules, command_rules

def get_active_commands(active_modules):
    grouped_commands = [m.commands for m in active_modules.values()]
    return list(itertools.chain.from_iterable(grouped_commands))

def update_modules(self, modified_modules):
    raise NotImplementedError
    command_dir = settings.settings['command_directory']
    for path, cmd_module_config in modified_modules.items():
        self.command_module_json[path] = cmd_module_config
        with open(os.path.join(command_dir, path), 'w') as outfile:
            json.dump(cmd_module_config, outfile, indent=4)
    self.load_modules()

def send_module_information_to_ui(command_modules):
    payload = {'modules': command_modules}
    pubsub.publish(topics.LOAD_MODULE_MAP, payload)

def fetch_module_map(command_modules):
    with self.lock:
        payload = {'modules': command_modules}
    pubsub.publish(topics.LOAD_MODULE_MAP, payload)