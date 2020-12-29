

def parse_line(line):
    parsedLine = [line[0]]
    for c in line[1:]:
        if parsedLine[-1] == 's' or parsedLine[-1] == 'n':
            parsedLine[-1] = parsedLine[-1] + c
        else:
            parsedLine.append(c)
    return parsedLine




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


flippedTiles = {}

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
        print("{} - {}".format(t, coord))

    if str(coord) in flippedTiles:
        flippedTiles[str(coord)] += 1
    else:
        flippedTiles[str(coord)] = 1

    print()

countBlack = 0

for key,tile in flippedTiles.items():
    if tile % 2 == 1:
        countBlack += 1


print ('Black Tiles: ', countBlack)







