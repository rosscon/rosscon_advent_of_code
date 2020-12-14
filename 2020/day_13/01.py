_fileName="input13.txt"


#Parse input file
infile = open(_fileName, 'r')
rows = [line for line in infile.readlines()]

arrivalEstimate = int(rows[0])
busses = rows[1].split(',')


def get_bus_next_timestamp(currentTimestamp, busFrequency):

    for i in range (0, busFrequency):
        if (currentTimestamp + i) % busFrequency == 0:
            return (currentTimestamp + i)

    return -1;


minTimestamp = -1
minBusId = 0

for bus in busses:
    if bus != 'x':
        bus = int(bus)
        nextTimestamp = get_bus_next_timestamp(arrivalEstimate, bus)

        if nextTimestamp < minTimestamp or minTimestamp == -1:
            minTimestamp = nextTimestamp
            minBusId = bus

answer = (minTimestamp - arrivalEstimate) * minBusId