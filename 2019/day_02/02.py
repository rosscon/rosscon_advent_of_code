import pandas as pd

_fileName="input02.txt"
memory = pd.read_csv(_fileName, sep=',', nrows=1, header=None).values[0]
memoryOrig = memory.copy()

def decode_instruction(instructionId = -1):

    instructions = {
            1 : {"ins":"add", "size":4},
            2 : {"ins":"mul", "size":4},
            99 : {"ins":"halt", "size":1},
            -1 : {"ins":"err", "size":1}
    }

    if instructionId in instructions.keys():
        return instructions[instructionId]
    else:
        #Error state
        return instructions[-1]


def execute_instruction(instruction, pc):

    if(instruction["ins"] == "add"):
        #print("add ", pc)
        ex_add(memory[ pc+1 : pc+instruction["size"] ])

    if(instruction["ins"] == "mul"):
        #print("mul ", pc)
        ex_mul(memory[ pc+1 : pc+instruction["size"] ])

    if(instruction["ins"] == "halt"):
        return -1

    pc += instruction["size"]
    return pc;

def ex_add(ins):
    #print(ins)
    memory[ins[2]] = memory[ins[0]] + memory[ins[1]]

def ex_mul(ins):
    #print(ins)
    memory[ins[2]] = memory[ins[0]] * memory[ins[1]]

def execute(noun, verb):

    memory[1] = noun
    memory[2] = verb

    pc = 0

    while pc >= 0:
        instruction = decode_instruction(memory[pc])
        pc = execute_instruction(instruction, pc)


target = 19690720
finished = False

for n in range(0,100):
    for v in range(0,100):
        memory = memoryOrig.copy()
        execute(n, v)
        print("Noun : ", n, " Verb : ", v, "Result : " , memory[0])
        if memory[0] == target:
            print("Result : ", ((100 * n) + v))
            finished = True
            break
    if finished:
        break
