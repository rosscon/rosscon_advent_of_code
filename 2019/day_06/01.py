_fileName="input06.txt"


#Parse input file
infile = open(_fileName, 'r')
rows = [line.rstrip() for line in infile.readlines()]


def parse_input_rows_objects(rows):
    objects = {}

    for row in rows:

        #print(row)

        obj = row.split(')')[0]
        sat = row.split(')')[1]
        #print("obj: ", obj, " sat: ", sat)

        if obj in objects:
            objects[obj]['satellites'].append(sat)
        else:
            objects[obj] = {'name': obj, 'satellites': [sat]}

        if sat in objects:
            objects[sat]['orbits'] = obj
        else:
            objects[sat] = {'name': sat, 'satellites': [], 'orbits': obj}

        #print()

    return objects


def count_direct_orbits(objects, obj):

    count = 1

    for sat in obj['satellites']:
        satellite = objects[sat]
        count += count_direct_orbits(objects, satellite)

    return count

def count_indirect_orbits(objects, obj):
    count = 1

    #print (obj)
    if 'orbits' in obj:
        count += count_indirect_orbits(objects, objects[obj['orbits']])
    else:
        return 0

    return count



#Parse the input into objects in dictionary
objects = parse_input_rows_objects(rows)

#find the root object
rootObjects = {}
leafObjects = []

for k,v in objects.items():
    if not 'orbits' in v:
        rootObjects[k] = v

    if len(v['satellites']) == 0:
        leafObjects.append(v)



totalDirect = count_direct_orbits(objects, rootObjects['COM'])

totalIndirect = 0
for k,v in objects.items():
    totalIndirect += count_indirect_orbits(objects, v) - 1
    #print()

print('Total direct orbits: ', totalDirect)
print('Total indirect orbits: ', totalIndirect)
print('Total orbits: ', totalDirect + totalIndirect)
