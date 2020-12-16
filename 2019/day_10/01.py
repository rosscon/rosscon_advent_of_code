import math

def parse_asteroids(lines):

    asteroids = []

    for y in range(len(lines)):

        line = lines[y]

        for x in range(len(line)):
            if lines[y][x] == '#':
                asteroids.append({'x': x, 'y': y})

    return asteroids


def solve_ratio(x, y):
    numbers = [x, y]
    gcd = math.gcd(x, y)
    solved = [int(i/gcd) for i in numbers]
    return solved


def find_ratios_for_asteroid(baseAsteroid, asteroids):

    ratios = {}
    for targetAsteroid in asteroids:
        dx = baseAsteroid['x'] - targetAsteroid['x']
        dy = baseAsteroid['y'] - targetAsteroid['y']

        if dx == 0 and dy == 0:
            continue;

        ratio = str(solve_ratio(dx, dy))

        if ratio not in ratios:
            ratios[ratio] = 1
        else:
            ratios[ratio] = ratios[ratio] + 1

    return ratios


def find_asteroid_max_visible(asteroids):
    maxVisible = 0;
    maxAsteroid = {}

    for asteroid in asteroids:
        ratios = find_ratios_for_asteroid(asteroid, asteroids)
        if len(ratios) > maxVisible:
            maxVisible = len(ratios)
            maxAsteroid = { 'asteroid' : asteroid, 'visible': len(ratios) }

    return maxAsteroid


_fileName = "input10.txt"

infile = open(_fileName, 'r')
lines = [line for line in infile.readlines()]

asteroids = parse_asteroids(lines)
bestAsteroid  = find_asteroid_max_visible(asteroids)

print ('Best Asteroid: ', bestAsteroid)