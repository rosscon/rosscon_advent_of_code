import intcode

tiles = {
        35: '#', # Scaffold
        46: ' ', # Empty Space
        60: '<', # Left
        62: '>', # Right
        94: '^', # Up
        76: 'v', # Right
        88: 'X', # Fallen
        10: '\n',# New Line
        }

state = {
        'minX' : 0,
        'minY' : 0,
        'maxX' : 0,
        'maxY' : 0,
        'x': 0, # Current x coord
        'y': 0, # Curreny y coord
        #'ints' : [],# Intersections
        }

def get_surr_coords (coord):
    return [
            [coord[0] , coord[1] -1], # Above
            [coord[0] , coord[1] -1], # Below
            [coord[0] - 1, coord[1]], # Left
            [coord[0] + 1, coord[1]], # Right
            ]

def is_intersection (coord, state):
    key = coord_to_key(coord)
    if state[key] != '#':
            return False

    for c in get_surr_coords(coord):
        key = coord_to_key(c)
        if key not in state:
            return False
        if state[key] != '#':
            return False
    return True


def print_state (state):

    output = ''

    for y in range(state['minY']-1, state['maxY'] + 1):
        for x in range(state['minX']-1, state['maxX'] + 1):

            key = coord_to_key([x, y])
            if key in state:
                if is_intersection([x, y], state):
                    output += 'O'
                else:
                    output += state[key]
            else:
                output += '?'
        output += '\n'

    print (output)


def key_to_coords(key):
    return [int(key.split(',')[0]), int(key.split(',')[1])]

def coord_to_key (coord):
    return "{},{}".format(coord[0], coord[1])


def update_state(statusCode, state = state, tiles = tiles):

    if( statusCode == 10 ):
        state['x'] = 0
        state['y'] += 1

        if state['y'] > state['maxY']:
            state['maxY'] = state['y']

        return state

    if statusCode in tiles:
        state[coord_to_key([state['x'], state['y']])] = tiles[statusCode]
    else:
        state[coord_to_key([state['x'], state['y']])] = "E"

    state['x'] += 1

    if state['x'] > state['maxX']:
        state['maxX'] = state['x']

    return state


def find_intersections (state):

    intersections = []

    for y in range(state['minY'], state['maxY']):
        for x in range(state['minX'], state['maxX']):
            key = coord_to_key([x, y])
            if key in state:
                if is_intersection([x, y], state):
                    intersections.append([x, y])

    return intersections


def calibrate (intersections):
    total = 0

    for i in intersections:
        total += (i[0] * i[1])

    return total


programState = intcode.load_file_into_memory('input17.txt')
programState['haltFor'] = ['INPUT', 'OUTPUT']

while programState['haltState'] == 'RUNNING':

    programState = intcode.execute_interactive(programState)

    if programState['haltState'] == 'HALTED_OUTPUT':
        print ('HALT')
        break

    if programState['haltState'] == 'PAUSE_OUTPUT':
        programState['haltState'] = 'RUNNING'
        if (len(programState['outIo']) == 1):
            update_state(programState['outIo'][0])
            programState['outIo'] = []

    if programState['haltState'] == 'PAUSE_INPUT':
        programState['haltState'] = 'RUNNING'
        break

print_state (state)

intersections = find_intersections(state)
cal = calibrate (intersections)
print ("Sum of alignment params: ", cal)