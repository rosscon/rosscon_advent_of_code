import math

def parse_line (line):
    reaction = {}

    chemsIn = { x.split(' ')[1] : int(x.split(' ')[0]) for x in line.split(' => ')[0].split(', ')}
    reaction['in'] = chemsIn
    reaction['out'] = line.split(' => ')[1].split(' ')[1]
    reaction['qty'] = int(line.split(' => ')[1].split(' ')[0])

    return reaction


remainders = {}


def recurse_reactions (reaction, reactions, target = 'ORE', required = 1):

    global remainders

    #print (reaction)

    spare = 0
    if reaction['out'] in remainders:
        spare = remainders[reaction['out']]
        if spare >= required:
            remainders[reaction['out']] = (remainders[reaction['out']] - required)
            return 0
        else:
            remainders[reaction['out']] = 0

    tmpRequired = required - spare
    multiple = int(math.floor(tmpRequired / reaction['qty']))

    #multiple = 1
    while (multiple * reaction['qty']) + spare < required:
        multiple += 1

    #print ("required: {}\tmultiple: {}\tspare: {}".format(required, multiple, spare))
    #print()

    if multiple * reaction['qty'] + spare > required:
        remainders[reaction['out']] = (multiple * reaction['qty'] + spare) - required

    if target in reaction['in']:
        return multiple * reaction['in'][target]


    count = 0

    for k,v in reaction['in'].items():
        count += recurse_reactions(reactions[k], reactions, target, (multiple * v))

    return count



fileName = "input14.txt"

infile = open(fileName, 'r')
lines = [line.rstrip() for line in infile.readlines()]


# Parse reactions
reactions = {}
for line in lines:
    parsed = parse_line(line)
    if parsed['out'] in reactions:
        print ('Error output already exists')
    else:
        reactions[parsed['out']] = parsed



targetOre = 1000000000000
#targetOre = 1000
fuel = 0
increment = 1
oreUsed = 0
root = reactions['FUEL']

while oreUsed < targetOre and increment >= 1:
    print (increment)
    tmpOreUsed = recurse_reactions(root, reactions, required = fuel)

    if tmpOreUsed > targetOre:
        fuel -= increment
        increment = int(increment / 2)
    else:
        oreUsed = tmpOreUsed
        increment = increment * 2

    fuel += increment

print ("Potential fuel: ", fuel - 1)