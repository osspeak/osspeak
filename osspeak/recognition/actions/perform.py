import threading
import log
import time
import queue
import collections
import traceback
from lib import keyboard
from settings import settings
import platforms.api
from recognition.actions import context
from recognition.rules import _lark

recognition_queue = queue.Queue()
results_map = {}

def get_recognition_context():
    t = threading.current_thread()
    return results_map[t]['context']

def recognition_namespace():
    recognition_context = get_recognition_context()
    return {'context': recognition_context, **recognition_context._meta.namespace}


def recognition_action_worker():
    while True:
        action, recognition_context = recognition_queue.get()
        t = threading.current_thread()
        results_map[t] = {'context': recognition_context}
        try:
            evaluation = action.perform()
        except Exception as e:
            traceback.print_exc()
            log.logger.error(f'Action {action} errored: {str(e)}')
            print(e)
        finally:
            del results_map[t]

worker = threading.Thread(target=recognition_action_worker, daemon=True)
worker.start()

def perform_io(item):
    if isinstance(item, (str, float, int)):
        keyboard.write(str(item), delay=.05)
        return True
    return False

def perform_action_from_event(action, namespace):
    recognition_context = context.RecognitionContext([], None, namespace, [])
    recognition_queue.put((action, recognition_context))

def perform_commands(grammar_context, words):
    word_list = [word['Text'] for word in words]
    utterance = ' '.join(word_list)
    lark_recognition_tree = grammar_context.lark_grammar.parse(utterance)
    recognition_contexts = get_recognition_contexts(lark_recognition_tree, grammar_context)
    if settings['perform_actions']:
        for recognition_context, command in recognition_contexts:
            recognition_queue.put((command.action, recognition_context))

def get_recognition_contexts(lark_recognition_tree, grammar_context):
    recognition_contexts = []
    for matched_rule in lark_recognition_tree.children:
        words = []
        rule_id = matched_rule.data
        command, variable_tree = grammar_context.command_contexts[rule_id]
        match_variables = collections.OrderedDict({path: [] for path in variable_tree.variables})
        variable_words = collections.OrderedDict({path: [] for path in variable_tree.variables})
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
                    variable_words[path].append(text)
                path = path[:-1]
            if is_substitute:
                substitute_paths.add(start_path)
        variables = tuple(match_variables.values())
        log.logger.info(f'Matched rule: {command.rule.text}')
        formatted_variable_words = tuple(' '.join(x) for x in variable_words.values())
        rec_context = context.RecognitionContext(variables, words, grammar_context.namespace, formatted_variable_words)
        recognition_contexts.append((rec_context, command))
    return recognition_contexts

def get_leaf_action(node, text):
    from recognition.actions import piece
    leaf_action, is_substitute = None, None
    if getattr(node, 'action_piece_substitute', None) is not None:
        leaf_action, is_substitute = node.action_piece_substitute, True 
    elif text is not None:
        escaped = text.replace("'", "\\'")
        leaf_action, is_substitute = piece.DSLActionPiece(f"'{escaped}'"), False
    return leaf_action, is_substitute

def var_result(variable_actions_pieces, perform_results: bool):
    results = []
    for action_piece in variable_actions_pieces:
        results.append(action_piece.perform_variable(perform_results=perform_results))
    if not perform_results:
        return concat_results(results)

def concat_results(results):
    acc = None
    for res in results:
        if None in (acc, res):
            acc = res
        else:
            try:
                acc += res
            except TypeError:
                pass
    return acc