import copy

_fileName="input11.txt"
_emptySeat='L'
_occupiedSeat='#'
_floor='.'

#Parse input file
infile = open(_fileName, 'r')
rows = [list(line) for line in infile.readlines()]


def get_visible_occupied_count(x, y, state):

    visibleCount = 0;

    #Traverse upward
    for i in range(y - 1, -1, -1):
        if state[i][x] == _occupiedSeat:
            visibleCount += 1
            break
        elif state[i][x] == _emptySeat:
            break

    #Traverse downward
    for i in range(y + 1, len(state), 1):
        if state[i][x] == _occupiedSeat:
            visibleCount += 1
            break
        elif state[i][x] == _emptySeat:
            break

    #Traverse left
    for i in range(x - 1, -1, -1):
        if state[y][i] == _occupiedSeat:
            visibleCount += 1
            break
        elif state[y][i] == _emptySeat:
            break

    #Traverse right
    for i in range(x + 1, len(state[0]), 1):
        if state[y][i] == _occupiedSeat:
            visibleCount += 1
            break
        elif state[y][i] == _emptySeat:
            break

    #Traverse diagonally
    ul = False
    ur = False
    dl = False
    dr = False
    for i in range(1, min(len(state[0]), len(state))):

        #up-left
        tmpX = x - i
        tmpY = y - i
        if not (tmpX < 0 or tmpY < 0) and not ul:
            if state[tmpY][tmpX] == _occupiedSeat:
                visibleCount += 1
                ul = True
            elif state[tmpY][tmpX] == _emptySeat:
                ul = True

        #up-right
        tmpX = x + i
        tmpY = y - i
        if not (tmpX >= len(state[0]) or tmpY < 0) and not ur:
            if state[tmpY][tmpX] == _occupiedSeat:
                visibleCount += 1
                ur = True
            elif state[tmpY][tmpX] == _emptySeat:
                ur = True

        #down-left
        tmpX = x - i
        tmpY = y + i
        if not (tmpX < 0 or tmpY >= len(state)) and not dl:
            if state[tmpY][tmpX] == _occupiedSeat:
                visibleCount += 1
                dl = True
            elif state[tmpY][tmpX] == _emptySeat:
                dl = True

        #down-right
        tmpX = x + i
        tmpY = y + i
        if not (tmpX >= len(state[0]) or tmpY >= len(state)) and not dr:
            if state[tmpY][tmpX] == _occupiedSeat:
                visibleCount += 1
                dr = True
            elif state[tmpY][tmpX] == _emptySeat:
                dr = True


    return visibleCount;



def iterate_seating(state):

    tmpState = copy.deepcopy(state)

    for y in range(len(state)):
        for x in range(len(state[y])):
            if tmpState[y][x] == _floor:
                continue

            if tmpState[y][x] == _emptySeat:
                if get_visible_occupied_count(x, y, state) == 0:
                    tmpState[y][x] = _occupiedSeat

            if tmpState[y][x] == _occupiedSeat:
                if get_visible_occupied_count(x, y, state) >= 5:
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








