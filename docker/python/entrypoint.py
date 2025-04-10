# docker/python/entrypoint.py

import json
import importlib.util

def load_function():
    spec = importlib.util.spec_from_file_location("function", "/function/function.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.handler

if __name__ == "__main__":
    with open("/tmp/input.json") as f:
        event = json.load(f)
    handler = load_function()
    output = handler(event)
    print(json.dumps(output))
