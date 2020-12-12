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


def run_program(memory = [], pc = 0, acc = 0, maxRun = 1):

    while pc < len(memory) and pc >= 0:
        if memory[pc]['exec'] < maxRun:
            execute_result = execute_instruction(memory[pc], pc, acc)
            #print(execute_result)
            memory[pc]['exec'] = True
            pc = execute_result['pc']
            acc = execute_result['acc']
        else:
            pc = -1

    return acc


memory = []

for line in lines:
    memory.append(decode_instruction(line))

accumulator = run_program(memory = memory, pc = 0, acc = _accumulator)