class Grid:
    def __init__(self, serial):
        self.grid = {
            (x, y): power_level(x, y, serial)
            for x in range(1, 301)
            for y in range(1, 301)
        }

    def square(self, x, y, size) -> int:
        return sum(
            self.grid[(this_x, this_y)]
            for this_x in range(x, x + size)
            for this_y in range(y, y + size)
        )

    def best_at_size(self, size):
        best = 0
        coords = (0, 0)
        for x in range(1, 301-size):
            for y in range(1, 301-size):
                pl = self.square(x, y, size)
                if pl > best:
                    coords = (x, y)
                    best = pl

        return best, coords

    def best(self):
        best = 0
        coords = (0, 0, 0)

        # lol this going up to 20 is just a hack, but works
        for size in range(1, 21):
            print(f"checking size {size}")
            pl, (x, y) = self.best_at_size(size)
            if pl > best:
                coords = (x, y, size)
                best = pl

        return coords


def power_level(x: int, y: int, serial) -> int:
    rack_id = x + 10
    return (((((rack_id * y) + serial) * rack_id) % 1000) // 100) - 5


grid = Grid(7347)

_, (x1, y1) = grid.best_at_size(3)
print(f"part 1: {x1},{y1}")

x2, y2, size = grid.best()
print(f"part 2: {x2},{y2},{size}")
