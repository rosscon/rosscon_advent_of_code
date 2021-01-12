import intcode
import copy


def print_state( state, ship ):

    output = ""

    for y in range(state['maxY']):
        for x in range (state['maxX']):

            if y >= ship['y'] and y < (ship['y'] + ship['height']) and x >= ship['x'] and x < (ship['x'] + ship['width']):
                output += 'O'
            else:
                if (x, y) in state:
                    if state[(x, y)] :
                        output += '#'
                    else:
                        output += '.'
                else:
                    output += ' '
        output += '\n'

    print (output)


def test_coord ( coord, programState ):

    x, y = coord


    programState['haltFor'] = ['INPUT', 'OUTPUT']
    programState['inIo'] = [x, y]

    programState = intcode.execute_interactive(programState)

    if programState['haltState'] == 'PAUSE_OUTPUT':
        programState['haltState'] = 'RUNNING'
        if (len(programState['outIo']) == 1):
            return programState['outIo'][0]

    return -1


def count_affected_coords ( state ):
    total = 0

    for y in range(state['maxY']):
        for x in range (state['maxX']):
            if (x, y) in state:
                if state[(x, y)] :
                    total += 1
    return total


# Determines whether a given rectangle is housed entirely within the
# tractor beam
def in_tractor_beam ( state, ship ):

    #Only need to check corners are in beam
    for y in [ship['y'], ship['y'] + ship['height'] - 1]:
        for x in [ship['x'], ship['x'] + ship['width'] - 1]:
            if (x, y) not in state:
                return False

            if state[(x, y)] == 0:
                return False

    return True


# Determines whether a rectangle of a given size can fit within the
# tractor beam
def can_fit_shape ( state, ship ):

    for y in range (state['maxY']):
        for x in range (state ['maxX']):
            ship['x'] = x
            ship['y'] = y

            if in_tractor_beam ( state, ship ):
                return ship

    return False



state = { 'maxX':0 , 'maxY':0 }
ship = { 'x' : 0, 'y': 0, 'width': 100, 'height': 100 }

programState = intcode.load_file_into_memory('input19.txt')

lastMaxX = 0

# Get an initial small state for the drone to work from
for y in range(10):
    for x in range(10):
        state[(x, y)] = test_coord ( (x, y), copy.deepcopy(programState) )

        if state[(x, y)]:
            if x > lastMaxX:
                lastMaxX = x
        if state['maxX'] < x : state['maxX'] = x
    if state['maxY'] < y : state['maxY'] = y





# Use max x value to determine where to move drone from, no point
# checking areas that will be outside the beam
found = False
while True:

    # Go right until hit an unaffected location
    inBeam = True
    x = lastMaxX

    # Follow the right edge
    while inBeam:
        state[(x, y)] = test_coord ( (x, y), copy.deepcopy(programState) )
        if state[(x, y)] == 0:
            inBeam = False
        else:
           lastMaxX = x
        x += 1
        if state['maxX'] < x : state['maxX'] = x

    x = lastMaxX
    # Check if ship corners are in beam, only need to check top right and bottom left
    if x > ship['width']:
        sx = x - ship['width'] + 1
        sy = y + ship['height'] - 1
        state[(sx, sy)] = test_coord ( (sx, sy), copy.deepcopy(programState) )
        if state[(sx, sy)] == 1:
            ship['y'] = y
            ship['x'] = x - ship['width'] + 1
            found = True
            break


    # Go left until hit an unaffected location
    """inBeam = True
    x = lastMaxX
    while inBeam and x >= 0:
        state[(x, y)] = test_coord ( (x, y), copy.deepcopy(programState) )
        if not state[(x, y)]:
            inBeam = False
        x -= 1"""

    y += 1
    if state['maxY'] < y + ship['height'] : state['maxY'] = y + ship['height']

#print_state( state, ship )

print ("Ship Location: ({},{})".format(ship['x'], ship['y']))
answer = (ship['x'] * 10000) + ship['y']
print ("Answer: ", answer)
