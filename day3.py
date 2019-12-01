#!python

import re

with open('d3.txt', 'r') as f:
    data = [ l.strip() for l in f.readlines() ]
    matrix = [ [], [] ]
    total = 0

    data = [ '#1 @ 82,901: 26x12' ]

    for d in data:
        m = re.match(r'#(\d+) \@ (\d+),(\d+): (\d+)x(\d+)', d)
        (claim_id, x_start, y_start, width, height) = map(int, m.groups())

        for x in range(x_start, x_start + width):
            for y in range(y_start, y_start + height):
                there = matrix[y][x]
                if there == '1':
                    total += 1
                matrix[y][x] = 'X' if there else '1'
    print(total)

