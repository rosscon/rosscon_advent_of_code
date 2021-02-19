import intcode

programState = intcode.load_file_into_memory('input25.txt')
programState['haltFor'] = ['INPUT', 'OUTPUT']

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
        for c in instruction:
            programState['inIo'].append(ord(c))
        programState['inIo'].append(10)

