#!python

from pprint import pp
import copy
import re
from collections import defaultdict

instructions = [
    'Step C must be finished before step A can begin.',
    'Step C must be finished before step F can begin.',
    'Step A must be finished before step B can begin.',
    'Step A must be finished before step D can begin.',
    'Step B must be finished before step E can begin.',
    'Step D must be finished before step E can begin.',
    'Step F must be finished before step E can begin.',
]

deps = defaultdict(set)
rev = defaultdict(set)

for line in instructions:
    m = re.match(r'Step ([A-Z]).*before step ([A-Z])', line)
    if m is not None:
        head = m.group(1)
        tail = m.group(2)
        deps[head].add(tail)
        deps[tail]  # get empty
        rev[head]
        rev[tail].add(head)

# real one
# with open('d7.txt') as f:
#     for line in f.readlines():
#         m = re.match(r'Step ([A-Z]).*before step ([A-Z])', line)
#         if m is not None:
#             head = m.group(1)
#             tail = m.group(2)
#             deps[head].add(tail)
#             deps[tail]  # get empty
#             rev[head]
#             rev[tail].add(head)


# this is kahn's algorithm, modified
def part1(deps, rev):
    deps = copy.deepcopy(deps)
    rev = copy.deepcopy(rev)
    S = {k for k in rev if len(rev[k]) == 0}
    L = []
    while len(S):
        n = sorted(S)[0]
        S.remove(n)
        L.append(n)
        for m in sorted(deps[n]):
            deps[n].remove(m)
            rev[m].remove(n)
            if len(rev[m]) == 0:
                S.add(m)

    print(''.join(L))


def part2(deps, rev):
    N_WORKERS = 2
    # starting elements
    S = {k for k in rev if len(rev[k]) == 0}
    finish_at = {}
    tick = 0

    while len(S):
        todo = sorted(S)


    # at every tick:
    # - are there things available
    #   if yes, and there is a worker available:
    #     - start work, keep track of when to finish
    # - when a thing finishes:
    #   - do bookkeeping for edges
    #   - add free things to avaiable work


part1(deps, rev)
part2(deps, rev)
