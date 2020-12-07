# Read in input file line by line
_fileName="input05.txt"
_tree="#"
_open="."

infile = open(_fileName, 'r')
lines = [line.rstrip() for line in infile.readlines()]


def decode_binary(string, t="1", f="0"):

    bits = string[::-1]

    sum = 0
    val = 1

    for bit in bits:
        if bit == t:
            sum += val
        val = val * 2

    return sum


def decode_seat(seat):

    rowPart = seat[:7]
    columnPart = seat[7:]

    row = decode_binary(rowPart, t = "B", f = "F")
    column = decode_binary(columnPart, t = "R", f = "L")

    return (row * 8) + column


seats = []

for seat in lines:
    seats.append(decode_seat(seat))

maxId = 0
for seat in seats:
    if seat > maxId:
        maxId = seat

print ("Max seat ID: ", maxId)

previousId = 0
gaps = []

seats.sort()

for seat in seats:
    if seat > (previousId + 1):
        gaps.append(previousId + 1)
    previousId = seat
