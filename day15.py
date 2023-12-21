from enum import StrEnum
from dataclasses import dataclass
import math


def main():
    with open("d15.txt") as f:
        lines = [line.strip() for line in f]

    grid = Grid(lines)

    grid.play_game()


class Kind(StrEnum):
    WALL = "#"
    OPEN = "."
    ELF = "E"
    GOBLIN = "G"

    @classmethod
    def from_str(cls, s):
        return {
            "#": cls.WALL,
            ".": cls.OPEN,
            "E": cls.ELF,
            "G": cls.GOBLIN,
        }[s]

    def is_attacker(self):
        return self == self.ELF or self == self.GOBLIN


@dataclass
class Tile:
    kind: Kind

    def is_attacker(self):
        return False

    def is_open(self):
        return self.kind == Kind.OPEN


@dataclass
class Attacker:
    kind: Kind
    hp: int = 200
    atk: int = 3

    def is_attacker(self):
        return True

    def is_open(self):
        return False


class Grid:
    def __init__(self, lines):
        self.max_r = len(lines)
        self.max_c = len(lines[0])

        self.g = {}

        for r, line in enumerate(lines):
            for c, char in enumerate(line):
                kind = Kind.from_str(char)
                self.g[r, c] = Attacker(kind) if kind.is_attacker() else Tile(kind)

    def __str__(self):
        lines = []
        for r in range(self.max_r):
            line = []
            for c in range(self.max_c):
                line.append(self.g[r, c].kind)

            lines.append("".join(line))

        return "\n".join(lines)

    def attackers(self):
        return sorted(pos for pos, ent in self.g.items() if ent.is_attacker())

    def non_walls(self):
        return sorted(pos for pos, ent in self.g.items() if ent.kind != Kind.WALL)

    def play_game(self):
        rounds_completed = 0

        while True:
            go_on = self.do_round()
            if not go_on:
                break

            rounds_completed += 1

        print(self)
        print(f"game ends after {rounds_completed} rounds")
        hp = sum(self.g[pos].hp for pos in self.attackers())
        print(hp * rounds_completed)

    def do_round(self):
        to_move = self.attackers()

        for pos in to_move:
            who = self.g[pos]
            if who.is_open():  # it dead
                continue

            if not self.targets_for(who):
                return False

            pos = self.move(who, pos)

            if tpos := self.best_target(who, pos):
                target = self.g[tpos]
                target.hp -= who.atk
                if target.hp <= 0:
                    self.g[tpos] = Tile(Kind.OPEN)

        return True

    def move(self, who, pos):
        targets = self.targets_for(who)
        assert targets

        if self.adjacent_targets(who, pos):
            return pos

        in_range = self.in_range_of(targets)
        dists = {
            pos: dist
            for pos, dist in self.distances_from(pos).items()
            if pos in in_range
        }

        if not dists:
            return pos

        best_dist = min(dist for dist in dists.values())
        nearest = min(pos for pos, dist in dists.items() if dist == best_dist)

        next_pos = self.step_toward(pos, nearest)
        self.g[next_pos] = who
        self.g[pos] = Tile(Kind.OPEN)
        return next_pos

    def adjacent_targets(self, who, pos):
        targets = self.targets_for(who)
        return [n for n in self.neighbors(pos) if n in targets]

    def best_target(self, who, pos):
        targets = self.adjacent_targets(who, pos)
        if not targets:
            return None

        def key(k):
            unit = self.g[k]
            return (unit.hp, k)

        return sorted(targets, key=key)[0]

    def targets_for(self, who):
        return [
            pos
            for pos, ent in self.g.items()
            if ent.is_attacker() and ent.kind != who.kind
        ]

    def in_range_of(self, targets):
        return {n for pos in targets for n in self.open_neighbors(pos)}

    def _dist_prev(self, start, target=None):
        dists, prev = {}, {}
        todo, seen = set(), set()

        todo.add(start)
        dists[start] = 0

        while todo:
            _, pos = min((dists[item], item) for item in todo if item in dists)
            todo.remove(pos)
            seen.add(pos)

            if target and target == pos:
                break

            for v in [n for n in self.open_neighbors(pos) if n not in seen]:
                todo.add(v)

                alt = dists[pos] + 1
                if alt < dists.get(v, math.inf):
                    dists[v] = alt
                    prev[v] = pos

        return dists, prev

    def distances_from(self, pos):
        dists, _ = self._dist_prev(pos)
        return dists

    def step_toward(self, start, end):
        _, prev = self._dist_prev(start, end)
        assert end in prev and end != start

        path = []

        cur = end
        while cur != start:
            path.append(cur)
            cur = prev[cur]

        return path[-1]

    def neighbors(self, pos):
        r, c = pos
        ret = []
        for r2, c2 in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
            if (r2, c2) not in self.g:
                continue

            ret.append((r2, c2))

        return sorted(ret)

    def open_neighbors(self, pos):
        return [n for n in self.neighbors(pos) if self.g[n].is_open()]


if __name__ == "__main__":
    main()
