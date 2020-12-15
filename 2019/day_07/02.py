import pandas as pd
import copy

_fileName="input07.txt"
memory = pd.read_csv(_fileName, sep=',', nrows=1, header=None).values[0]
memoryOrig = memory.copy()

instanceState = {'id' : 'Def',
                 'memory' : memory.copy(),
                 'pc': 0,
                 'inIo': [0, 0],
                 'outIo': [],
                 'inPtr' : 0,
                 'haltState' : 'RUNNING' #RUNNING, PAUSE_OUTPUT, PAUSE_INPUT, HALTED
                 }


#Decodes the opcode instruction and parameters
def decode_instruction(instruction = "fatal"):

    instruction = str(instruction).zfill(5)
    #print(instruction)

    opCodes = {
            "01" : {"ins":"add", "size":4, "io":"iio"},
            "02" : {"ins":"multiply", "size":4, "io":"iio"},
            "03" : {"ins":"int_input", "size":2, "io":"o"},
            "04" : {"ins":"out_value", "size":2, "io":"i"},
            "05" : {"ins":"jump-if-true", "size":3, "io":"ii"},
            "06" : {"ins":"jump-if-false", "size":3, "io":"ii"},
            "07" : {"ins":"less_than", "size":4, "io":"iio"},
            "08" : {"ins":"equals", "size":4, "io":"iio"},
            "99" : {"ins":"halt", "size":1, "io":""},
            "fatal" : {"ins":"fatal_err", "size":1, "io":"", "dbg": instruction}
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

    global instanceState

    blocks = len(instruction["io"])
    inputs = []

    for i in range(0, blocks):
        if instruction["io"][i] == "i":
            if instruction["params"][i] == "position":
                inputs.append(instanceState['memory'][instanceState['memory'][pc + i + 1]])
            elif instruction["params"][i] == "immediate":
                inputs.append(instanceState['memory'][pc + i + 1])

    return inputs

#writes the output to location marked as an oputput location in instruction
def write_output(instruction, output, pc):

    blocks = len(instruction["io"])

    for i in range(0, blocks):
        if instruction["io"][i] == "o":
            if instruction["params"][i] == "position":
                instanceState['memory'][instanceState['memory'][pc + i + 1]] = output
            elif instruction["params"][i] == "immediate":
                instanceState['memory'][pc + i + 1] = output

    return False


#Execute instruction
def execute_instruction(instruction, pc):

    inputs = fetch_inputs(instruction, pc)
    #print('inputs: ', inputs)
    #print ("inputs : ", inputs)
    output = 0

    tmpPc = pc


    if(instruction["ins"] == "add"):
        output = ex_add(inputs)

    if(instruction["ins"] == "multiply"):
        output = ex_multiply(inputs)

    if(instruction["ins"] == "int_input"):
        output = ex_int_input(inputs)

    if(instruction["ins"] == "out_value"):
        output = ex_output_value(inputs)

    if(instruction["ins"] == "jump-if-true"):
        pc = ex_jump_if_true(inputs, pc)

    if(instruction["ins"] == "jump-if-false"):
        pc = ex_jump_if_false(inputs, pc)

    if(instruction["ins"] == "less_than"):
        output = ex_less_than(inputs)

    if(instruction["ins"] == "equals"):
        output = ex_equals(inputs)

    if(instruction["ins"] == "halt"):
        instanceState['haltState'] = 'HALTED'
        return -1


    write_output(instruction, output, pc)

    if pc == tmpPc:
        pc += instruction["size"]
    return pc;



def ex_add(inputs):
    return inputs[0] + inputs[1]

def ex_multiply(inputs):
    return inputs[0] * inputs[1]

def ex_int_input(inputs):

    global instanceState

    if(len(instanceState['inIo']) < (instanceState['inPtr'] + 1)):
        intInput = input("Enter an integer: ")
        return int(intInput)
    else:
        intInput = int(instanceState['inIo'][instanceState['inPtr']])
        instanceState['inPtr'] += 1
        return intInput

    return -1

def ex_output_value(inputs):
    global instanceState
    print(inputs[0])
    instanceState['outIo'].append(inputs[0])
    instanceState['haltState'] = 'PAUSE_OUTPUT'

def ex_jump_if_true(inputs, pc):
    if inputs[0] != 0:
        pc = inputs[1]
    return pc

def ex_jump_if_false(inputs, pc):
    if inputs[0] == 0:
        pc = inputs[1]
    return pc

def ex_less_than(inputs):
    if inputs[0] < inputs[1]:
        return 1
    else:
        return 0

def ex_equals(inputs):
    if inputs[0] == inputs[1]:
        return 1
    else:
        return 0

def execute():

    global instanceState

    while instanceState['pc'] >= 0:
        instruction = decode_instruction(instanceState['memory'][instanceState['pc']])
        #print(instruction)
        instanceState['pc'] = execute_instruction(instruction, instanceState['pc'])
        #pc = -1


def exec_piped_instance(instance):

    global instanceState
    instanceState = instance

    while instanceState['pc'] >= 0 and instanceState['haltState'] == 'RUNNING':
        instruction = decode_instruction(instanceState['memory'][instanceState['pc']])
        #print(instruction)
        instanceState['pc'] = execute_instruction(instruction, instanceState['pc'])


    return instance


def execute_piped(instances, initInstance = 0):

    halted = False

    currentInstance = 0
    finalOutput = 0

    while not halted:

        print ('Switching to instance: ', currentInstance)

        instances[currentInstance]['haltState'] = 'RUNNING'
        instances[currentInstance] = exec_piped_instance(instances[currentInstance])

        tmpHaltState = instances[currentInstance]['haltState']
        tmpOutput = instances[currentInstance]['outIo']
        finalOutput = tmpOutput

        currentInstance += 1
        currentInstance = currentInstance % len(instances)

        #print (tmpOutput)

        if tmpHaltState != 'HALTED':
            instances[currentInstance]['inIo'].append(tmpOutput[-1])

        if instances[currentInstance]['haltState'] == 'HALTED':
            halted = True

    return finalOutput




#execute()


amplifiers = [
        {'id' : 'Amp A', 'memory' : memory.copy(), 'pc': 0, 'inIo': [0, 0], 'outIo': [], 'inPtr' : 0, 'haltState':'RUNNING'},
        {'id' : 'Amp B', 'memory' : memory.copy(), 'pc': 0, 'inIo': [0], 'outIo': [], 'inPtr' : 0, 'haltState':'RUNNING'},
        {'id' : 'Amp C', 'memory' : memory.copy(), 'pc': 0, 'inIo': [0], 'outIo': [], 'inPtr' : 0, 'haltState':'RUNNING'},
        {'id' : 'Amp D', 'memory' : memory.copy(), 'pc': 0, 'inIo': [0], 'outIo': [], 'inPtr' : 0, 'haltState':'RUNNING'},
        {'id' : 'Amp E', 'memory' : memory.copy(), 'pc': 0, 'inIo': [0], 'outIo': [], 'inPtr' : 0, 'haltState':'RUNNING'}
        ]


#output = execute_piped(amplifiers)
print('-------')

#loop through all combinations of phase inputs
from itertools import permutations


phaseInputs = [5, 6, 7, 8, 9]

maxSignal = 0

for combo in permutations(phaseInputs, 5):

    combo = list(combo)
    print (combo)

    tmpAmplifiers = copy.deepcopy(amplifiers)

    for i in range(0, len(tmpAmplifiers)):
        tmpAmplifiers[i]['inIo'][0] = combo[i]
        print (tmpAmplifiers[i]['inIo'])

    tmpOut = execute_piped(tmpAmplifiers)[-1]

    if tmpOut > maxSignal:
        maxSignal = tmpOut

print ('Max signal: ', maxSignal)






