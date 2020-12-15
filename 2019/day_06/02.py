_fileName="input06.txt"


#Parse input file
infile = open(_fileName, 'r')
rows = [line.rstrip() for line in infile.readlines()]


def parse_input_rows_objects(rows):
    objects = {}

    for row in rows:

        obj = row.split(')')[0]
        sat = row.split(')')[1]

        if obj in objects:
            objects[obj]['satellites'].append(sat)
        else:
            objects[obj] = {'name': obj, 'satellites': [sat]}

        if sat in objects:
            objects[sat]['orbits'] = obj
        else:
            objects[sat] = {'name': sat, 'satellites': [], 'orbits': obj}


    return objects



def get_chain_to_root(objects, obj):

    chain = [obj['name']]

    if 'orbits' in obj:
        orbits = objects[obj['orbits']]
        chain.extend(get_chain_to_root(objects, orbits))

    return chain




def manouvers_to_target(objects, source, destination):

    sourceChain = get_chain_to_root(objects, source)
    destinationChain = get_chain_to_root(objects, destination)
    #print (sourceChain)
    #print (destinationChain)

    for i in range (0, len(sourceChain)):
        for j in range(0, len(destinationChain)):
            if sourceChain[i] == destinationChain[j]:
                return (i + j - 2)

    return -1



#Parse the input into objects in dictionary
objects = parse_input_rows_objects(rows)

#Source and destination objects
sourceObject = objects['YOU']
destinationObject = objects['SAN']

manouvers = manouvers_to_target (objects, sourceObject, destinationObject)
print ('Orbital manouvers : ', manouvers)