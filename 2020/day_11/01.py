import copy

_fileName="input11.txt"
_emptySeat='L'
_occupiedSeat='#'
_floor='.'

#Parse input file
infile = open(_fileName, 'r')
rows = [list(line) for line in infile.readlines()]

def get_surrounding_coordinates(x, y):

    return [
            {'x':(x - 1), 'y':(y - 1)},
            {'x':x, 'y':(y - 1)},
            {'x':(x + 1), 'y':(y - 1)},
            {'x':(x - 1), 'y':y},
            {'x':(x + 1), 'y':y},
            {'x':(x - 1), 'y':(y + 1)},
            {'x':x, 'y':(y + 1)},
            {'x':(x + 1), 'y':(y + 1)},
            ]



def get_surrounding_occupied_count(x, y, state):

    occupiedCount = 0

    yMax = len(state)
    xMax = len(state[0])

    surroundingCoordinates = get_surrounding_coordinates(x, y)

    for coordinate in surroundingCoordinates:
        if(coordinate['x'] < 0 or coordinate['x'] >= xMax):
            continue
        if(coordinate['y'] < 0 or coordinate['y'] >= yMax):
            continue

        if state[coordinate['y']][coordinate['x']] == _occupiedSeat:
            occupiedCount += 1

    return occupiedCount;



def iterate_seating(state):

    tmpState = copy.deepcopy(state)

    for y in range(len(state)):
        for x in range(len(state[y])):
            if tmpState[y][x] == _floor:
                continue

            if tmpState[y][x] == _emptySeat:
                if get_surrounding_occupied_count(x, y, state) == 0:
                    tmpState[y][x] = _occupiedSeat

            if tmpState[y][x] == _occupiedSeat:
                if get_surrounding_occupied_count(x, y, state) >= 4:
                    tmpState[y][x] = _emptySeat

    return tmpState

def count_seat_state(state, seatState = _occupiedSeat):
    count = 0

    for y in range(len(state)):
        for x in range(len(state[y])):
            if(state[y][x] == seatState):
                count += 1

    return count

#Loop through seating until no changes
previousState = copy.deepcopy(rows)
newState = copy.deepcopy(rows)

rounds = 0

while((newState != previousState or rounds == 0)):
    previousState = copy.deepcopy(newState)
    newState = iterate_seating(newState)
    rounds += 1

count = count_seat_state(newState)








