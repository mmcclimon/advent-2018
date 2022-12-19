from dataclasses import dataclass
from typing import Self


@dataclass
class Node:
    children: list[Self]
    metadata: list[int]
    length: int

    def metadata_sum(self) -> int:
        return sum(self.metadata +
                   [child.metadata_sum() for child in self.children])

    def value(self) -> int:
        if not self.children:
            return self.metadata_sum()

        val = 0
        for md in self.metadata:
            if md - 1 < len(self.children):
                val += self.children[md-1].value()

        return val


def parse_entry(arr: list[int]) -> Node:
    # print(f"parse! {arr=}")
    i = 0
    done = 0
    while i < len(arr) or done < 100:
        done += 1
        child_len, md_len = arr[i], arr[i+1]
        i += 2

        # print(f"{i=}, {child_len=}, {md_len=}")

        children = []
        for j in range(child_len):
            child = parse_entry(arr[i:])
            children.append(child)

            i += child.length
            # print(f"adding {child.length} to i")

        md = arr[i:i+md_len]
        i += md_len
        return Node(children=children, metadata=md, length=i)

    raise Exception('unreachable?')


# if True:
with open('d8.txt') as f:
    s = f.read()
    # s = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
    s.strip()
    arr: list[int] = list(map(int, s.split(' ')))

    node = parse_entry(arr)
    print(f"part 1: {node.metadata_sum()}")
    print(f"part 2: {node.value()}")
