import pandas as pd

_fileName="input02.txt"
memory = pd.read_csv(_fileName, sep=',', nrows=1, header=None).values[0]
pc=0

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

memory[1] = 12
memory[2] = 2

while pc >= 0:
    instruction = decode_instruction(memory[pc])
    pc = execute_instruction(instruction, pc)


print (memory[0])