import pandas as pd

#Decodes the opcode instruction and parameters
def decode_instruction(instruction = "fatal"):

    instruction = str(instruction).zfill(5)

    opCodes = {
            "01" : {"ins":"add", "size":4, "io":"iio"},
            "02" : {"ins":"multiply", "size":4, "io":"iio"},
            "03" : {"ins":"int_input", "size":2, "io":"o"},
            "04" : {"ins":"out_value", "size":2, "io":"i"},
            "05" : {"ins":"jump-if-true", "size":3, "io":"ii"},
            "06" : {"ins":"jump-if-false", "size":3, "io":"ii"},
            "07" : {"ins":"less_than", "size":4, "io":"iio"},
            "08" : {"ins":"equals", "size":4, "io":"iio"},
            "09" : {"ins":"rb-offset", "size":2, "io":"i"},
            "99" : {"ins":"halt", "size":1, "io":""},
            "fatal" : {"ins":"fatal_err", "size":1, "io":"", "dbg": instruction}
    }

    opcode = instruction[-2:]

    if opcode not in opCodes.keys():
        return opCodes["fatal"]


    modes = {
            "0" : "position",
            "1" : "immediate",
            "2" : "relative",
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
def fetch_inputs(instruction, pc, rb):

    global instanceState

    blocks = len(instruction["io"])
    inputs = []

    for i in range(0, blocks):
        if instruction["io"][i] == "i":

            fetchAddress = -1

            if instruction["params"][i] == "position":
                fetchAddress = instanceState['memory'][pc + i + 1]
            elif instruction["params"][i] == "immediate":
                fetchAddress = pc + i + 1
            elif instruction["params"][i] == "relative":
                relativePos = instanceState['memory'][pc + i + 1]
                fetchAddress = relativePos + rb

            extend_memory(fetchAddress)
            inputs.append(instanceState['memory'][fetchAddress])

    return inputs

def extend_memory(address):
    if(address < 0):
        return -1
    elif address >= len(instanceState['memory']):
        diff = (address + 1) - len(instanceState['memory'])
        tmpMem = [0]*(diff + 1)
        instanceState['memory'].extend(tmpMem)

#writes the output to location marked as an oputput location in instruction
def write_output(instruction, output, pc, rb):

    blocks = len(instruction["io"])

    for i in range(0, blocks):
        if instruction["io"][i] == "o":

            writeAddress = -1

            if instruction["params"][i] == "position":
                writeAddress = instanceState['memory'][pc + i + 1]
            elif instruction["params"][i] == "immediate":
                writeAddress = pc + i + 1
            elif instruction["params"][i] == "relative":
                relativePos = instanceState['memory'][pc + i + 1]
                writeAddress = relativePos + rb

            extend_memory(writeAddress)
            instanceState['memory'][writeAddress] = output

    return False


#Execute instruction
def execute_instruction(instruction, pc, rb):

    inputs = fetch_inputs(instruction, pc, rb)
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

    if(instruction["ins"] == "rb-offset"):
        rb = ex_relative_base(inputs, rb)

    if(instruction["ins"] == "halt"):
        instanceState['haltState'] = 'HALTED'
        return {'pc': -1, 'rb': rb}


    write_output(instruction, output, pc, rb)

    if pc == tmpPc:
        pc += instruction["size"]

    state = {'pc': pc, 'rb': rb}

    return state;



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
    if instanceState['dbgOut']:
        print('>>', inputs[0])
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

def ex_relative_base(inputs, rb):
    return rb + inputs[0]

def load_file_into_memory(filename):

    global instanceState

    memory = pd.read_csv(filename, sep=',', nrows=1, header=None).values[0].tolist()

    tmpState = {'id' : 'Def',
                 'memory' : memory,
                 'pc': 0,
                 'rb' : 0,
                 'inIo': [],
                 'outIo': [],
                 'inPtr' : 0,
                 'haltState' : 'RUNNING', #RUNNING, PAUSE_OUTPUT, PAUSE_INPUT, HALTED
                 'dbgOut' : False
                 }

    instanceState = tmpState
    return instanceState


def execute():

    global instanceState

    while instanceState['pc'] >= 0:
        instruction = decode_instruction(instanceState['memory'][instanceState['pc']])
        es = execute_instruction(instruction, instanceState['pc'], instanceState['rb'])
        instanceState['pc'] = es['pc']
        instanceState['rb'] = es['rb']


def exec_piped_instance(instance):

    global instanceState
    instanceState = instance

    while instanceState['pc'] >= 0 and instanceState['haltState'] == 'RUNNING':
        instruction = decode_instruction(instanceState['memory'][instanceState['pc']])
        es = execute_instruction(instruction, instanceState['pc'], instanceState['rb'])
        instanceState['pc'] = es['pc']
        instanceState['rb'] = es['rb']

    instance = instanceState
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

        if tmpHaltState != 'HALTED':
            instances[currentInstance]['inIo'].append(tmpOutput[-1])

        if instances[currentInstance]['haltState'] == 'HALTED':
            halted = True

    return finalOutput


# Runs the intcode programe but will return state whenever an input is required
def execute_interactive(state):
    global instanceState
    instanceState = state

    while instanceState['pc'] >= 0 and instanceState['haltState'] == 'RUNNING':
        instruction = decode_instruction(instanceState['memory'][instanceState['pc']])
        es = execute_instruction(instruction, instanceState['pc'], instanceState['rb'])
        instanceState['pc'] = es['pc']
        instanceState['rb'] = es['rb']

        #if instanceState['haltState'] == 'PAUSE_OUTPUT':
            #print('PAUSEDOUT')
        #    instanceState['haltState'] = 'RUNNING'

    return instanceState



