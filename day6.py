#!python

import re
import string
from collections import defaultdict

coords = []
with open('d6.txt') as f:
    for line in f.readlines():
        line = line.strip()
        m = re.match(r'(\d+), (\d+)', line)
        t = ( int(m.group(1)), int(m.group(2)) )
        coords.append(t)

max_x = 0
max_y = 0
for (x, y) in coords:
    if x > max_x:
        max_x = x
    if y > max_y:
        max_y = y

grid = [['?' for x in range(max_x+1)] for y in range(max_y+1)]

THRESHOLD = 10000
good_points = 0

for y in range(max_y+1):
    for x in range(max_x+1):
        least_dist = None
        least_coord = None
        total_coords = 0

        for (i, coord) in enumerate(coords):
            (x_coord, y_coord) = coord
            # for every coordinate, calculate taxicab distance
            dist = abs(x_coord - x) + abs(y_coord - y)
            total_coords += dist
            # print("  {} = {}".format(coord, dist))

            # minimum wins, but if there are two, it's a neutral
            if least_dist is None or dist < least_dist:
                least_dist = dist
                least_coord = coord
            elif least_dist == dist:
                least_dist == -1
                least_coord = None

            # print("{}: checking {}, dist is {} (least: {})".format((x,y), (x_coord, y_coord), dist, least))

        # print("  LEAST: {} (dist={})".format(least_coord, least_dist))
        if total_coords < THRESHOLD:
            good_points += 1
        if least_dist == -1:
            grid[y][x] = '.'
        else:
            grid[y][x] = least_coord

# discard everything on an edge
infinite = set()
# first row
for elem in grid[0]:
    infinite.add(elem)

# last row
for elem in grid[-1]:
    infinite.add(elem)

for (i, row) in enumerate(grid):
    infinite.add(row[0])    # first column
    infinite.add(row[-1])   # last column
# for x in range(max_x):
#     for y in range(max_y):
#         if x == 0 or y == 0 or x == max_x or y == max_y:
#             print("adding point at {} to infinite, coord={}".format((x,y), grid[x][y]))
#             infinite.add(grid[x][y])


# count.

counts = defaultdict(int)
for row in grid:
    for elem in row:
        if elem is not None and elem not in infinite:
            counts[elem] += 1


greatest = (0, 0)
for k, v in counts.items():
    # print("{}: {}".format(k, v))
    if v > greatest[1]:
        greatest = (k, v)

print("greatest: {}: {}".format(*greatest))
print("total safe points: {}".format(good_points))

def print_grid():
    letters = {}
    for pair in zip(coords, string.ascii_lowercase):
        letters[pair[0]] = pair[1]
    for row in grid:
        for elem in row:
            try:
                print(letters[elem], end='')
            except KeyError:
                print('.', end='')
        print('')
