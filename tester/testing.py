
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

def deepsize(ls):
    if not isinstance(ls, list): return 1
    return sum(deepsize(e) for e in ls)

def add_tag_at(tree, place, tag):
    localplace, left, prev = 0, place, place
    while left > 0 and localplace < len(tree):
        prev = left
        left -= deepsize(tree[localplace])
        localplace += 1
    pre, post = tree[:localplace], tree[localplace:]
    if left == 0:
        if randint(0,1) == 0 and len(post) > 0 and isinstance(post[0], list):
            return pre + [add_tag_at(post[0], 0, tag)] + post[1:]
        return pre + [[tag] if randint(0,1) == 0 else tag] + post
    pre, point = pre[:-1], pre[-1]
    if not isinstance(point, list): return pre + [point, tag] + post
    return pre + [add_tag_at(point, prev, tag)] + post

def generate_flatten():
    result, inp = [], []
    for tag in range(30):
        yield (inp, result)
        place = randint(0, len(inp))
        inp = inp[:place] + [tag] + inp[place:]
        result = add_tag_at(result, place, tag)

test_gens = {
        'fibonacci': generate_fibo,
        'flatten': generate_flatten,
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

