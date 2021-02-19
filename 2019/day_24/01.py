####################################################
# PARSE INPUT
####################################################
def parse_input(in_lines):
    parsed_state = {'x': 0, 'y': 0, 'mins': 0}

    for y in range(len(in_lines)):
        parsed_state['y'] = max(parsed_state['y'], y)
        for x in range(len(in_lines[y])):
            parsed_state['x'] = max(parsed_state['x'], x)
            parsed_state[(x, y)] = in_lines[y][x]

    return parsed_state


####################################################
# TIME STEP
####################################################
def next_step(in_state):
    new_state = {'x': in_state['x'], 'y': in_state['y'], 'mins': in_state['mins'] + 1}
    neighbours = [(0, -1), (-1, 0), (1, 0), (0, 1)]

    for y in range(in_state['y'] + 1):
        for x in range(in_state['x'] + 1):
            count_adjacent_bugs = 0
            for n in neighbours:
                dx, dy = n
                neighbour_key = (x + dx, y + dy)
                if neighbour_key in in_state and in_state[neighbour_key] == "#":
                    count_adjacent_bugs += 1

            if in_state[(x, y)] == "#" and count_adjacent_bugs != 1:
                new_state[(x, y)] = "."
            elif in_state[(x, y)] == "." and (count_adjacent_bugs == 1 or count_adjacent_bugs == 2):
                new_state[(x, y)] = "#"
            else:
                new_state[(x, y)] = in_state[(x, y)]

    return new_state


####################################################
# CALCULATE BIODIVERSITY
####################################################
def calculate_biodiversity(in_state):
    biodiversity = 0
    current_tile_value = 1

    for y in range(in_state['y'] + 1):
        for x in range(in_state['x'] + 1):
            if in_state[(x, y)] == '#':
                biodiversity += current_tile_value
            current_tile_value *= 2

    return biodiversity


####################################################
# STATE TO STRING
####################################################
def state_to_string(in_state):
    state_string = "After {} mins\n ".format(in_state['mins'])
    for y in range(in_state['y'] + 1):
        for x in range(in_state['x'] + 1):
            state_string += in_state[(x, y)]
        state_string += "\n "
    state_string += str(calculate_biodiversity(in_state))

    return state_string


###########################################
# Load initial state from file
###########################################
instructionsFile = "input24.txt"
lines = [line.strip() for line in open(instructionsFile, 'r').readlines()]
state = parse_input(lines)
print(state_to_string(state))
print()

previous_states = {calculate_biodiversity(state): 1}

while True:
    state = next_step(state)
    diversity = calculate_biodiversity(state)
    if diversity in previous_states:
        print(state_to_string(state))
        break
    previous_states[diversity] = 1

