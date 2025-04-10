# function/python/2/function.py

def handler(event):
    x = event.get("x", 0)
    y = event.get("y", 0)
    return {"result": x + y}
