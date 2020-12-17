import math

def parse_moons(lines):
    moons = []
    for line in lines:
        line = line[1:-1]
        splitLine = line.split(', ')
        moon = {'dx': 0, 'dy': 0, 'dz': 0}
        for p in splitLine:
            moon[p.split('=')[0]] = int(p.split('=')[1])
        moons.append(moon)
    return moons


def update_velocities(moons, dimensions = ['x', 'y', 'z']):

    for i in range(len(moons)):
        for j in range(len(moons)):
            if i != j:
                for d in dimensions:
                    if moons[i][d] == moons[j][d]:
                        moons[i]['d'+d] = moons[i]['d'+d]
                    elif moons[i][d] < moons[j][d]:
                        moons[i]['d'+d] += 1
                    elif moons[i][d] > moons[j][d]:
                        moons[i]['d'+d] -= 1
    return moons


def update_positions(moons, dimensions = ['x', 'y', 'z']):
    for moon in moons:
        for d in dimensions:
            moon[d] += moon['d' + d]
    return moons

def update_potential_energy(moons):

    for moon in moons:
        total = 0
        for d in ['x', 'y', 'z']:
            total += abs(moon[d])
        moon['pe'] = total
    return moons

def update_kinetic_energy(moons):

    for moon in moons:
        total = 0
        for d in ['dx', 'dy', 'dz']:
            total += abs(moon[d])
        moon['ke'] = total
    return moons

def update_total_energy(moons):

    for moon in moons:
        moon['te'] = moon['pe'] * moon['ke']
    return moons

def dimension_matches(moons, initialMoons, dimension):

    for i in range(len(moons)):
        for k in [dimension, 'd' + dimension]:
            if moons[i][k] != initialMoons[i][k]:
                return False

    return True

def lcm(a, b):
        return a * b // math.gcd(a, b)


fileName = "input12.txt"

infile = open(fileName, 'r')
lines = [line.rstrip() for line in infile.readlines()]

moons = parse_moons(lines)
initalMoons = parse_moons(lines)

multiples = []

#Need to find the point at which each dimension returns back to start and find
#lowest common multiple
for d in ['x', 'y', 'z']:
    steps = 0
    moons = parse_moons(lines)
    while steps == 0 or (not dimension_matches(moons, initalMoons, d)):
        moons = update_velocities(moons, [d])
        moons = update_positions(moons, [d])
        steps += 1

    multiples.append(steps)


#Find the lowest common multiple between steps
answer = lcm(lcm(multiples[0], multiples[1]), multiples[2])

print ('Total Steps: ', answer)





