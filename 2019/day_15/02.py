import intcode
import time
import random


#programState = intcode.load_file_into_memory('input15.txt')
#programState['haltFor'] = ['INPUT', 'OUTPUT']

tiles = {
        0: '#', # Wall
        1: ' ', # Empty Space
        2: 'O', # Oxygen
        3: 'D', # Droid
        }

state = {
        'minX' : -5,
        'minY' : -5,
        'maxX' : 5,
        'maxY' : 5,
        'droidX': 0,
        'droidY': 0,
        'mv' : 0,
        }

queue = []
queue.append('-1,0')
queue.append('1,0')
queue.append('0,1')
queue.append('0,-1')

visited = set()
visited.add('0,0')

nodes = {
            '-1,0' : '0,0',
            '1,0'  : '0,0',
            '0,1'  : '0,0',
            '0,-1' : '0,0',
        }

route = []


def print_state (state):

    output = ''

    for y in range(state['minY']-1, state['maxY'] + 2):
        for x in range(state['minX']-1, state['maxX'] + 2):

            if state['droidX'] == x and state['droidY'] == y:
                output += 'D'
            elif x == 0 and y == 0:
                output += 'S'
            else:
                key = "{},{}".format(x,y)
                if key in state:
                    output += state[key]
                else:
                    output += '?'
        output += '\n'

    print (output)


def key_to_coords(key):
    return [int(key.split(',')[0]), int(key.split(',')[1])]


def movement_to_coords (mv, startCoord):
    if mv == 1: #NORTH
        return [startCoord[0], startCoord[1] + 1]
    elif mv == 2: #SOUTH
        return [startCoord[0], startCoord[1] - 1]
    elif mv == 3: #WEST
        return [startCoord[0] - 1, startCoord[1]]
    elif mv == 4: #EAST
        return [startCoord[0] + 1, startCoord[1]]

    return startCoord


def update_state(statusCode, state = state, tiles = tiles):

    status = tiles[statusCode]
    key = movement_to_coords(state['mv'], [state['droidX'], state['droidY']])

    state["{},{}".format(key[0], key[1])] = status

    if key[0] < state['minX']: state['minX'] = key[0]
    if key[0] > state['maxX']: state['maxX'] = key[0]
    if key[1] < state['minY']: state['minY'] = key[1]
    if key[1] > state['maxY']: state['maxY'] = key[1]

    if status != '#':
        state['droidX'] = key[0]
        state['droidY'] = key[1]

    if status == 'O':
        state['oxy'] = "{},{}".format(key[0], key[1])

    return state


def get_valid_movements(state):

    movements = []

    for m in range(1, 5):
        key = movement_to_coords(m, [state['droidX'], state['droidY']])
        key = "{},{}".format(key[0], key[1])
        if key in state and state[key] != '#':
            movements.append(m)
        elif key not in state:
            movements.append(m)

    return movements


def get_valid_preferred_movements(state):

    movements = []

    for m in range(1, 5):
        key = movement_to_coords(m, [state['droidX'], state['droidY']])
        key = "{},{}".format(key[0], key[1])
        if key not in state:
            movements.append(m)

    if len(movements) == 0:
        return get_valid_movements(state)

    return movements


def get_node_children (coord, visited):

    children = []

    for c in [[coord[0] - 1, coord[1]], [coord[0], coord[1] + 1], [coord[0] + 1, coord[1]], [coord[0], coord[1] - 1]]:
        if "{},{}".format(c[0], c[1]) not in visited:
            children.append(c)

    return children



def calc_coords_to_target (nodes, target):
    coords = []
    coords.append(target)
    if target in nodes:
        coords = (calc_coords_to_target(nodes, nodes[target])) + coords
    return coords

def calc_route_to_target (nodes, target):
    coords = calc_coords_to_target(nodes, target)
    route = []
    prevCoord = key_to_coords(coords[0])
    for coord in coords[1:]:
        coord = key_to_coords(coord)
        if prevCoord[0] > coord[0]: route.append(3) # West
        elif prevCoord[0] < coord[0]: route.append(4) # East
        elif prevCoord[1] < coord[1]: route.append(1) # North
        elif prevCoord[1] > coord[1]: route.append(2) # South
        prevCoord = coord
    return route

def update_queues (target, state):

    global visited
    global queue
    global nodes

    visited.add(target)

    if target in state:
        if state[target] != '#':
            children = get_node_children(key_to_coords(target), visited)
            for child in children:
                ck = "{},{}".format(child[0], child[1])
                queue.append(ck)
                nodes[ck] = target
    else:
       print('{} not in state'.format(target))

    return -1

def count_spaces (state):
    count = 0
    for k,v in state.items():
        if v == ' ':
            count += 1
    return count

def spread_oxygen (state):

    spreadTo = {}

    for k,v in state.items():
        if v == 'O':
            coord = key_to_coords(k)
            for c in [[coord[0] - 1, coord[1]], [coord[0], coord[1] + 1], [coord[0] + 1, coord[1]], [coord[0], coord[1] - 1]]:
                n = "{},{}".format(c[0], c[1])
                if n in state and state[n] == ' ':
                    spreadTo[n] = 'O'

    for k,v in spreadTo.items():
        state[k] = v

    return state

print_state(state)
while len(queue) > 0:

    state['droidX'] = 0
    state['droidY'] = 0
    state['mv'] = 0

    target = queue.pop(0)
    rt = calc_route_to_target (nodes, target)

    programState = intcode.load_file_into_memory('input15.txt')
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

        if programState['haltState'] == 'PAUSE_INPUT' and len(rt) > 0:
            programState['haltState'] = 'RUNNING'
            state['mv'] = rt.pop(0)
            programState['inIo'].append(state['mv'])

    update_queues(target, state)
    print_state(state)

print_state(state)
oxyRoute = calc_route_to_target(nodes, state['oxy'])

print ('Steps to oxygen: ', len(oxyRoute))

counter = 0
while count_spaces(state) > 0:
    state = spread_oxygen(state)
    print_state(state)
    counter += 1


print ('Time to fill with oxygen: ', counter)


