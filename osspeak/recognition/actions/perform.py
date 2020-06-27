import threading
import log
import time
import queue
import collections
import traceback
from settings import settings
import platforms.api
from recognition.actions import context, astree
from recognition.actions.library import _keyboard, macro
from recognition.rules import _lark

recognition_queue = queue.Queue()
recognition_history = collections.deque(maxlen=100)

class RecognitionEvent:

    def __init__(self, words):
        self.words = words

class ActionPerformContext:

    def __init__(self, action: astree.BaseActionNode, recognition_context: context.RecognitionContext, source):
        self.action = action
        self.recognition_context = recognition_context
        self.source = source

def recognition_action_worker():
    while True:
        queued_action_context = recognition_queue.get()
        # action, recognition_context, source = recognition_queue.get()
        try:
            evaluation = queued_action_context.action.perform(queued_action_context.recognition_context)
        except Exception as e:
            traceback.print_exc()
            log.logger.error(f'Action {queued_action_context.action} errored: {str(e)}')
            print(e)
        recognition_history.append(queued_action_context)
        for m in macro.recording_macros.values():
            m.action_contexts.append(queued_action_context)

worker = threading.Thread(target=recognition_action_worker, daemon=True)
worker.start()

def perform_action_from_event(action, namespace, source):
    recognition_context = context.RecognitionContext([], None, namespace)
    queued_action = ActionPerformContext(action, recognition_context, source)
    recognition_queue.put(queued_action)

def perform_commands(grammar_context, words):
    word_list = [word['Text'] for word in words]
    utterance = ' '.join(word_list)
    lark_recognition_tree = grammar_context.parse_recognition(utterance)
    recognition_contexts = get_recognition_contexts(lark_recognition_tree, grammar_context)
    recognition_event = RecognitionEvent(word_list)
    source = {'type': 'recognition_event', 'event': recognition_event}
    if settings['perform_actions']:
        for recognition_context, command in recognition_contexts:
            queued_action = ActionPerformContext(command.action, recognition_context, source)
            recognition_queue.put(queued_action)

def get_recognition_contexts(lark_recognition_tree, grammar_context):
    recognition_contexts = []
    for matched_rule in lark_recognition_tree.children:
        words = []
        rule_id = matched_rule.data
        command, variable_tree = grammar_context.command_contexts[rule_id]
        match_variables = collections.OrderedDict({path: [] for path in variable_tree.variables})
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
                if path in match_variables:
                    match_variables[path].append(action)
                path = path[:-1]
                if path in substitute_paths:
                    break
            if is_substitute:
                substitute_paths.add(start_path)
        variables = tuple([consolidate_variables(x) for x in match_variables.values()])
        log.logger.info(f'''Matched rule: {command.utterance_text} with words "{' '.join(words)}"''')
        rec_context = context.RecognitionContext(variables, words, grammar_context.namespace)
        recognition_contexts.append((rec_context, command))
    return recognition_contexts
    
def get_leaf_action(node, text):
    leaf_action, is_substitute = None, None
    if getattr(node, 'action_substitute', None) is not None:
        leaf_action, is_substitute = node.action_substitute, True 
    elif text is not None:
        leaf_action, is_substitute = astree.Literal(text), False
    return leaf_action, is_substitute

def consolidate_variables(var_actions):
    if len(var_actions) == 1:
        return var_actions[0]
    expressions = []
    for expr in var_actions[:-1]:
        expressions.extend([expr, astree.ExprSequenceSeparator(' ')])
    try:
        expressions.append(var_actions[-1])
    except IndexError:
        pass
    return astree.ExpressionSequence(expressions)
