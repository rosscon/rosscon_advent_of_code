import sys

def parse_tile (tile):

    rows = tile.rstrip().split('\n')

    tileId = int(rows[0][5:-1])
    edges = {}

    edges['top'] = rows[1] # Top Row (First)
    edges['bottom'] = rows[-1][::-1] # Bottom Row (Last)
    edges['left'] = ''.join([x[0] for x in rows[1:]])[::-1]
    edges['right'] = ''.join([x[-1] for x in rows[1:]])

    tile = {
            'id' : tileId,
            'edges' : edges,
            'rotation' : 0, # Degress of rotation 0, 90, 180, 270
            'flipH' : False, # whether the tile has been flipped horizontally
            'flipV' : False, # Whether the tile has been flipped vertically
            'tile' : rows[1:], # Original unmodified tile contents
            'connected' : {}
            }

    return tile


def parse_tiles(tiles):

    tmpTiles = {}

    for tile in tiles:
        tile = parse_tile(tile)
        tmpTiles[tile['id']] = tile
    return tmpTiles

# Rotates a tile by a given angle clockwise 90, 180, 270
def rotate_tile(tile, angle):

    print('ROTATE  {} {}'.format(tile['id'], angle))

    if len(tile['connected'].items()) > 0:
        print("ERROR - Cannot rotate a connected tile")
        print(tile['connected'])
        return tile

    if angle == 180:

        print(180)
        tile = rotate_tile(tile, 90)
        tile = rotate_tile(tile, 90)
        return tile

    elif angle == 90:
        tmpTop = tile['edges']['top']
        tmpBottom = tile['edges']['bottom']
        tmpLeft = tile['edges']['left']
        tmpRight = tile['edges']['right']

        tile['edges']['top'] = tmpLeft
        tile['edges']['bottom'] = tmpRight
        tile['edges']['left'] = tmpBottom
        tile['edges']['right'] = tmpTop

        tile['rotation'] += angle
        tile['rotation'] = tile['rotation'] % 360

        return tile

    elif angle == 270:

        tile = rotate_tile(tile, 90)
        tile = rotate_tile(tile, 90)
        tile = rotate_tile(tile, 90)

    else:
        print('ROTATE ERROR')

    return tile



# Flip a tile horizontally, left becomes right, top and bottom become reversed
def flip_tile_h(tile):

    print('FLIP-H {}'.format(tile['id']))
    if len(tile['connected'].items()) > 0:
        "ERROR - Cannot flip a connected tile"
        return tile

    tile['flipH'] = not tile['flipH']
    # Swap left and right
    tmpTop = tile['edges']['top']
    tmpBottom = tile['edges']['bottom']
    tmpLeft = tile['edges']['left']
    tmpRight = tile['edges']['right']

    tile['edges']['top'] = tmpTop[::-1]
    tile['edges']['bottom'] = tmpBottom[::-1]
    tile['edges']['left'] = tmpRight[::-1]
    tile['edges']['right'] = tmpLeft[::-1]

    return tile

# Flip a tile vertically, top becomes bottom, left and right become reversed
def flip_tile_v(tile):

    print('FLIP-V {}'.format(tile['id']))
    if len(tile['connected'].items()) > 0:
        "ERROR - Cannot flip a connected tile"
        return tile

    tile['flipV'] = not tile['flipV']

    tmpTop = tile['edges']['top']
    tmpBottom = tile['edges']['bottom']
    tmpLeft = tile['edges']['left']
    tmpRight = tile['edges']['right']

    tile['edges']['top'] = tmpBottom[::-1]
    tile['edges']['bottom'] = tmpTop[::-1]
    tile['edges']['left'] = tmpLeft[::-1]
    tile['edges']['right'] = tmpRight[::-1]

    return tile



