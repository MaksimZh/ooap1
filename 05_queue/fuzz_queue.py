import atheris

with atheris.instrument_imports():
    import my_queue
    import sys

methods = [
    lambda a, code: a.enqueue(code.pop(0)) if len(code) >= 1 else None,
    lambda a, code: a.dequeue(),
    lambda a, code: a.get_dequeue_status(),
    lambda a, code: a.get(),
    lambda a, code: a.get_get_status(),
    lambda a, code: a.get_size(),
]

def TestOneInput(data):
    try:
        a = my_queue.Queue()
        code = list(data)
        while len(code) > 0:
            command = code.pop(0)
            methods[command % len(methods)](a, code)
    except:
        d = list(data)
        print(d[: len(d) - len(code)])
        raise


atheris.Setup(sys.argv, TestOneInput)
atheris.Fuzz()
