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


def timestamp_matches_pattern(timestamp, busses):

    for i in range(0, len(busses)):
        if busses[i] != 'x':
            if get_bus_next_timestamp(timestamp, int(busses[i])) != (timestamp + i):
                return False

    return True


def get_time_to_next_bus(timestamp, busFrequency):
    for i in range (0, busFrequency):
        if (timestamp + i) % busFrequency == 0:
            return i


currentTimestamp = int(busses[0])
step = int(busses[0])

for bus in busses[1:]:
    if bus != 'x':

        print('Bus: ', bus)

        while(True):

            print('Timestamp: ', currentTimestamp, \
                  '\tGap: ', (currentTimestamp + busses.index(bus)) % int(bus))

            if (currentTimestamp + busses.index(bus)) % int(bus) == 0:
                print('Timestamp: ', currentTimestamp, '\tBusID: ', busses[busses.index(bus)])
                break;
            currentTimestamp += step


        step = step * int(bus)
        print('Step: ', step, '\n')

print ('Solution: ', currentTimestamp)