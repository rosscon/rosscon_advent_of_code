import intcode

script = [
    'NOT A T',
    'NOT B J',
    'OR T J',
    'NOT C T',
    'OR T J',
    'AND D J',
    'WALK']

intInput = []
for command in script:
    for c in command:
        intInput.append(ord(c))
    intInput.append(ord("\n"))

programState = intcode.load_file_into_memory('input21.txt')
programState['haltFor'] = ['INPUT', 'OUTPUT']
programState['inIo'] = intInput

while programState['haltState'] == 'RUNNING':

    programState = intcode.execute_interactive(programState)

    if programState['haltState'] == 'HALTED_OUTPUT':
        print('HALT')
        break

    if programState['haltState'] == 'PAUSE_OUTPUT':
        programState['haltState'] = 'RUNNING'
        if len(programState['outIo']) == 1:
            try:
                print(chr(programState['outIo'][0]), end='')
            except:
                print(programState['outIo'][0])
        programState['outIo'] = []

    if programState['haltState'] == 'PAUSE_INPUT':
        programState['haltState'] = 'RUNNING'
        instruction = input()
        while not instruction == "":
            for c in instruction:
                programState['inIo'].append(ord(c))
            programState['inIo'].append(ord("\n"))
            instruction = input()

