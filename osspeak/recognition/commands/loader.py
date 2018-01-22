from profile import Profiler
import itertools
from recognition.actions import library
import uuid
import profile
import os
import collections
import json
import log
import recognition.actions.library.state
from recognition.actions import perform
import settings
from interfaces.gui import serializer
from recognition.actions import variables
from recognition.commands import commands
from recognition.rules.converter import SrgsXmlConverter
from platforms import api
import xml.etree.ElementTree as ET
from communication import messages, pubsub, topics

class CommandModuleCache:

    def __init__(self):
        self.map_grammar_to_commands = collections.OrderedDict()
        self.command_module_json = {}
        self.command_modules = {}
        self.active_command_modules = {}

    def populate(self):
        self.command_module_json = load_command_json()
        self.command_modules = load_command_modules(self.command_module_json)

async def load_modules(cache, current_window, current_state, initialize=False):
    previous_active_modules = cache.active_command_modules
    if initialize:
        cache.populate()
        load_command_module_information(cache.command_modules)
    cache.active_modules = get_active_modules(cache.command_modules, current_window, current_state)
    fire_activation_events(cache.active_modules, previous_active_modules)
    send_module_information_to_ui(cache.command_modules)
    grammar_id, grammar_xml = build_grammar(cache.active_modules, cache.map_grammar_to_commands)
    await pubsub.publish_async(topics.LOAD_ENGINE_GRAMMAR, ET.tostring(grammar_xml).decode('utf8'), grammar_id)

def build_grammar(active_modules, map_grammar_to_commands):
    rules, command_rules = get_active_rules(active_modules)
    all_rules = list(rules.values()) + command_rules
    node_ids = generate_node_ids(all_rules, rules)
    active_commands = get_active_commands(active_modules)
    namespace = get_namespace(active_modules)
    command_contexts = {}
    for cmd in active_commands:
        variable_tree = variables.RecognitionResultsTree(cmd.rule, node_ids, rules)
        command_contexts[node_ids[cmd.rule]] = {'command': cmd, 'variable_tree': variable_tree, 'namespace': namespace}
    grammar_xml = build_grammar_xml(all_rules, node_ids, rules)
    grammar_id = str(uuid.uuid4())
    save_command_contexts(map_grammar_to_commands, command_contexts, grammar_id)
    return grammar_id, grammar_xml

def get_namespace(active_modules):
    ns = library.namespace.copy()
    for mod in active_modules.values():
        ns.update(mod.functions)
    return ns

def save_command_contexts(map_grammar_to_commands, command_contexts, grammar_id):
    # remove oldest grammar if needed
    if len(map_grammar_to_commands) > 4:
        map_grammar_to_commands.popitem(last=False)
    map_grammar_to_commands[grammar_id] = command_contexts

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

def fire_activation_events(active_modules, previous_active_modules):
    previous_names, current_names = set(previous_active_modules), set(active_modules)
    for deactivated_name in previous_names - current_names:
        cmd_module = previous_active_modules[deactivated_name]
        if 'deactivate' in cmd_module.events:
            cmd_module.events['deactivate'].perform(variables=[])
    for activated_name in current_names - previous_names:
        cmd_module = active_modules[activated_name]
        if 'activate' in cmd_module.events:
            cmd_module.events['activate'].perform(variables=[])

def load_command_json():
    json_module_dicts = {}
    command_dir = settings.settings['command_directory']
    if not os.path.isdir(command_dir):
        os.makedirs(command_dir)
    for root, dirs, filenames in os.walk(command_dir):
        # skip hidden directories such as .git
        dirs[:] = sorted([d for d in dirs if not d.startswith('.')])
        directory_modules = load_json_directory(filenames, command_dir, root)
        json_module_dicts.update(directory_modules)
    return json_module_dicts

def load_json_directory(filenames, command_dir, root):
    directory_modules = {}
    for fname in sorted(filenames):
        if not fname.endswith('.json'):
            continue
        full_path = os.path.join(root, fname)
        partial_path = full_path[len(command_dir) + 1:]
        log.logger.debug(f"Loading command module '{partial_path}'...")
        with open(full_path) as f:
            try:
                module_config = json.load(f)
            except json.decoder.JSONDecodeError as e:
                module_config = {'Error': str(e)}
                log.logger.warning(f"JSON error loading command module '{partial_path}':\n{e}")
            directory_modules[partial_path] = module_config
    return directory_modules

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
    title_filter = cmd_module.conditions.get('title')
    current_window_matches = title_filter is None or title_filter.lower() in current_window.lower() 
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