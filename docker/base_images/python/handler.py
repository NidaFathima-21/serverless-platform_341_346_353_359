import importlib.util
import os
import json

func_file = os.environ.get("FUNCTION_FILE", "hello.py")
func_path = f"/functions/{func_file}"
raw_args = os.environ.get("ARGS", "[]")

try:
    args = json.loads(raw_args)
except:
    args = []

spec = importlib.util.spec_from_file_location("user_func", func_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

if hasattr(module, 'main'):
    print(module.main(*args))
else:
    print("No main() found")
