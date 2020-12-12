# Read in input file line by line
_fileName="input08.txt"

infile = open(_fileName, 'r')
lines = [line for line in infile.readlines()]

_accumulator = 0


def decode_instruction(instruction):

    operation = instruction.split(" ")[0]
    argument = int(instruction.split(" ")[1])
    decodedInstruction = { 'op' : operation, 'arg': argument, 'exec': 0}
    return decodedInstruction

def execute_instruction(instruction, pc, acc):

    #print (instruction)

    if instruction['op'] == 'nop':
        pc += 1
        return {'pc' : pc, 'acc': acc}

    if instruction['op'] == 'acc':
        pc += 1
        acc += instruction['arg']
        return {'pc' : pc, 'acc': acc}

    if instruction['op'] == 'jmp':
        pc += instruction['arg']
        return {'pc' : pc, 'acc': acc}

    return {'pc' : -1, 'acc' : -1}


def run_program(mem = [], pc = 0, acc = 0, maxRun = 1):

    while pc < len(mem) and pc >= 0:
        if mem[pc]['exec'] < maxRun:
            execute_result = execute_instruction(mem[pc], pc, acc)
            #print(execute_result)
            mem[pc]['exec'] += 1
            pc = execute_result['pc']
            acc = execute_result['acc']
        else:
            pc = -1

    return {'pc' : pc, 'acc' : acc}


memory = []

for line in lines:
    memory.append(decode_instruction(line))

for i in range(len(memory)):
    tmpMemory = []
    for line in lines:
        tmpMemory.append(decode_instruction(line))


    if tmpMemory[i]['op'] == 'acc':
        continue
    else:
        if tmpMemory[i]['op'] == 'nop' and tmpMemory[i]['arg'] != 0:
            tmpMemory[i]['op'] = 'jmp'
            #print('nop to jmp ', memory[i], tmpMemory[i])
        elif tmpMemory[i]['op'] == 'jmp':
            tmpMemory[i]['op'] = 'nop'
            #print(memory[i], tmpMemory[i])
        else:
            continue

        programResult = run_program(mem = tmpMemory, pc = 0, acc = 0)

        if programResult['pc'] != -1:
            print (programResult)
            break
        else:
            print ('loop detected', programResult, '\n')



