import intcode
import copy


def print_state(state, xp, yp):

    output = ""

    for y in range(yp):
        for x in range (xp):
            if (x, y) in state:
                if state[(x, y)] :
                    output += '#'
                else:
                    output += ' '
            else:
                output += '?'
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


def count_affected_coords ( state, xp, yp ):
    total = 0

    for y in range(yp):
        for x in range (xp):
            if (x, y) in state:
                if state[(x, y)] :
                    total += 1
    return total


state = {}

programState = intcode.load_file_into_memory('input19.txt')

for y in range(50):
    for x in range(50):
        state[(x, y)] = test_coord ( (x, y), copy.deepcopy(programState) )

print_state( state, 50, 50 )
affected = count_affected_coords( state, 50, 50 )
print ("Affected points: ", affected)