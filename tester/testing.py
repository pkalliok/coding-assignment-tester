
from requests import post
from random import randint, choice
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

vowels = 'aeiouyåä'
def random_vowel(): return choice(vowels)
def random_consonant(): return choice('bcdðfghjkĸlmnpqrsštvwxz')

def random_repeat(element):
    if randint(0,1) == 0: return ''
    return random_repeat(element) + element()

def random_start():
    return random_repeat(random_consonant) + \
            random_vowel() + (random_vowel() if randint(0,2) == 0 else '')

def random_non_start():
    return random_consonant() + random_start()

def random_end():
    return random_repeat(random_non_start) + random_repeat(random_consonant)

def random_swap_pair():
    st1, st2 = random_start(), random_start()
    end1, end2 = random_end(), random_end()
    sp = ' ' + random_repeat(lambda: ' ')
    return (st1 + end1 + sp + st2 + end2, st2 + end1 + sp + st1 + end2)

def random_swapped_sentence():
    if randint(0,3) == 0: return random_swap_pair()
    if randint(0,2) == 0:
        word = random_start() + random_end()
        return (word, word)
    s1, s2 = random_swapped_sentence()
    w1, w2 = random_swap_pair()
    sp = ' ' + random_repeat(lambda: ' ')
    return (w1 + sp + s1, w2 + sp + s2)

def generate_swaps():
    for i in range(30): yield random_swapped_sentence()

def random_numbers(n):
    return [randint(1,99) for _ in range(randint(0,n))]

def extend_toplevel_zero(tree, mind, maxd):
    return ([0] + tree + [0], 1, 1 if maxd is None else maxd)

def extend_toplevel_nonzero(tree, mind, maxd):
    return (random_numbers(3) + tree + random_numbers(3), mind, maxd)

def embed_toplevel(tree, mind, maxd):
    return ([tree],
            None if mind is None else mind+1,
            None if maxd is None else maxd+1)

def embed_toplevel_imbalance(tree, mind, maxd):
    return ([tree] + random_numbers(3) + [[tree]],
            None if mind is None else mind+1,
            None if maxd is None else maxd+2)

def generate_zero_trees():
    tree, mindepth, maxdepth = [], None, None
    tree_trans = [extend_toplevel_zero, extend_toplevel_nonzero,
            embed_toplevel, embed_toplevel_imbalance]
    for i in range(30):
        tree, mindepth, maxdepth = choice(tree_trans)(tree, mindepth, maxdepth)
        yield (tree, [mindepth, maxdepth])

test_gens = {
        'fibonacci': generate_fibo,
        'flatten': generate_flatten,
        'sananmuunnos': generate_swaps,
        'zerodepth': generate_zero_trees,
}

def run_test_against(endpoint, inp, expected):
    try: req = post(endpoint, verify=False, json=inp)
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

