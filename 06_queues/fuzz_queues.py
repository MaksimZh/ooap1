import atheris

with atheris.instrument_imports():
    import queues
    import sys

methods1 = [
    lambda a, code: a.get_size(),
    lambda a, code: a.put_tail(code.pop(0)) if len(code) >= 1 else None,
    lambda a, code: a.pop_front(),
    lambda a, code: a.get_pop_front_status(),
    lambda a, code: a.get_front(),
    lambda a, code: a.get_get_front_status(),
]

methods2 = methods1 + [
    lambda a, code: a.put_front(code.pop(0)) if len(code) >= 1 else None,
    lambda a, code: a.pop_tail(),
    lambda a, code: a.get_pop_tail_status(),
    lambda a, code: a.get_tail(),
    lambda a, code: a.get_get_tail_status(),
]

def launch(obj, methods, code):
    c = code.copy()
    try:
        while len(c) > 0:
            command = c.pop(0)
            methods[command % len(methods)](obj, c)
    except:
        print(type(obj), code[: len(code) - len(c)])
        raise

def TestOneInput(data):
    code = list(data)
    launch(queues.Queue(), methods1, code)
    launch(queues.Deque(), methods2, code)


atheris.Setup(sys.argv, TestOneInput)
atheris.Fuzz()
