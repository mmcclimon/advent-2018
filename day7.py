#!python

import copy
import re
from collections import defaultdict, deque

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
    head = m.group(1)
    tail = m.group(2)
    deps[tail]  # get empty
    deps[head].add(tail)


# Kahn's algorithm
def kahn(deps):
    L = []      # Empty list that will contain the sorted elements
    S = set()   # Set of all nodes with no incoming edge
    to_delete = set()
    graph = copy.deepcopy(deps)
    for k,v in graph.items():
        if len(v) == 0:
            S.add(k)

    total = 0
    while len(S):
        n = S.pop()
        del graph[n]

        L.append(n)
        for m, edges in sorted(graph.items()):
            if n in edges:
                edges.remove(n)
            if not edges:
                S.add(m)

        total += 1

    return L


class Node:
    def __init__(self, name, children):
        self.name = name
        self.children = children
        self.t_mark = False
        self.p_mark = False

    def __repr__(self):
        return "<Node {}, children={}".format(self.name, self.children)

    def visit(self, L, nodelist):
        print("visit({})".format(self.name))
        if self.p_mark:
            print("  already in L, nothing to do")
            return
        if self.t_mark:
            raise Exception('not a DAG')
        self.t_mark = True
        for node_name in reversed(sorted(self.children)):
            n = nodelist.d[node_name]
            print("  at {}, gonna visit {}".format(self.name, node_name))
            n.visit(L, nodelist)
        self.p_mark = True
        print("  adding {} to head".format(self.name))
        L.appendleft(self)

class NodeList:
    def __init__(self, d):
        self.d = d

    def add(self, node):
        self.d[ node.name ] = node

    def has_unmarked_nodes(self):
        for node in self.d.values():
            if not node.t_mark and not node.p_mark:
                return True
        return False



nl = NodeList({})
for k, v in deps.items():
    print(k, v)
    nl.add(Node(k,v))

print(deps)

L = deque()
while nl.has_unmarked_nodes():
    to_visit = None;
    for node in nl.d.values():
        node.visit(L, nl)

output = []
for n in L:
    output.append(n.name)
print(output)