# finds matches with with all other tiles, aims to only flip other tiles
def find_matches(tileId):

    sides = {
            'top' : {'op': 'bottom', 'fa' : 'h', 'rt': {'left' : 270, 'right' : 90}},
            'right': {'op': 'left', 'fa' : 'v', 'rt': {'top' : 270, 'bottom' : 90}},
            'bottom': {'op': 'top', 'fa' : 'h', 'rt': {'left' : 90, 'right' : 270}},
            'left' : {'op': 'right', 'fa' : 'v', 'rt': {'top' : 90, 'bottom' : 270}},
            }


    for e in sides.keys():

        if e in tiles[tileId]['connected']: continue

        for key in tiles.keys():

            if key == tileId: continue

            for s in sides.keys():

                if tiles[key]['edges'][s] == tiles[tileId]['edges'][e]: # same direction matching
                    print ('MATCH c:{}, t:{} {} - {}'.format(e, s, tileId, key))

                    if sides[e]['op'] == s:
                        print ('OP')
                        if sides[s]['fa'] == 'v':
                            tiles[key] == flip_tile_v(tiles[key])
                        elif sides[s]['fa'] == 'h':
                            tiles[key] == flip_tile_h(tiles[key])


                    elif e == s: # If same side then a flip needs to occur
                        print ('S FLIP')
                        if sides[s]['fa'] == 'v':
                            tiles[key] == flip_tile_h(tiles[key])
                        elif sides[s]['fa'] == 'h':
                            tiles[key] == flip_tile_v(tiles[key])

                    else:
                        print('ROTATE REQ {}, - {}'.format(tileId, key))
                        tiles[key] = rotate_tile(tiles[key], sides[e]['rt'][s])

                    if tiles[tileId]['edges'][e] == tiles[key]['edges'][sides[e]['op']]:
                        print('+ FLIP')
                        if sides[s]['fa'] == 'v':
                            tiles[key] == flip_tile_h(tiles[key])
                        elif sides[s]['fa'] == 'h':
                            tiles[key] == flip_tile_v(tiles[key])

                    #Check Translation of tile worked
                    if tiles[tileId]['edges'][e] == tiles[key]['edges'][sides[e]['op']][::-1]:
                        print ("Tiles Matched 1")
                    elif tiles[tileId]['edges'][e] == tiles[key]['edges'][sides[e]['op']]:
                        print ("Tiles Match but Inverted 1")
                    else:
                        print ("Something bad happened 1")
                        sys.exit()

                    # Join Tiles
                    print("JOIN")
                    print('J1 B: ', tiles[tileId]['connected'])
                    tiles[tileId]['connected'][e] = key
                    tiles[key]['connected'][sides[e]['op']] = tileId
                    print('J1 A: ', tiles[tileId]['connected'])

                    find_matches(key)

                    continue



                elif tiles[key]['edges'][s][::-1] == tiles[tileId]['edges'][e]: # opposite direction matching
                    print ('RV-MATCH c:{}, t:{} {} - {}'.format(e, s, tileId, key))

                    if sides[e]['op'] == s:
                        print ('R-OP')

                    elif e == s:
                        print ('ROTATE REQ {}, - {}'.format(tileId, key))
                        tiles[key] == rotate_tile(tiles[key], 180)

                    else:
                        print('ROTATE REQ {}, - {}'.format(tileId, key))
                        tiles[key] = rotate_tile(tiles[key], sides[e]['rt'][s])


                    if tiles[tileId]['edges'][e] == tiles[key]['edges'][sides[e]['op']]:
                        print('+ FLIP')
                        if sides[s]['fa'] == 'v':
                            tiles[key] == flip_tile_v(tiles[key])
                        elif sides[s]['fa'] == 'h':
                            tiles[key] == flip_tile_h(tiles[key])

                    #Check Translation of tile worked
                    if tiles[tileId]['edges'][e] == tiles[key]['edges'][sides[e]['op']][::-1]:
                        print ("Tiles Matched 2")
                    elif tiles[tileId]['edges'][e] == tiles[key]['edges'][sides[e]['op']]:
                        print ("Tiles Match but Inverted 2")
                    else:
                        print ("Something bad happened 2")
                        sys.exit()

                    # Join Tiles
                    print("JOIN2")
                    print('J2 B: ', tiles[tileId]['connected'])
                    tiles[tileId]['connected'][e] = key
                    tiles[key]['connected'][sides[e]['op']] = tileId
                    print('J2 A: ', tiles[tileId]['connected'])
                    find_matches(key)
                    continue

    #return tiles


def find_corners():
    corners = []

    for key, tile in tiles.items():
        if len(tile['connected']) == 2: corners.append(tile)

    return corners


def rotate_tile_contents(tile, angle):

    if angle == 90:
        tmpRows = []
        for i in range(len(tile['tile'])):
            row = ''
            for j in range(len(tile['tile']) -1, -1, -1):
                row += tile['tile'][j][i]
            tmpRows.append(row)
        tile['tile'] = tmpRows

    else:
        if angle == 180:
            tile = rotate_tile_contents(tile, 90)
            tile = rotate_tile_contents(tile, 90)
        elif angle == 270:
            tile = rotate_tile_contents(tile, 90)
            tile = rotate_tile_contents(tile, 90)
            tile = rotate_tile_contents(tile, 90)

    return tile


