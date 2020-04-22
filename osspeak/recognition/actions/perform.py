import threading
import log
import time
import queue
import collections
import traceback
from lib import keyboard
from settings import settings
import platforms.api
from recognition.actions import context, astree
from recognition.actions.library import _keyboard
from recognition.rules import _lark

recognition_queue = queue.Queue()
results_map = {}

def perform_action(action, context):
    context.argument_frames.append({})
    gen = action.evaluate_lazy(context)
    evaluated_nodes = []
    written_nodes = []
    for i, (node, result) in enumerate(action.evaluate_lazy(context)):
        assert isinstance(node, astree.BaseActionNode)
        if isinstance(result, (str, float, int)):
            if isinstance(node, astree.Literal) and i > 1:
                previous = evaluated_nodes[i - 1]
                if written_nodes and isinstance(written_nodes[-1], astree.Literal) and isinstance(previous, astree.ExprSequenceSeparator):
                    _keyboard.KeyPress.from_raw_text(previous.value).send()
            _keyboard.KeyPress.from_raw_text(str(result)).send()
            written_nodes.append(node)
        elif isinstance(result, _keyboard.KeyPress):
            result.send()
        evaluated_nodes.append(node)
    context.argument_frames.pop()

def recognition_action_worker():
    while True:
        action, recognition_context = recognition_queue.get()
        t = threading.current_thread()
        results_map[t] = {'context': recognition_context}
        try:
            evaluation = perform_action(action, recognition_context)
        except Exception as e:
            traceback.print_exc()
            log.logger.error(f'Action {action} errored: {str(e)}')
            print(e)
        finally:
            del results_map[t]

worker = threading.Thread(target=recognition_action_worker, daemon=True)
worker.start()

def perform_action_from_event(action, namespace):
    recognition_context = context.RecognitionContext([], None, namespace, [])
    recognition_queue.put((action, recognition_context))

def perform_commands(grammar_context, words):
    word_list = [word['Text'] for word in words]
    utterance = ' '.join(word_list)
    lark_recognition_tree = grammar_context.parse_recognition(utterance)
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
        for start_path, text in _lark.yield_paths(matched_rule, variable_tree.node_paths, grammar_context.named_rules):
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
        log.logger.info(f'Matched rule: {command.utterance_text}')
        # formatted_variable_words = tuple(' '.join(x) for x in variable_words.values())
        print(variable_words)
        formatted_variable_words = ()
        rec_context = context.RecognitionContext(variables, words, grammar_context.namespace, formatted_variable_words)
        recognition_contexts.append((rec_context, command))
    return recognition_contexts

def get_leaf_action(node, text):
    leaf_action, is_substitute = None, None
    if getattr(node, 'action_substitute', None) is not None:
        leaf_action, is_substitute = node.action_substitute, True 
    elif text is not None:
        leaf_action, is_substitute = astree.String(text), False
    return leaf_action, is_substitute
