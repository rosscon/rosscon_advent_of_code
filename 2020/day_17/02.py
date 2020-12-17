
# Common function for converting coordinate to key
def coordinate_to_key (x, y, z, w):
    return "{},{},{},{}".format(x, y, z, w)

# Converts a key back into x,y,z coordinates
def key_to_coordinate (key):
    x = int(key.split(',')[0])
    y = int(key.split(',')[1])
    z = int(key.split(',')[2])
    w = int(key.split(',')[3])
    return { 'x': x, 'y': y, 'z': z, 'w': w }


# gets the status of a given cube, if it hasnt been created et creates it
def get_status_of_cube (x, y, z, w, state, default = '.'):
    key = coordinate_to_key(x, y, z, w)

    if key in state:
        return state[key]

    return default


# Calculates the neightbouring coordinates for a given coordinate
def get_neighbouring_coordinates (x, y, z, w):
    coordinates = []
    for nx in range(x - 1, x + 2):
        for ny in range (y - 1, y + 2):
            for nz in range (z - 1, z + 2):
                for nw in range (w - 1, w + 2):
                    if not (x == nx and y == ny and z == nz and nw == w):
                        coordinates.append(coordinate_to_key(nx, ny, nz, nw))
    return coordinates

# Calculates the minimum and maximum x,y,z values
def get_min_max_coordinates(state, activeState = '#'):

    minCoord = { 'x': 0, 'y': 0, 'z': 0, 'w': 0}
    maxCoord = { 'x': 0, 'y': 0, 'z': 0, 'w': 0 }

    for key, value in state.items():

        coordinate = key_to_coordinate(key)

        if coordinate['x'] < minCoord['x']:
            minCoord['x'] = coordinate['x']
        elif coordinate['x'] > maxCoord['x']:
            maxCoord['x'] = coordinate['x']

        if coordinate['y'] < minCoord['y']:
            minCoord['y'] = coordinate['y']
        elif coordinate['y'] > maxCoord['y']:
            maxCoord['y'] = coordinate['y']

        if coordinate['z'] < minCoord['z']:
            minCoord['z'] = coordinate['z']
        elif coordinate['z'] > maxCoord['z']:
            maxCoord['z'] = coordinate['z']

        if coordinate['w'] < minCoord['w']:
            minCoord['w'] = coordinate['w']
        elif coordinate['w'] > maxCoord['w']:
            maxCoord['w'] = coordinate['w']

    return { 'min': minCoord, 'max': maxCoord }


# Parse the input file
def parse_input(rows):
    newState = {}

    for y in range(len(rows)):
        for x in range(len(rows[y])):
            key = coordinate_to_key(x, y, 0, 0)
            newState[key] = rows[y][x]

    return newState


# Count how many active cubes exist in a list
def count_active_in_list(cubes, state, activeState = '#', inactiveState = '.'):
    count = 0

    for c in cubes:
        coord = key_to_coordinate(c)
        status = get_status_of_cube(coord['x'], coord['y'], coord['z'], coord['w'], state, default = inactiveState )
        if status == activeState:
            count += 1

    return count


# Returns the state of the next iteration
def iterate_state(state, activeState = '#', inactiveState = '.', buffer = 1):
    newState = {}

    minMax = get_min_max_coordinates(state)

    for x in range ((minMax['min']['x']) - buffer, (minMax['max']['x'] + buffer + 1)):
        for y in range ((minMax['min']['y']) - buffer, (minMax['max']['y'] + buffer + 1)):
            for z in range ((minMax['min']['z']) - buffer, (minMax['max']['z'] + buffer + 1)):
                for w in range ((minMax['min']['w']) - buffer, (minMax['max']['w'] + buffer + 1)):
                    currentCubeState = get_status_of_cube(x, y, z, w, state)

                    neighbours = get_neighbouring_coordinates(x, y, z, w)
                    nCount = count_active_in_list(neighbours, state)

                    key = coordinate_to_key(x, y, z, w)

                    if currentCubeState == inactiveState and nCount == 3:
                        newState [key] = activeState
                    elif currentCubeState == activeState and (nCount == 2 or nCount == 3):
                        newState [key] = activeState

    return newState

# Useful for debugging
def print_state(state):
    minMax = get_min_max_coordinates(state)

    for w in range (minMax['min']['w'], (minMax['max']['w'] + 1)):
        for z in range (minMax['min']['z'], (minMax['max']['z'] + 1)):
            print ('z: {}\tw:{}'.format(z, w))

            for y in range (minMax['min']['y'], (minMax['max']['y'] + 1)):
                for x in range (minMax['min']['x'], (minMax['max']['x'] + 1)):
                    print(get_status_of_cube(x, y, z, w, state), end = '')
                print('\n')
            print()


_fileName = "input17.txt"

#Parse input file
infile = open(_fileName, 'r')
rows = [line.rstrip() for line in infile.readlines()]


currentState = parse_input(rows)

print('---')
print_state(currentState)

for i in range (6):
    currentState = iterate_state(currentState)

#print('--------------')
#print_state(currentState)

activeCubeCount = count_active_in_list(currentState.keys(), currentState)

print("Active cubes: ", activeCubeCount)