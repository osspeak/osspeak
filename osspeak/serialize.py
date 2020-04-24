import os
import types
import json
import json.decoder
import importlib

import settings

def object_decoder(obj):
    if isinstance(obj, dict) and '__type__' in obj and '__module__' in obj:
        _module = importlib.import_module(obj['__module__'])
        _cls = getattr(_module, obj['__type__'])
        instance = _cls.__new__(_cls)
        for k, v in obj.items():
            if k not in ('__type__', '__module__'):
                setattr(instance, k, object_decoder(v))
        return instance
    return obj

class SimpleJsonEncoder(json.JSONEncoder):

    def default(self, o):
        d = o.__dict__.copy()
        d['__type__'] = o.__class__.__name__
        d['__module__'] = o.__module__
        return d

def to_json_string(obj, encoder):
    return json.dumps(obj, cls=encoder)

def from_text(text: str):
    return json.loads(text, object_hook=object_decoder)

def delete(file_name):
    try:
        os.remove(file_name)
    except FileNotFoundError:
        pass
    
def load(file_name, default_fn=None, object_hook=object_decoder):
    try:
        with open(file_name) as f:
            return json.load(f, object_hook=object_hook)
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        if default_fn is None:
            raise e
        return default_fn()

def save(obj, file_name, cls=SimpleJsonEncoder):
    try:
        with open(file_name, 'w') as f:
            json.dump(obj, f, indent=4, cls=cls)
    except OSError:
        pass
