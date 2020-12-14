_fileName="input12.txt"


#Parse input file
infile = open(_fileName, 'r')
rows = [line for line in infile.readlines()]

_directions = {
        'N' : { 'x': 0, 'y':1, 'r':0, 'f':0 },    #Move ship North
        'E' : { 'x': 1, 'y':0, 'r':0, 'f':0 },    #Move ship East
        'S' : { 'x': 0, 'y':-1, 'r':0, 'f':0 },   #Move ship South
        'W' : { 'x': -1, 'y':0, 'r':0, 'f':0 },   #Move ship West
        'L' : { 'x': 0, 'y':0, 'r':-1, 'f':0 },   #Rotate ship left (anti-clockwise)
        'R' : { 'x': 0, 'y':0, 'r':1, 'f':0 },    #Rotate ship right (clockwise)
        'F' : { 'x': 0, 'y':0, 'r':0, 'f':1 }     #Move ship forward facing direction
        }

_rotations = { 0: 'N', 90: 'E', 180: 'S', 270: 'W' }

def parse_input_to_instructions(lines):
    instructions = []

    for line in lines:
        instruction = {'direction':line[0], 'distance':int(line[1:-1])}
        instructions.append(instruction)

    return instructions


def move_ship(shipState, moveInstruction = {'x': 0, 'y':0, 'r':0, 'f':0 }):

    if moveInstruction['direction'] in _directions:
        direction = _directions[moveInstruction['direction']]

        shipState['x'] += (direction['x'] * moveInstruction['distance'])
        shipState['y'] += (direction['y'] * moveInstruction['distance'])
        shipState['r'] += (direction['r'] * moveInstruction['distance'])
        shipState['r'] %= 360

        rotation = _rotations[shipState['r']]
        direction2 = _directions[rotation]
        shipState['x'] += (direction2['x'] * direction['f'] * moveInstruction['distance'])
        shipState['y'] += (direction2['y'] * direction['f'] * moveInstruction['distance'])

    return shipState


shipState = { 'x': 0, 'y': 0, 'r':90 }

instructions = parse_input_to_instructions(rows)

for instruction in instructions:
    print(instruction)
    shipState = move_ship(shipState, instruction)
    print(shipState, '\n')

answer = abs(shipState['x']) + abs(shipState['y'])
print ('Answer: ', answer)


