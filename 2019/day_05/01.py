import pandas as pd

_fileName="input05.txt"
memory = pd.read_csv(_fileName, sep=',', nrows=1, header=None).values[0]
memoryOrig = memory.copy()

#Decodes the opcode instruction and parameters
def decode_instruction(instruction = "fatal"):

    instruction = str(instruction).zfill(5)
    #print(instruction)

    opCodes = {
            "01" : {"ins":"add", "size":4, "io":"iio"},
            "02" : {"ins":"multiply", "size":4, "io":"iio"},
            "03" : {"ins":"int_input", "size":2, "io":"o"},
            "04" : {"ins":"out_value", "size":2, "io":"i"},
            "99" : {"ins":"halt", "size":1, "io":""},
            "fatal" : {"ins":"fatal_err", "size":1, "io":""}
    }

    opcode = instruction[-2:]

    if opcode not in opCodes.keys():
        return opCodes["fatal"]


    modes = {
            "0" : "position",
            "1" : "immediate",
            "fatal" : "error"
    }

    parameterModes = []

    for p in instruction[0:3]:
        if p not in modes:
            parameterModes.append(modes["fatal"])
        else:
            parameterModes.append(modes[p])

    parameterModes = parameterModes[::-1]

    decodedInstruction = opCodes[opcode]
    decodedInstruction["params"] = parameterModes

    return decodedInstruction


#fetches the input values from memory, understands params to locate
def fetch_inputs(instruction, pc):

    blocks = len(instruction["io"])
    inputs = []

    for i in range(0, blocks):
        if instruction["io"][i] == "i":
            if instruction["params"][i] == "position":
                inputs.append(memory[memory[pc + i + 1]])
            elif instruction["params"][i] == "immediate":
                inputs.append(memory[pc + i + 1])

    return inputs

#writes the output to location marked as an oputput location in instruction
def write_output(instruction, output, pc):

    blocks = len(instruction["io"])

    for i in range(0, blocks):
        if instruction["io"][i] == "o":
            if instruction["params"][i] == "position":
                memory[memory[pc + i + 1]] = output
            elif instruction["params"][i] == "immediate":
                memory[pc + i + 1] = output

    return False


#Execute instruction
def execute_instruction(instruction, pc):

    inputs = fetch_inputs(instruction, pc)
    #print ("inputs : ", inputs)
    output = 0


    if(instruction["ins"] == "add"):
        output = ex_add(inputs)

    if(instruction["ins"] == "multiply"):
        output = ex_multiply(inputs)

    if(instruction["ins"] == "int_input"):
        output = ex_int_input(inputs)

    if(instruction["ins"] == "out_value"):
        output = ex_output_value(inputs)

    if(instruction["ins"] == "halt"):
        return -1


    write_output(instruction, output, pc)

    pc += instruction["size"]
    return pc;



def ex_add(inputs):
    return inputs[0] + inputs[1]

def ex_multiply(inputs):
    return inputs[0] * inputs[1]

def ex_int_input(inputs):
    intInput = input("Enter an integer: ")
    intInput = int(intInput)
    return intInput

def ex_output_value(inputs):
    print(inputs[0])

def execute():
    pc = 0
    while pc >= 0:
        instruction = decode_instruction(memory[pc])
        #print(instruction)
        pc = execute_instruction(instruction, pc)
        #pc = -1


execute()
