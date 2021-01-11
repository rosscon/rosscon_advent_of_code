import intcode
import time

tiles = {
        35: '#', # Scaffold
        46: ' ', # Empty Space
        60: '<', # Left
        62: '>', # Right
        94: '^', # Up
        118: 'v', # Right
        88: 'X', # Fallen
        #10: '\n',# New Line
        }

state = {
        'minX' : 0,
        'minY' : 0,
        'maxX' : 0,
        'maxY' : 0,
        'x': 0,         # Current x coord
        'y': 0,         # Curreny y coord
        'prev' : "",    # Previous char
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

        if state['prev'] == 10:
            state['y'] = 0

        state['prev'] = statusCode

        return state

    if statusCode in tiles:
        state[coord_to_key([state['x'], state['y']])] = tiles[statusCode]
        state['x'] += 1
    else:
        print (chr(statusCode), end = '')
    #    state[coord_to_key([state['x'], state['y']])] = "E"



    if state['x'] > state['maxX']:
        state['maxX'] = state['x']

    state['prev'] = statusCode

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

"""
breaking down the path
L,12,R,4,R,4,R,12,R,4,L,12,R,12,R,4,L,12,R,12,R,4,L,6,L,8,L,8,R,12,R,4,L,6,L,8,L,8,L,12,R,4,R,4,L,12,R,4,R,4,R,12,R,4,L,12,R,12,R,4,L,12,R,12,R,4,L,6,L,8,L,8

L,12,R,4,R,4
R,12,R,4,L,12
R,12,R,4,L,12

R,12,R,4,L,6,L,8,L,8
R,12,R,4,L,6,L,8,L,8

L,12,R,4,R,4
L,12,R,4,R,4
R,12,R,4,L,12
R,12,R,4,L,12

R,12,R,4,L,6,L,8,L,8"
"""

inputs = [
        "A,B,B,C,C,A,A,B,B,C",  # Main routine
        "L,12,R,4,R,4",         # Function A
        "R,12,R,4,L,12",        # Function B
        "R,12,R,4,L,6,L,8,L,8", # Function C
        "n",                    # Video Feed
        ]

programState = intcode.load_file_into_memory('input17.txt')
programState['haltFor'] = ['INPUT', 'OUTPUT']
programState['memory'][0] = 2

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
            if state['y'] == 0 and state['maxY'] > 0:
                print_state (state)
                time.sleep(.017)
                #break

    if programState['haltState'] == 'PAUSE_INPUT':
        programState['haltState'] = 'RUNNING'
        i = inputs.pop(0)
        for c in i:
            programState['inIo'].append(ord(c))
        programState['inIo'].append(10)
        print()
        #break

print_state (state)

intersections = find_intersections(state)
cal = calibrate (intersections)
print ("Sum of alignment params: ", cal)

print ("Total Dust: ", state['prev'])