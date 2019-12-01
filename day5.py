#!python

import string

s = 'dabAcCaCBAcCcaDA';
with open('d5.txt') as f:
    s = (f.readlines())[0].strip()

def should_remove(c1, c2):
    return c1.lower() == c2.lower() and (
            (c1.islower() and c2.isupper()) or
            (c1.isupper() and c2.islower()))

def do_pass(s):
    s2 = []
    i = 0
    at_end = False
    while i < len(s):
        c = s[i]
        d = None
        try:
            d = s[i+1]
        except IndexError:
            d = ''

        if should_remove(c,d):
            i += 1  # skip next one
        else:
            s2.append(c)

        i += 1

    return ''.join(s2)

def do_all_passes(orig):
    ret = ''
    s = orig

    while s != ret:
        ret = do_pass(s)
        s = do_pass(ret)

    return ret

def do_with_letters(s):
    ret = {}
    for letter in string.ascii_lowercase:
        t = { ord(letter): None, ord(letter.upper()): None }
        length = len(do_all_passes(s.translate(t)))
        ret[letter] = length
        print("did {}: len is {}".format(letter, length))

    res = None
    for k in ret:
        if not res:
            res = (k, ret[k])
        elif ret[k] < res[1]:
            res = (k, ret[k])

    print(res)

do_with_letters(s)
