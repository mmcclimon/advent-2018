from collections import Counter
from collections.abc import Collection
from dataclasses import dataclass, field
from enum import Enum
import itertools
from typing import Iterator


class Map:
    def __init__(self, plan, carts):
        self.plan = plan
        self.carts = carts
        self._tick = 0

    @classmethod
    def parse(cls, lines):
        plan = []
        table = str.maketrans("<>^v", "--||")
        plan = [list(line) for line in lines]
        carts = CartSet()

        for y, line in enumerate(plan):
            for x, char in enumerate(line):
                if char in "><^v":
                    carts.add(Cart(x, y, char))
                    plan[y][x] = char.translate(table)

        return cls(plan, carts)

    def __str__(self):
        ret = []
        for y, row in enumerate(self.plan):
            line = []

            for x, char in enumerate(row):
                if cart := self.carts.cart_at(x, y):
                    line.append(cart.direction)
                else:
                    line.append(char)

            ret.append("".join(line))

        return "\n".join(ret)

    def tick(self):
        for cart in self.carts:
            cart.move(self.plan)

        self._tick += 1

    def run_until_crash(self):
        while True:
            for cart in self.carts:
                # print(f"{(cart.x, cart.y)} ", end="")
                cart.move(self.plan)

                if crash := self.carts.get_crash():
                    return to_output(crash)

    def last_cart_standing(self):
        while True:
            for cart in self.carts:
                cart.move(self.plan)

                if crash := self.carts.get_crash():
                    self.carts.remove(crash)

            if len(self.carts) == 1:
                return to_output(self.carts.carts[0].coords())


class CartSet(Collection):
    def __init__(self):
        self.carts = []

    def add(self, cart):
        self.carts.append(cart)

    def __len__(self):
        return len(self.carts)

    def __contains__(self, coords):
        return bool(self.cart_at(*coords))

    def __iter__(self):
        yield from sorted(self.carts)

    def cart_at(self, x, y):
        for cart in self.carts:
            if cart.coords() == (x, y):
                return cart

        return None

    def get_crash(self):
        locs = Counter((c.x, c.y) for c in self.carts)
        if len(locs) == len(self.carts):
            return

        # oh no!
        for loc, count in locs.items():
            if count > 1:
                return loc

    def remove(self, coords):
        self.carts = [c for c in self.carts if c.coords() != coords]


def to_output(tup):
    return ",".join(map(str, tup))


Turn = Enum("Turn", ["LEFT", "STRAIGHT", "RIGHT"])

DIRECTIONS = {
    "\\": {
        "<": "^",
        ">": "v",
        "v": ">",
        "^": "<",
    },
    "/": {
        "<": "v",
        ">": "^",
        "v": "<",
        "^": ">",
    },
}

TURNS = {
    Turn.LEFT: {
        "<": "v",
        ">": "^",
        "v": ">",
        "^": "<",
    },
    Turn.RIGHT: {
        "<": "^",
        ">": "v",
        "v": "<",
        "^": ">",
    },
    Turn.STRAIGHT: {
        "<": "<",
        ">": ">",
        "v": "v",
        "^": "^",
    },
}


@dataclass
class Cart:
    x: int
    y: int
    direction: str
    next_turn: Iterator[Turn] = field(
        default_factory=lambda: itertools.cycle([Turn.LEFT, Turn.STRAIGHT, Turn.RIGHT])
    )

    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x

        return self.y < other.y

    def coords(self):
        return self.x, self.y

    def move(self, plan):
        match self.direction:
            case "<":
                self.x -= 1
            case ">":
                self.x += 1
            case "v":
                self.y += 1
            case "^":
                self.y -= 1

        char = plan[self.y][self.x]
        if char in "-|":
            return

        if char == "+":
            turn = next(self.next_turn)
            self.direction = TURNS[turn][self.direction]
            return

        self.direction = DIRECTIONS[char][self.direction]


with open("d13.txt") as f:
    lines = f.readlines()

print("part 1: ", Map.parse(lines).run_until_crash())
print("part 2: ", Map.parse(lines).last_cart_standing())
