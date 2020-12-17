import intcode

# Common function for converting coordinate to key
def coordinate_to_key (x, y):
    return "{},{}".format(x, y)


# Converts a key back into x,y,z coordinates
def key_to_coordinate (key):
    x = int(key.split(',')[0])
    y = int(key.split(',')[1])
    return { 'x': x, 'y': y}


# Gets the state of the panel the robot is currently on
def get_panel_state (paintState, robotState, default = '.'):

    if robotState['location'] in paintState:
        return paintState[robotState['location']]

    return default



def paint_panel (paintState, robotState, color):
    paintState[robotState['location']] = color
    return paintState



def rotate_robot (robotState, direction):

    if direction == 0: # 0 for left 90
        if robotState['facing'] == 'N':
            robotState['facing'] = 'W'
        elif robotState['facing'] == 'W':
            robotState['facing'] = 'S'
        elif robotState['facing'] == 'S':
            robotState['facing'] = 'E'
        elif robotState['facing'] == 'E':
            robotState['facing'] = 'N'

    elif direction == 1: # 0 for right 90
        if robotState['facing'] == 'N':
            robotState['facing'] = 'E'
        elif robotState['facing'] == 'E':
            robotState['facing'] = 'S'
        elif robotState['facing'] == 'S':
            robotState['facing'] = 'W'
        elif robotState['facing'] == 'W':
            robotState['facing'] = 'N'

    return robotState



def move_robot (robotState):

    robotCoordinate = key_to_coordinate(robotState['location'])

    if robotState['facing'] == 'N':
        robotCoordinate['y'] += -1
    elif robotState['facing'] == 'S':
        robotCoordinate['y'] += 1
    elif robotState['facing'] == 'E':
        robotCoordinate['x'] += 1
    elif robotState['facing'] == 'W':
        robotCoordinate['x'] += -1

    robotLocation = coordinate_to_key(robotCoordinate['x'], robotCoordinate['y'])
    robotState['location'] = robotLocation
    return robotState


# Calculates the minimum and maximum x,y,z values
def get_min_max_coordinates(paintState):

    minCoord = { 'x': 0, 'y': 0}
    maxCoord = { 'x': 0, 'y': 0}

    for key, value in paintState.items():

        coordinate = key_to_coordinate(key)

        if coordinate['x'] < minCoord['x']:
            minCoord['x'] = coordinate['x']
        elif coordinate['x'] > maxCoord['x']:
            maxCoord['x'] = coordinate['x']

        if coordinate['y'] < minCoord['y']:
            minCoord['y'] = coordinate['y']
        elif coordinate['y'] > maxCoord['y']:
            maxCoord['y'] = coordinate['y']

    return { 'min': minCoord, 'max': maxCoord }

def print_paint_state(paintState, robotState):

    minMax = get_min_max_coordinates(paintState)

    for y in range (minMax['min']['y']-1, (minMax['max']['y'] + 2)):
        for x in range (minMax['min']['x']-1, (minMax['max']['x'] + 2)):
            if coordinate_to_key (x, y) != robotState['location']:
                print(get_panel_state(paintState, {'location': coordinate_to_key (x, y)}), end = '')
            else:
                if robotState['facing'] == 'N': print('^', end = '')
                if robotState['facing'] == 'E': print('>', end = '')
                if robotState['facing'] == 'S': print('v', end = '')
                if robotState['facing'] == 'W': print('<', end = '')
        print('\n')
    print()






paintState={'0,0': '.'}
robotState={'location': '0,0', 'facing': 'N'}

programState = intcode.load_file_into_memory('input11.txt')
programState['inIo'].append(0)
programState['dbgOut'] = True
colors = ['.','#']

visited = {}

i = 0
runs = 10

print_paint_state(paintState, robotState)

while programState['haltState'] == 'RUNNING':

    programState = intcode.execute_interactive(programState)
    if programState['haltState'] == 'HALTED':
        #print (programState)
        print ('HALT 1')
        break

    programState['haltState'] = 'RUNNING'
    programState = intcode.execute_interactive(programState)
    if programState['haltState'] == 'HALTED':
        #print ('HALT 2')
        break

    outputs = programState['outIo']
    programState['outIo'] = []

    paintState = paint_panel(paintState, robotState, colors[outputs[0]])
    robotState = rotate_robot(robotState, outputs[1])
    robotState = move_robot(robotState)

    panelState = get_panel_state(paintState, robotState)
    print(panelState, end = '')
    panelState = colors.index(panelState)
    print(panelState)

    if robotState['location'] in visited:
        visited[robotState['location']] += 1
    else:
        visited[robotState['location']] = 1

    programState['inIo'].append(panelState)
    programState['haltState'] = 'RUNNING'


print_paint_state(paintState, robotState)
