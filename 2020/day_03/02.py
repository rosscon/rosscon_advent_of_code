
def check_slope(filename, x=0, y=0, dx=1, dy=1, tree="#", openSq="."):
    infile = open(_fileName, 'r')
    lines = [line.rstrip() for line in infile.readlines()]
    treeCount = 0

    for y in range(y, len(lines), dy):
        #print("[", x, ",", y, "] - ", lines[y][x])
        if lines[y][x] == tree:
            treeCount += 1

        x += dx
        if x >= len(lines[y]):
            x -= len(lines[y])

    return treeCount


_fileName="input03.txt"
_slopes = [
        {"x": 0, "y": 0, "dx": 1, "dy": 1},
        {"x": 0, "y": 0, "dx": 3, "dy": 1},
        {"x": 0, "y": 0, "dx": 5, "dy": 1},
        {"x": 0, "y": 0, "dx": 7, "dy": 1},
        {"x": 0, "y": 0, "dx": 1, "dy": 2}
        ]

multiplied = 1;

for slope in _slopes:
    trees = check_slope(filename=_fileName, dx=slope["dx"], dy=slope["dy"])
    print("Slope ", slope, " Trees ", trees)
    multiplied *= trees

print ("Sloped multiplied = ", multiplied)