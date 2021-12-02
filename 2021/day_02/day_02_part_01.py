fileName = "input.txt"

infile = open(fileName, 'r')
instructions = [line.strip().split(' ') for line in infile.readlines()]
instructions = [(instruction[0], int(instruction[1])) for instruction in instructions]

modifiers = {
    'forward': [1, 0],
    'backward': [-1, 0],
    'up': [0, -1],
    'down': [0, 1]
}

position = [0, 0]

for direction, magnitude in instructions:
    modifier = [m * magnitude for m in modifiers[direction]]

    for i in range(len(position)):
        position[i] = position[i] + modifier[i]

print(position)
print(position[0] * position[1])



