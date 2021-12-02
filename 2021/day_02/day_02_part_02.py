fileName = "input.txt"

infile = open(fileName, 'r')
instructions = [line.strip().split(' ') for line in infile.readlines()]
instructions = [(instruction[0], int(instruction[1])) for instruction in instructions]

position = [0, 0]
aim = 0

for direction, magnitude in instructions:

    if direction == 'up':
        aim = aim - magnitude
    elif direction == 'down':
        aim = aim + magnitude
    elif direction == 'forward':
        position[0] = position[0] + magnitude
        position[1] = position[1] + (magnitude * aim)


print(position)
print(position[0] * position[1])



