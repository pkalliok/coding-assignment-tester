
from requests import post
from random import randint
from json.decoder import JSONDecodeError

class FailedTest(Exception):
    def __init__(s, **kw): s.content = kw
    def __str__(s): return repr(s.content)

def shorten(text, length):
    return text if len(text) < length else text[:length-3] + '...'

def generate_fibo():
    a, b = 1, 0
    for i in range(30):
        yield (i+1, a)
        a, b = a+b, a

test_gens = {
        'fibonacci': generate_fibo,
}

def run_test_against(endpoint, inp, expected):
    try: req = post(endpoint, json=inp)
    except Exception as e:
        raise FailedTest(reason='Calling endpoint failed', endpoint=endpoint,
                problem=repr(e))
    try: result = req.json()
    except JSONDecodeError as e:
        raise FailedTest(reason='Decoding output failed', endpoint=endpoint,
                input=inp, expected=expected, result=shorten(req.text, 20),
                problem=repr(e))
    if result != expected:
        raise FailedTest(reason='Wrong output from endpoint', input=inp,
                expected=expected, result=result)
    return (inp, result)

def run_tests_against(assignment, endpoint):
    try: generator = test_gens[assignment]
    except KeyError:
        raise FailedTest(reason='Unknown assignment', unknown=assignment)
    return [run_test_against(endpoint, inp, expected)
            for inp, expected in generator()]

