import threading
import log
import time
import queue
import collections
import keyboard
from settings import settings
import platforms.api
from recognition.actions import context
from recognition.rules import _lark, astree

recognition_queue = queue.Queue()
results_map = {}

def get_recognition_context():
    t = threading.current_thread()
    return results_map[t]['context']

def recognition_action_worker():
    while True:
        action, recognition_context = recognition_queue.get()
        t = threading.current_thread()
        results_map[t] = {'context': recognition_context}
        try:
            evaluation = action.perform()
        except Exception as e:
            log.logger.error(f'Action {action.text} errored: {str(e)}')
            print(e)
        finally:
            del results_map[t]

worker = threading.Thread(target=recognition_action_worker, daemon=True)
worker.start()

def perform_io(item):
    if isinstance(item, (str, float, int)):
        keyboard.write(str(item))
        return True
    return False

def perform_action_from_event(action, namespace):
    recognition_context = context.create_event_context(namespace)
    recognition_queue.put((action, recognition_context))

def perform_commands(grammar_context, words):
    word_list = [word['Text'] for word in words]
    utterance = ' '.join(word_list)
    lark_recognition_tree = grammar_context.lark_grammar.parse(utterance)
    for matched_rule in lark_recognition_tree.children:
        words = []
        rule_id = matched_rule.data
        command_context = grammar_context.command_contexts[rule_id]
        variable_tree = command_context['variable_tree']
        match_variables  = collections.OrderedDict({path: [] for path in variable_tree.variables})
        substitute_paths = set()
        for start_path, text in _lark.yield_paths(matched_rule, variable_tree.node_paths):
            if text is not None:
                words.extend(text.split())
            node = variable_tree.node_paths[start_path]
            action, is_substitute = get_leaf_action(node, text)
            if action is None:
                continue
            path = start_path
            while path:
                if path in substitute_paths:
                    break
                if path in match_variables:
                    match_variables[path].append(action)
                path = path[:-1]
            if is_substitute:
                substitute_paths.add(start_path)
        command = command_context['command']
        variables = tuple(match_variables.values())
        action_result = perform_action(command, variables, grammar_context.namespace, tuple(words))

def get_leaf_action(node, text):
    from recognition import action
    leaf_action, is_substitute = None, None
    if getattr(node, 'action_substitute', None) is not None:
        leaf_action, is_substitute = node.action_substitute, True 
    elif text is not None:
        leaf_action, is_substitute = action(f"'{text}'"), False
    return leaf_action, is_substitute

def perform_action(command, variables, namespace, words):
    log.logger.info(f'Matched rule: {command.rule.raw_text}')
    recognition_context = context.RecognitionContext(variables, words, namespace)
    recognition_queue.put((command.action, recognition_context))
    
def var_result(variable_actions, perform_results):
    results = []
    for action in variable_actions:
        results.append(action.perform_variable(perform_results=perform_results))
    if not perform_results:
        return concat_results(results)

def concat_results(results):
    acc = None
    for res in results:
        if acc is None:
            acc = res
        else:
            try:
                acc += res
            except TypeError:
                pass
    return acc