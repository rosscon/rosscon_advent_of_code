

def parse_line(line):
    parsedLine = [line[0]]
    for c in line[1:]:
        if parsedLine[-1] == 's' or parsedLine[-1] == 'n':
            parsedLine[-1] = parsedLine[-1] + c
        else:
            parsedLine.append(c)
    return parsedLine


def setup_tiles(lines, oddT, evenT):
    tiles = {}

    # Process each line
    for line in lines:
        line = parse_line(line)

        coord = { 'x' : 0, 'y': 0 }

        for t in line:
            if coord['y'] % 2 == 0:
                translations = evenT
            else:
                translations = oddT

            mv = translations[t]
            coord['x'] += mv['x']
            coord['y'] += mv['y']

        if tile_to_key(coord) in tiles:
            tiles[tile_to_key(coord)] += 1
        else:
            tiles[tile_to_key(coord)] = 1

    for key,tile in tiles.items():
        if tile % 2 == 1:
            tiles[key] = 1
        else:
            tiles[key] = 0

    return tiles


def tile_to_key(tile):
    return '{},{}'.format(tile['x'], tile['y'])


def key_to_tile(key):
    return { 'x': int(key.split(',')[0]), 'y' : int(key.split(',')[1]) }


def get_surrounding_tiles(tile, oddT, evenT):

    surrounding = []

    translation = oddT

    if tile['y'] % 2 == 0:
        translation = evenT

    for key,value in translation.items():
        surrounding.append({ 'x' : tile['x'] + value['x'], 'y' : tile['y'] + value['y']})

    return surrounding



def count_black_tiles(tiles):
    blackTiles = 0

    for key,tile in tiles.items():
        if tile % 2 == 1:
            blackTiles += 1

    return blackTiles




def iterate_tiles(tiles, oddT, evenT):
    newTiles = {}

    for tile in tiles:
        tile = key_to_tile(tile)
        checkTiles = get_surrounding_tiles(tile, oddT, evenT) + [tile]

        for t in checkTiles:
            ct = get_surrounding_tiles(t, oddT, evenT)
            surr = {}
            for c in ct:
                key = tile_to_key(c)
                if key in tiles:
                    surr[key] = tiles[key]

            key = tile_to_key(t)
            blackCount = count_black_tiles(surr)
            ownState = 0

            if key in tiles:
                ownState = tiles[key] % 2

            if ownState == 1 and blackCount > 0 and blackCount <= 2:
                newTiles[key] = 1

            if ownState == 0 and blackCount == 2:
                newTiles[key] = 1


    return newTiles


_fileName = "input24.txt"
lines = ""


with open(_fileName) as file:
    lines = file.read().rstrip()

lines = lines.split("\n")

oddT = {
        'w' :  { 'x': -1, 'y': 0 },
        'e' :  { 'x': 1,  'y': 0 },
        'sw' : { 'x': 0, 'y': -1 },
        'se' : { 'x': 1,  'y': -1 },
        'nw' : { 'x': 0, 'y': 1 },
        'ne' : { 'x': 1,  'y': 1 }
        }

evenT = {
        'w' :  { 'x': -1, 'y': 0 },
        'e' :  { 'x': 1,  'y': 0 },
        'sw' : { 'x': -1, 'y': -1 },
        'se' : { 'x': 0,  'y': -1 },
        'nw' : { 'x': -1, 'y': 1 },
        'ne' : { 'x': 0,  'y': 1 }
        }



tiles = setup_tiles(lines, oddT, evenT)


countBlack = 0

for key,tile in tiles.items():
    if tile % 2 == 1:
        countBlack += 1

print ('Black Tiles: ', countBlack)


for i in range(100):
    tiles = iterate_tiles(tiles, oddT, evenT)
    print("Day {}: {}".format(i + 1, len(tiles.items())))






