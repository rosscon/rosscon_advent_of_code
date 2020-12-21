

def parse_tile (tile):

    rows = tile.rstrip().split('\n')

    tileId = int(rows[0][5:-1])
    edges = {}

    edges['top'] = rows[1] # Top Row (First)
    edges['bottom'] = rows[-1] # Bottom Row (Last)
    edges['left'] = ''.join([x[0] for x in rows[1:]])
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

    #print('ROTATE  {} {}'.format(tile['id'], angle))

    if len(tile['connected'].items()) > 0:
        "ERROR - Cannot rotate a connected tile"
        return tile

    if angle == 180:
        tile = flip_tile_v(tile)
        tile = flip_tile_h(tile)
        tile['rotation'] += angle
        tile['rotation'] = tile['rotation'] % 360

    elif angle == 90:
        tmpTop = tile['edges']['top']
        tmpBottom = tile['edges']['bottom']
        tmpLeft = tile['edges']['left']
        tmpRight = tile['edges']['right']

        tile['edges']['top'] = tmpLeft[::-1]
        tile['edges']['bottom'] = tmpRight[::-1]
        tile['edges']['left'] = tmpBottom
        tile['edges']['right'] = tmpTop

        tile['rotation'] += angle
        tile['rotation'] = tile['rotation'] % 360

    elif angle == 270:

        tmpTop = tile['edges']['top']
        tmpBottom = tile['edges']['bottom']
        tmpLeft = tile['edges']['left']
        tmpRight = tile['edges']['right']

        tile['edges']['top'] = tmpRight
        tile['edges']['bottom'] = tmpLeft
        tile['edges']['left'] = tmpTop[::-1]
        tile['edges']['right'] = tmpBottom[::-1]


        tile['rotation'] += angle
        tile['rotation'] = tile['rotation'] % 360

    else:
        print('ROTATE ERROR')

    return tile



# Flip a tile horizontally, left becomes right, top and bottom become reversed
def flip_tile_h(tile):

    #print('FLIP-H {}'.format(tile['id']))
    if len(tile['connected'].items()) > 0:
        "ERROR - Cannot flip a connected tile"
        return tile

    tile['flipH'] = not tile['flipH']
    # Swap left and right
    tmpL = tile['edges']['left']
    tile['edges']['left'] = tile['edges']['right']
    tile['edges']['right'] = tmpL

    # Reverse top and bottom
    tile['edges']['top'] = tile['edges']['top'][::-1]
    tile['edges']['bottom'] = tile['edges']['bottom'][::-1]

    return tile

# Flip a tile vertically, top becomes bottom, left and right become reversed
def flip_tile_v(tile):

    #print('FLIP-V {}'.format(tile['id']))
    if len(tile['connected'].items()) > 0:
        "ERROR - Cannot flip a connected tile"
        return tile

    tile['flipV'] = not tile['flipV']
    # Swap left and right
    tmpT = tile['edges']['top']
    tile['edges']['top'] = tile['edges']['bottom']
    tile['edges']['bottom'] = tmpT

    # Reverse top and bottom
    tile['edges']['left'] = tile['edges']['left'][::-1]
    tile['edges']['right'] = tile['edges']['right'][::-1]

    return tile



# finds matches with with all other tiles, aims to only flip other tiles
def find_matches(tileId):

    sides = {
            'top' : {'op': 'bottom', 'fa' : 'v', 'rt': {'left' : 270, 'right' : 90}},
            'bottom': {'op': 'top', 'fa' : 'v', 'rt': {'left' : 90, 'right' : 270}},
            'left' : {'op': 'right', 'fa' : 'h', 'rt': {'top' : 90, 'bottom' : 270}},
            'right': {'op': 'left', 'fa' : 'h', 'rt': {'top' : 270, 'bottom' : 90}}
            }


    for e in sides.keys():

        if e in tiles[tileId]['connected']: continue

        for key,tile in tiles.items():

            if key == tileId: continue

            for s in sides.keys():
                if tile['edges'][s] == tiles[tileId]['edges'][e]: # same direction matching
                    #print ('MATCH c:{}, t:{}'.format(e, s))

                    if sides[e]['op'] == s: # Opposite matching sides require no flip or rotate
                        tiles[key] = tiles[key]
                        #print ('NO ACTION')

                    elif e == s: # If same side then a flip needs to occur
                        #print ('FLIP')
                        if sides[s]['fa'] == 'v':
                            tiles[key] == flip_tile_v(tiles[key])
                        elif sides[s]['fa'] == 'h':
                            tiles[key] == flip_tile_h(tiles[key])
                    else:
                        #print('ROTATE + FLIP REQ {}, - {}'.format(tileId, key))
                        tiles[key] = rotate_tile(tiles[key], sides[e]['rt'][s])
                        if sides[e]['fa'] == 'v':
                            tiles[key] == flip_tile_h(tiles[key])
                        elif sides[e]['fa'] == 'h':
                            tiles[key] == flip_tile_v(tiles[key])

                    # Join Tiles
                    tiles[tileId]['connected'][e] = key
                    tiles[key]['connected'][sides[e]['op']] = tileId
                    find_matches(key)
                    continue



                elif tile['edges'][s][::-1] == tiles[tileId]['edges'][e]: # opposite direction matching
                    #print ('RV-MATCH c:{}, t:{}'.format(e, s))

                    if sides[e]['op'] == s:
                        #print ('FLIP INV')
                        if sides[s]['fa'] == 'v':
                            tiles[key] == flip_tile_h(tiles[key])
                        elif sides[s]['fa'] == 'h':
                            tiles[key] == flip_tile_v(tiles[key])

                    elif e == s:
                        #print ('ROTATE OP')
                        tiles[key] == rotate_tile(tiles[key], 180)

                    else:
                        #print ('ROTATE + REQ {}, - {}'.format(tileId, key))
                        tiles[key] = rotate_tile(tiles[key], sides[e]['rt'][s])


                    # Join Tiles
                    tiles[tileId]['connected'][e] = key
                    tiles[key]['connected'][sides[e]['op']] = tileId
                    find_matches(key)
                    continue

    #return tiles


def find_corners():
    corners = []

    for key, tile in tiles.items():
        if len(tile['connected']) == 2: corners.append(tile)

    return corners





_fileName = "input20.txt"
lines = ""

with open(_fileName) as file:
    lines = file.read().rstrip()

tiles = lines.split("\n\n")
tiles = parse_tiles(tiles)

find_matches(list(tiles.keys())[10])

corners = find_corners()

multiply = 1

for corner in corners:
    multiply *= corner['id']

print("Answer: ", multiply)

