from collections import defaultdict


def c2b(c: str) -> bool:
    return c == "#"


def char_for(val: bool) -> str:
    return "#" if val else "."


def to_zero(indexes):
    delta = 0 - indexes[0]
    return tuple(i + delta for i in indexes)


class PlantLine:
    def __init__(self, line, rules):
        line = line.removeprefix("initial state: ")
        self.rules = rules
        self.pots = defaultdict(bool)
        self.generation = 0

        self._min = 0
        self._max = len(line)

        for i, char in enumerate(line):
            self.pots[i] = c2b(char)

    def _range(self, *, extended=False):
        if extended:
            yield from range(self._min - 2, self._max + 2)
        else:
            yield from range(self._min, self._max)

    def __str__(self):
        return "".join(char_for(self.pots[i]) for i in self._range())

    def do_generation(self):
        future = defaultdict(bool)

        for i in self._range(extended=True):
            future[i] = self.rules[self.surrounding(i)]

        self.pots = future
        self.generation += 1
        self._trim()

    def surrounding(self, pot):
        return tuple(self.pots[i] for i in range(pot - 2, pot + 3))

    def plant_indexes(self):
        return [i for i, pot in self.pots.items() if pot]

    def sum(self):
        return sum(self.plant_indexes())

    def _trim(self):
        # we know that ..... => ., so we don't need to keep going forever

        for i in self._range(extended=True):
            if any(self.surrounding(i)):
                continue

            del self.pots[i]

        indexes = self.plant_indexes()
        self._min = min(indexes)
        self._max = max(indexes) + 1

    def find_stable(self):
        prev = self.plant_indexes()
        while True:
            self.do_generation()
            cur = self.plant_indexes()
            if to_zero(prev) == to_zero(cur):
                return

            prev = cur


class Rules:
    def __init__(self, lines):
        self.rules = set()

        for line in lines:
            state, result = line.split(" => ")
            if result == "#":
                vals = tuple(map(c2b, state))
                self.rules.add(vals)

    def __getitem__(self, item) -> bool:
        return item in self.rules


with open('d12.txt') as f:
    lines = [line.strip() for line in f]
    rules = Rules(lines[2:])
    plants1 = PlantLine(lines[0], rules)
    plants2 = PlantLine(lines[0], rules)

# part 1
for i in range(20):
    plants1.do_generation()

print(f"part 1: {plants1.sum()}")

# part 2
plants2.find_stable()
indexes = plants2.plant_indexes()

delta = 50_000_000_000 - plants2.generation
at_time = [i + delta for i in indexes]
print(f"part 2: {(sum(at_time))}")
