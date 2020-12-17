
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


def update_velocities(moons):

    for i in range(len(moons)):
        for j in range(len(moons)):
            if i != j:
                for d in ['x', 'y', 'z']:
                    if moons[i][d] == moons[j][d]:
                        moons[i]['d'+d] = moons[i]['d'+d]
                    elif moons[i][d] < moons[j][d]:
                        moons[i]['d'+d] += 1
                    elif moons[i][d] > moons[j][d]:
                        moons[i]['d'+d] -= 1
    return moons


def update_positions(moons):
    for moon in moons:
        for d in ['x', 'y', 'z']:
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


fileName = "input12.txt"

infile = open(fileName, 'r')
lines = [line.rstrip() for line in infile.readlines()]

moons = parse_moons(lines)

for i in range(1000):
    moons = update_velocities(moons)
    moons = update_positions(moons)
    moons = update_potential_energy(moons)
    moons = update_kinetic_energy(moons)
    moons = update_total_energy(moons)

totalEnergy = 0
for moon in moons:
    totalEnergy += moon['te']


print ('Total Energy: ', totalEnergy)





