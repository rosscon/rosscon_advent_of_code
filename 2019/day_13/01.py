import intcode

programState = intcode.load_file_into_memory('input13.txt')

tiles = {
        0: ' ', # Empty Space
        1: 'X', # Wall
        2: '=', # Block
        3: '_', # Horizontal paddle
        4: 'O' # Ball
        }


gameState = {
        'minX' : 0,
        'minY' : 0,
        'maxX' : 0,
        'maxY' : 0
        }

def update_game_state(state, gameState = gameState, tiles = tiles):
    x = state[0]
    y = state[1]
    t = tiles[state[2]]
    gameState["{},{}".format(x,y)] = t

    if x < gameState['minX'] : gameState['minX'] = x
    if x > gameState['maxX'] : gameState['maxX'] = x
    if y < gameState['minY'] : gameState['minY'] = y
    if y > gameState['maxY'] : gameState['maxY'] = y


def print_game_state(gameState):
    for y in range(gameState['minY'], gameState['maxY'] + 1):
        for x in range(gameState['minX'], gameState['maxX'] + 1):
            key = "{},{}".format(x,y)
            if key in gameState:
                print(gameState[key], end = '')
            else:
                print('*', end = '')
        print()

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
        #print ('PAUSED')
        programState['haltState'] = 'RUNNING'
        if (len(programState['outIo']) == 3):
            update_game_state(programState['outIo'])
            programState['outIo'] = []


    #programState['haltState'] = 'RUNNING'


print_game_state(gameState)
blockCount = count_tiles(gameState, '=')
print('Block Count: ', blockCount)