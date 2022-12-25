import atheris

with atheris.instrument_imports():
    import dyn_array
    import sys

methods = [
    lambda a, code: a.make_array(code.pop(0)) if len(code) >= 1 else None,
    lambda a, code: a.get_make_array_status(),
    lambda a, code: a.append(code.pop(0)) if len(code) >= 1 else None,
    lambda a, code: a.insert(code.pop(0), code.pop(0)) if len(code) >= 2 else None,
    lambda a, code: a.get_insert_status(),
    lambda a, code: a.remove(code.pop(0)) if len(code) >= 1 else None,
    lambda a, code: a.get_remove_status(),
    lambda a, code: a.get_count(),
    lambda a, code: a.get_capacity(),
    lambda a, code: a.get_item(code.pop(0)) if len(code) >= 1 else None,
    lambda a, code: a.get_get_item_status(),
]

def TestOneInput(data):
    try:
        a = dyn_array.DynArray()
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
