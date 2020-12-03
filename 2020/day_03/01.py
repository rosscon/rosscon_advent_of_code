# Read in input file line by line
_fileName="input03.txt"
_tree="#"
_open="."

infile = open(_fileName, 'r')
lines = [line.rstrip() for line in infile.readlines()]

dx = 3 #positive right, negative left
dy = 1 #positive down, negative up

x = 0
y = 0

treeCount = 0
openCount = 0
errorCount = 0

for y in range(y, len(lines), dy):
    print("[", x, ",", y, "] - ", lines[y][x])
    if lines[y][x] == _tree:
        treeCount += 1
    elif lines[y][x] == _open:
        openCount += 1
    else:
        errorCount +=1

    x += dx
    if x >= len(lines[y]):
        x -= len(lines[y])


print ("Trees = ", treeCount)
print ("Open squares = ", openCount)
print ("Errors = ", openCount)