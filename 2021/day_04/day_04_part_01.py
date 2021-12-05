#
# Parse the puzzle input
#

fileName = "input.txt"

infile = open(fileName, 'r')
input_data = [line.strip() for line in infile.readlines()]

draw_numbers = [int(x) for x in input_data[0].split(',')]

boards = []
markings = []

current_board = []
current_markings = []

for row in input_data[2:]:
    if row == '':
        boards.append(current_board)
        markings.append(current_markings)
        current_board = []
        current_markings = []
        continue

    current_board.append([int(x) for x in row.replace('  ', ' ').split(' ')])
    current_markings.append([False for x in row.replace('  ', ' ').split(' ')])


#
# Run bingo games
#

# check the board for number and update markings accordingly
def mark_board(board, board_markings, selected_number):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == selected_number:
                board_markings[i][j] = True
                return board_markings

    return board_markings


# check if markings indicate a winning board
def is_winning_board(board_markings):
    # Check each row
    for i in range(len(board_markings)):
        if len(board_markings[i]) == len([x for x in board_markings[i] if x == True]):
            return True

    # check each column
    for i in range(len(board_markings[i])):
        column = []
        for j in range(len(board_markings)):
            column.append(board_markings[j][i])
        if len(column) == len([x for x in column if x == True]):
            return True

    return False


# Calculates score of winning board
def calculate_score(board, board_markings, selected_number):
    score = 0

    for i in range(len(board_markings)):
        for j in range(len(board_markings[i])):
            if not board_markings[i][j]:
                score += board[i][j]

    return score * selected_number;


for number in draw_numbers:
    print(number)
    for i in range(len(boards)):
        markings[i] = mark_board(boards[i], markings[i], number)

        if is_winning_board(markings[i]):
            score = calculate_score(boards[i], markings[i], number)
            print(markings[i])
            print(boards[i])
            print("Score: " + str(score))
            quit()
