import json
import traceback
import os
import importlib

import settings
import serialize
import log

def record(name):
    m = Macro()
    recording_macros[name] = m

def stop(name=None):
    names = list(recording_macros) if name is None else [name]
    for name in names:
        m = recording_macros.get(name)
        if m is None:
            log.logger.warn(f'No macro named {name}')
        else:
            m.action_contexts = m.action_contexts[1:] # remove record command
            macros[name] = m
            del recording_macros[name]
    serialize.save(macros, settings.settings['macros'], cls=MacroJsonEncoder)

def play(name):
    if name not in macros:
        log.logger.warn(f'No macro named {name}')
    for action_context in macros[name].action_contexts:
        try:
            evaluation = action_context.action.perform(action_context.recognition_context)
        except Exception as e:
            traceback.print_exc()
            log.logger.error(f'Action {action_context.action} errored: {str(e)}')
            print(e)

def _restore_saved():
    from recognition.actions.library import stdlib
    saved_macros = serialize.load(settings.settings['macros'], lambda: {})
    for m in saved_macros.values():
        for action_context in m.action_contexts:
            action_context.recognition_context.namespace = {**stdlib.namespace, **action_context.recognition_context.namespace} 
    macros.update(saved_macros)
    return macros

class Macro:

    def __init__(self):
        self.action_contexts = []

class MacroJsonEncoder(serialize.SimpleJsonEncoder):

    def default(self, o):
        from recognition.actions import context, astree
        if isinstance(o, context.RecognitionContext):
            d = o.__dict__.copy()
            d['__type__'] = o.__class__.__name__
            d['__module__'] = o.__module__
            ns = {}
            for k, v in d['namespace'].items():
                if isinstance(v, (astree.FunctionDefinition, astree.BaseActionNode)):
                    ns[k] = v
            d['namespace'] = ns
            return d
        return super().default(o)

macros = {} # update from _restore_saved in stdlib to avoid import issues
recording_macros = {}