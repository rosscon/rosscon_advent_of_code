import intcode
import time

programState = intcode.load_file_into_memory('input13.txt')
programState['haltFor'] = ['INPUT', 'OUTPUT']
programState['memory'][0] = 2

tiles = {
        0: ' ', # Empty Space
        1: 'X', # Wall
        2: '=', # Block
        3: 'T', # Horizontal paddle
        4: 'O' # Ball
        }


gameState = {
        'minX' : 0,
        'minY' : 0,
        'maxX' : 0,
        'maxY' : 0,
        'score' : 0,
        'ballX' : 0,
        'paddleX' : 0
        }

def update_game_state(state, gameState = gameState, tiles = tiles):
    x = state[0]
    y = state[1]

    if x >= 0:
        t = tiles[state[2]]
        gameState["{},{}".format(x,y)] = t

        if x < gameState['minX'] : gameState['minX'] = x
        if x > gameState['maxX'] : gameState['maxX'] = x
        if y < gameState['minY'] : gameState['minY'] = y
        if y > gameState['maxY'] : gameState['maxY'] = y

        if state[2] == 3 : gameState['paddleX'] = x
        if state[2] == 4 : gameState['ballX'] = x

    elif x == -1:
        gameState['score'] = state[2]



def print_game_state(gameState):

    output = ''

    blockCount = count_tiles(gameState, '=')

    print ('Score: ', gameState['score'], ' Block Count: ', blockCount)
    for y in range(gameState['minY'], gameState['maxY'] + 1):
        for x in range(gameState['minX'], gameState['maxX'] + 1):
            key = "{},{}".format(x,y)
            if key in gameState:
                #print(gameState[key], end = '')
                output += gameState[key]
            else:
                gameState[key] += '*'
                #print('*', end = '')
        #print()
        output += '\n'

    print (output)
    time.sleep(.017)

def count_tiles(gameState, tile):
    count = 0

    for v in gameState.values():
        if v == tile: count += 1

    return count



while programState['haltState'] == 'RUNNING':

    programState = intcode.execute_interactive(programState)

    if programState['haltState'] == 'HALTED_OUTPUT':
        print ('HALT')
        break

    if programState['haltState'] == 'PAUSE_OUTPUT':
        programState['haltState'] = 'RUNNING'
        if (len(programState['outIo']) == 3):
            update_game_state(programState['outIo'])
            programState['outIo'] = []
            if len(gameState) >= 1007:
                if count_tiles(gameState, 'T') > 0 and count_tiles(gameState, 'O') > 0:
                    print_game_state(gameState)


    if programState['haltState'] == 'PAUSE_INPUT':
        programState['haltState'] = 'RUNNING'

        # Follow the ball with the paddle
        if gameState['ballX'] < gameState['paddleX']:
            programState['inIo'].append(-1)
        elif gameState['ballX'] > gameState['paddleX']:
            programState['inIo'].append(1)
        else: programState['inIo'].append(0)

        #print('inputs: ', programState['inIo'])


    #programState['haltState'] = 'RUNNING'


print_game_state(gameState)
blockCount = count_tiles(gameState, '=')
print('Block Count: ', blockCount)