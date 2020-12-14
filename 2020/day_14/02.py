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


def apply_floating_bitmask (bits, mask):
    output = ['']

    if len(bits) != len(mask):
        return ['ERROR']

    for i in range(0, len(mask)):
        if mask[i] == '0':
            for j in range(0, len(output)):
                output[j] = output[j] + bits[i]

        if mask[i] == '1':
            for j in range(0, len(output)):
                output[j] = output[j] + '1'

        elif mask[i] == 'X':
            #duplicate floating bit
            tmpOutput = []
            for o in output:
                tmpOutput.append(o + '0')
                tmpOutput.append(o + '1')
            output = tmpOutput

    return output


def exec_write(instruction, mask='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', memory={}):


    binAddr = convert_dec_bin(instruction['addr'])

    addresses = apply_floating_bitmask(binAddr, mask)
    print ('Address: ', instruction['addr'], \
           '\nMask: ', mask, \
           '\nAddresses', len(addresses))

    for addr in addresses:
        memory[addr] = instruction['val']

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
    total += memVal

print ('Total: ', total)