def transform_tile_contents(tile):

    tile = rotate_tile_contents(tile, tile['rotation'])

    if tile['flipH']:
        rows = []
        for row in tile['tile']:
            rows.append(row[::-1])
        tile['tile'] = rows

    if tile['flipV']:
        tile['tile'] = tile['tile'][::-1]

    return tile

def trim_edges(tile):
    tile['tile'] = tile['tile'][1:-1]
    tmpRows = []
    for row in tile['tile']:
        tmpRows.append(row[1:-1])
    tile['tile'] = tmpRows
    return tile

def tiles_to_image(tileId, rowIndex = -1, gaps = False):

    image = ''

    #Left Master Node
    if rowIndex == -1:
        for i in range(len(tiles[tileId]['tile'])):
            image += tiles[tileId]['tile'][i]
            if gaps:
                image += ' ' + tiles_to_image(tiles[tileId]['connected']['right'], rowIndex = i, gaps = gaps)
            else:
                image += tiles_to_image(tiles[tileId]['connected']['right'], rowIndex = i, gaps = gaps)

            image += "\n"
        if gaps: image += "\n"

        if 'bottom' in tiles[tileId]['connected']:
            image += tiles_to_image(tiles[tileId]['connected']['bottom'], rowIndex = -1, gaps = gaps)


    else:
        image += tiles[tileId]['tile'][rowIndex]
        if 'right' in tiles[tileId]['connected']:
            if gaps:
                image += ' ' + tiles_to_image(tiles[tileId]['connected']['right'], rowIndex = rowIndex, gaps = gaps)
            else:
                image += tiles_to_image(tiles[tileId]['connected']['right'], rowIndex = rowIndex, gaps = gaps)
    return image

def find_top_left(corners):

    for c in corners:
        if 'right' in c['connected'] and 'bottom' in c['connected']:
            if not ('left' in c['connected'] or 'top' in c['connected']):
                return c

    return -1


def find_monsters(image):

    monster = [
            '                  # ',
            '#    ##    ##    ###',
            ' #  #  #  #  #  #   '
            ]

    priorRoughness = image.count('#')
    stop = False

    for r in [0, 90, 180]:
        for flipH in [True, False]:
            for flipV in [True, False]:

                tile = {
                        'rotation' : r, # Degress of rotation 0, 90, 180, 270
                        'flipH' : flipH, # whether the tile has been flipped horizontally
                        'flipV' : flipV, # Whether the tile has been flipped vertically
                        'tile' : image.rstrip().split('\n'), # Original unmodified tile contents
                        'connected' : {}
                        }

                tile = transform_tile_contents(tile)

                # check to see if the monster lines up at any point
                for dx in range(len(tile['tile'][0]) - len(monster[0])):
                    for dy in range(len(tile['tile']) - len(monster)):
                        #print('{} - {}'.format(dx, dy))

                        monsterMatches = True

                        for mx in range(len(monster[0])):
                            for my in range(len(monster)):
                                if (monster[my][mx] == '#'):
                                    if tile['tile'][dy + my][dx + mx] != '#':
                                        monsterMatches = False
                                        break
                            if not monsterMatches: break

                        if monsterMatches:
                            for mx in range(len(monster[0])):
                                for my in range(len(monster)):
                                    if (monster[my][mx] == '#'):
                                        tile['tile'][dy + my] = tile['tile'][dy + my][:dx + mx] + 'O' + tile['tile'][dy + my][dx + mx + 1:]



                afterRoughness = '\n'.join(tile['tile']).count('#')

                print ('\n'.join(monster))
                print ('\n'.join(tile['tile']))
                print ("{} -- {}".format(priorRoughness, afterRoughness))
                print()

                if priorRoughness != afterRoughness:
                    stop = True
                    break
            if stop : break
        if stop: break



    return image


_fileName = "input20.txt"
lines = ""

with open(_fileName) as file:
    lines = file.read().rstrip()

tiles = lines.split("\n\n")
tiles = parse_tiles(tiles)

find_matches(list(tiles.keys())[6])

corners = find_corners()
top_left = find_top_left(corners)


for key in tiles.keys():
    tiles[key] = transform_tile_contents(tiles[key])
    tiles[key] = trim_edges(tiles[key])


image2 = tiles_to_image(top_left['id'], gaps = False)
print(image2)

image3 = find_monsters(image2)

