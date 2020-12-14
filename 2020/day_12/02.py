_fileName="input12.txt"


#Parse input file
infile = open(_fileName, 'r')
rows = [line for line in infile.readlines()]

_waypointMovements = {
        'N' : { 'x': 0, 'y':1, 'r':0, },    #Move waypoint North
        'E' : { 'x': 1, 'y':0, 'r':0, },    #Move waypoint East
        'S' : { 'x': 0, 'y':-1, 'r':0, },   #Move waypoint South
        'W' : { 'x': -1, 'y':0, 'r':0, },   #Move waypoint West
        'L' : { 'x': 0, 'y':0, 'r':1, },   #Rotate waypoint left (anti-clockwise)
        'R' : { 'x': 0, 'y':0, 'r':-1, },    #Rotate waypoint right (clockwise)
        }

_shipMovements = {
        'F' : { 'x': 1, 'y':1 },      #Move ship towards waypoint
        'B' : { 'x': -1, 'y':-1 }     #Move ship away from waypoint
        }

_rotations = {
        0:   { 'x': { 'x': 1, 'y': 0 }, 'y': { 'x': 0, 'y': 1 }},
        90:  { 'x': { 'x': 0, 'y': -1 }, 'y': { 'x': 1, 'y': 0 }},
        180: { 'x': { 'x': -1, 'y': 0 }, 'y': { 'x': 0, 'y': -1 }},
        270: { 'x': { 'x': 0, 'y': 1 }, 'y': { 'x': -1, 'y': 0 }}
        }


def parse_input_to_instructions(lines):
    instructions = []

    for line in lines:
        instruction = {'direction':line[0], 'distance':int(line[1:-1])}
        instructions.append(instruction)

    return instructions


def move_waypoint(waypointState, moveInstruction):

    if moveInstruction['direction'] in _waypointMovements:
        direction = _waypointMovements[moveInstruction['direction']]

        #Cardinal move waypoint
        waypointState['x'] += (direction['x'] * moveInstruction['distance'])
        waypointState['y'] += (direction['y'] * moveInstruction['distance'])

        #Rotate waypoint
        rotateAngle = (360 + ( moveInstruction['distance'] * direction['r'] )) % 360
        rotation = _rotations[rotateAngle]

        tmpX = \
            (rotation['x']['x'] * waypointState['x']) + \
            (rotation['x']['y'] * waypointState['y'])

        tmpY =  \
            (rotation['y']['x'] * waypointState['x']) + \
            (rotation['y']['y'] * waypointState['y'])

        waypointState['x'] = tmpX
        waypointState['y'] = tmpY

    return waypointState


def move_ship(shipState, waypointState, moveInstruction = {'x': 0, 'y':0, 'r':0, 'f':0 }):

    if moveInstruction['direction'] in _shipMovements:
        direction = _shipMovements[moveInstruction['direction']]

        shipState['x'] += (waypointState['x'] * moveInstruction['distance'] * direction['x'])
        shipState['y'] += (waypointState['y'] * moveInstruction['distance'] * direction['x'])

    return shipState


shipState = { 'x': 0, 'y': 0 }
waypointState = { 'x':10, 'y': 1 }

instructions = parse_input_to_instructions(rows)

for instruction in instructions:
    waypointState = move_waypoint(waypointState, instruction)
    shipState = move_ship(shipState, waypointState, instruction)
    print('Instruction: ', instruction, '\nShip: ', shipState, '\nWaypoint: ', waypointState, '\n')

answer = abs(shipState['x']) + abs(shipState['y'])
print ('Answer: ', answer)


