from dataclasses import dataclass
import math
import re
from typing import Self, Tuple


@dataclass
class Point:
    x: int
    y: int
    vx: int
    vy: int

    @classmethod
    def from_line(cls, line: str) -> Self:
        m = re.match(r"position=<(.*?)> velocity=<(.*?)>", line)
        assert m is not None

        x, y = m.group(1).split(",")
        vx, vy = m.group(2).split(",")

        return cls(*(int(s.strip()) for s in [x, y, vx, vy]))

    def advance(self):
        self.x += self.vx
        self.y += self.vy

    def rewind(self):
        self.x -= self.vx
        self.y -= self.vy


class PointSet:
    def __init__(self, points: list[Point]):
        self.points = points
        self.time = 0

    def advance(self) -> None:
        self.time += 1
        for point in self.points:
            point.advance()

    def rewind(self) -> None:
        self.time -= 1
        for point in self.points:
            point.rewind()

    def minmax_x(self) -> Tuple[int, int]:
        xs = [point.x for point in self.points]
        return min(xs), max(xs)

    def minmax_y(self) -> Tuple[int, int]:
        ys = [point.y for point in self.points]
        return min(ys), max(ys)

    def bounds(self):
        minx, maxx = self.minmax_x()
        miny, maxy = self.minmax_y()
        return (maxx - minx) + (maxy - miny)

    def print(self):
        grid = {(p.x, p.y) for p in self.points}
        min_x, max_x = self.minmax_x()
        min_y, max_y = self.minmax_y()

        for y in range(min_y, max_y + 1):
            line = ["█" if (x, y) in grid else " "
                    for x in range(min_x, max_x + 1)]
            print("".join(line))


lights = None
with open("d10.txt", "r") as f:
    points = []
    for line in f:
        points.append(Point.from_line(line))

    lights = PointSet(points)

mindiff = math.inf

while True:
    lights.advance()
    bounds = lights.bounds()
    if bounds <= mindiff:
        mindiff = bounds
    else:
        lights.rewind()
        lights.print()
        print(f"\npart 2: {lights.time}")
        break
