#
# Parse the puzzle input
#
import sys

fileName = "input.txt"

infile = open(fileName, 'r')
input_data = [line.strip() for line in infile.readlines()]

vent_lines = [[[int(z) for z in y.split(',')] for y in x.split(' -> ')] for x in input_data]


def is_horizontal(c1, c2):
    return c1[1] == c2[1]


def is_vertical(c1, c2):
    return c1[0] == c2[0]


# Process each vent line

grid = {}

for vent_line in vent_lines:

    line_points = []

    if is_horizontal(vent_line[0], vent_line[1]):

        y = vent_line[0][1]
        x1 = min(vent_line[0][0], vent_line[1][0])
        x2 = max(vent_line[0][0], vent_line[1][0])

        for x in range(x1, x2 + 1):
            line_points.append((x, y))

    elif is_vertical(vent_line[0], vent_line[1]):

        x = vent_line[0][0]
        y1 = min(vent_line[0][1], vent_line[1][1])
        y2 = max(vent_line[0][1], vent_line[1][1])

        for y in range(y1, y2 + 1):
            line_points.append((x, y))

    for line_point in line_points:
        if line_point not in grid:
            grid[line_point] = 1
        else:
            grid[line_point] = grid[line_point] + 1

overlaps = [x_key for x_key, x_val in grid.items() if x_val > 1]
print(len(overlaps))


