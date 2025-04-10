# function/python/1/function.py

def handler(event):
    name = event.get("name", "world")
    return f"Hello, {name}!"
