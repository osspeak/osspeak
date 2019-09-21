import json
import importlib
import settings

def to_json_string(obj):
    return json.dumps(obj, cls=SimpleJsonEncoder)

def from_text(text: str):
    return json.loads(text, object_hook=object_decoder)

def load_cache():
    try:
        with open(settings.settings['cache']) as f:
            return json.load(f)
    except FileNotFoundError:
        return empty_cache()

def empty_cache():
    return {'command_modules': {}}

def save_cache(command_module_cache):
    try:
        with open(settings.settings['cache'], 'w') as f:
            json.dump(command_module_cache, f, indent=4)
    except OSError:
        pass

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