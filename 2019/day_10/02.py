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
        ratio = math.atan2(dx, dy) * -1
        ratio = (math.degrees(ratio) + 360) % 360

        if ratio not in ratios:
            ratios[ratio] = [targetAsteroid]
        else:
            ratios[ratio].append(targetAsteroid)

    return ratios


def find_asteroid_max_visible(asteroids):
    maxVisible = 0;
    maxAsteroid = {}

    for asteroid in asteroids:
        ratios = find_ratios_for_asteroid(asteroid, asteroids)
        if len(ratios) > maxVisible:
            maxVisible = len(ratios)
            maxAsteroid = { 'asteroid' : asteroid, 'visible': len(ratios), 'asteroids': ratios }

    return maxAsteroid


def find_nearest_asteroid_index(base, asteroids):

    nearestDistance = -1
    nearestIndex = 0

    for i in range(len(asteroids)):
        dx = base['x'] - asteroids[i]['x']
        dy = base['y'] - asteroids[i]['y']

        dist = math.sqrt(pow(dx, 2) + pow(dy, 2))
        #print('dist: ', dist)

        if dist < nearestDistance or nearestDistance == -1:
            nearestDistance = dist
            nearestIndex = i

    return nearestIndex


def vaporisation_laser(bestAsteroid, stop = -1):

    countVaporised = 0
    vaporisedAsteroids = []

    while len(bestAsteroid['asteroids']) > 0 and (countVaporised < stop or stop == -1):

        removeKeys = []

        for angle in sorted(bestAsteroid['asteroids'].keys()):

            print('angle: ', angle)

            if len(bestAsteroid['asteroids'][angle]) > 1:
                nearestIndex = find_nearest_asteroid_index(bestAsteroid['asteroid'], bestAsteroid['asteroids'][angle])
                vaporisedAsteroids.append(bestAsteroid['asteroids'][angle][nearestIndex])
                del bestAsteroid['asteroids'][angle][nearestIndex]
            else:
                vaporisedAsteroids.append(bestAsteroid['asteroids'][angle][0])
                removeKeys.append(angle)

            countVaporised += 1

        [bestAsteroid['asteroids'].pop(x) for x in removeKeys]
        print()

    return vaporisedAsteroids


_fileName = "input10.txt"

infile = open(_fileName, 'r')
lines = [line for line in infile.readlines()]

asteroids = parse_asteroids(lines)
bestAsteroid  = find_asteroid_max_visible(asteroids)

print ('Best Asteroid: ', bestAsteroid['asteroid'])
print ()
vaporisedAsteroids = vaporisation_laser(bestAsteroid)

targetAsteroid = vaporisedAsteroids[199]

answer = (targetAsteroid['x'] * 100) + targetAsteroid['y']

print ('Answer: ', answer)


