#!python

import copy
import re
from collections import defaultdict


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

    print("part 1: " + ''.join(L))


def part2(deps, rev):
    N_WORKERS = 5
    S = {k for k in rev if len(rev[k]) == 0}    # starting elements
    finish_at = {}
    tick = 0

    while True:
        # Do bookkeeping for anything finished and add free things to
        # available work
        to_remove = [n for n in finish_at.keys() if finish_at[n] == tick]
        for n in to_remove:
            finish_at.pop(n)
            for m in sorted(deps[n]):
                deps[n].remove(m)
                rev[m].remove(n)
                if len(rev[m]) == 0:
                    S.add(m)

        # if there are things to do, and workers available, start them
        if len(S):
            todo = list(reversed(sorted(S)))
            workers_avail = N_WORKERS - len(finish_at)

            for i in range(min(workers_avail, len(todo))):
                item = todo.pop()
                S.remove(item)
                time_to_finish = (ord(item) - ord('A')) + 61
                finish_at[item] = tick + time_to_finish

        if len(finish_at) == 0 and len(S) == 0:
            break

        tick += 1

    print(f"part 2: {tick}")


if __name__ == '__main__':
    deps = defaultdict(set)
    rev = defaultdict(set)

    with open('d7.txt') as f:
        for line in f.readlines():
            m = re.match(r'Step ([A-Z]).*before step ([A-Z])', line)
            if m is not None:
                head = m.group(1)
                tail = m.group(2)
                deps[head].add(tail)
                deps[tail]  # get empty
                rev[head]
                rev[tail].add(head)

    part1(deps, rev)
    part2(deps, rev)
