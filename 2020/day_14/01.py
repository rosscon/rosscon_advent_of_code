_fileName="input14.txt"


#Parse input file
infile = open(_fileName, 'r')
rows = [line.rstrip() for line in infile.readlines()]


def parse_instruction(instruction):

    command = instruction.split(' = ')[0]
    value = instruction.split(' = ')[1]

    if command != 'mask':
        addr = int(command[4: -1])
        command = 'write'

        instruction = {'cmd':'write', 'addr':addr, 'val': int(value)}
        return instruction

    else:
        instruction = {'cmd':command, 'val': value}
        return instruction

    return -1


def convert_dec_bin (value, numBits = 36):

    tmpVal = value
    output = ''

    for i in range(numBits - 1, -1, -1):
        if tmpVal >= pow(2, i):
            tmpVal = tmpVal - pow(2, i)
            output += '1'
        else:
            output += '0'

    return output

def convert_bin_int (bits):

    output = 0

    for i in range (0, len(bits)):
        if bits[i] == '1':
            output = pow(2, i)

    return output


def apply_bitmask (bits, mask):
    output = ''

    if len(bits) != len(mask):
        return 'ERROR'

    for i in range(0, len(mask)):
        if mask[i] == 'X':
            output += bits[i]
        else:
            output += mask[i]

    return output


def exec_write(instruction, mask='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', memory={}):

    binVal = convert_dec_bin(instruction['val'])
    #print(binVal, ' - ', instruction['val'])

    binVal = apply_bitmask(binVal, mask)

    memory[instruction['addr']] = binVal

    return memory


mask = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
memory = {}

for row in rows:
    instruction = parse_instruction(row)

    if instruction['cmd'] == 'mask':
        mask = instruction['val']

    if instruction['cmd'] == 'write':
        memory = exec_write(instruction, mask=mask, memory=memory)

total = 0
for memVal in memory.values():
    total += int(memVal, 2)





