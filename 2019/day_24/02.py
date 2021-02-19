####################################################
# PARSE INPUT
####################################################
def parse_input(in_lines):
    parsed_state = {'x': 0, 'y': 0, 'mins': 0, 'zmin': 0, 'zmax': 0}

    for y in range(len(in_lines)):
        parsed_state['y'] = max(parsed_state['y'], y)
        for x in range(len(in_lines[y])):
            if not (x == 2 and y == 2):
                parsed_state['x'] = max(parsed_state['x'], x)
                parsed_state[(x, y, 0)] = in_lines[y][x]

    return parsed_state


####################################################
# GET NEIGHBOURS RECURSIVE
# for recursive need to get neighbours in
# other levels too
####################################################
def get_neighbours(in_x, in_y, in_z):
    neighbours = []

    # OUTER EDGES - Connect with upper layer
    # Top row
    if in_y == 0:
        neighbours.append((2, 1, in_z - 1))

    # Bottom row
    if in_y == 4:
        neighbours.append((2, 3, in_z - 1))

    # Left Column
    if in_x == 0:
        neighbours.append((1, 2, in_z - 1))

    # Right column
    if in_x == 4:
        neighbours.append((3, 2, in_z - 1))

    # INNER EDGES - Connect with lower layer
    # Top
    if in_x == 2 and in_y == 1:
        neighbours.append((0, 0, in_z + 1))
        neighbours.append((1, 0, in_z + 1))
        neighbours.append((2, 0, in_z + 1))
        neighbours.append((3, 0, in_z + 1))
        neighbours.append((4, 0, in_z + 1))

    # Bottom
    if in_x == 2 and in_y == 3:
        neighbours.append((0, 4, in_z + 1))
        neighbours.append((1, 4, in_z + 1))
        neighbours.append((2, 4, in_z + 1))
        neighbours.append((3, 4, in_z + 1))
        neighbours.append((4, 4, in_z + 1))

    # Left
    if in_x == 1 and in_y == 2:
        neighbours.append((0, 0, in_z + 1))
        neighbours.append((0, 1, in_z + 1))
        neighbours.append((0, 2, in_z + 1))
        neighbours.append((0, 3, in_z + 1))
        neighbours.append((0, 4, in_z + 1))

    # Right
    if in_x == 3 and in_y == 2:
        neighbours.append((4, 0, in_z + 1))
        neighbours.append((4, 1, in_z + 1))
        neighbours.append((4, 2, in_z + 1))
        neighbours.append((4, 3, in_z + 1))
        neighbours.append((4, 4, in_z + 1))

    # SAME LEVEL
    for n in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
        dx, dy = n
        if 0 <= (in_x + dx) <= 4 and 0 <= (in_y + dy) <= 4:
            neighbours.append((in_x + dx, in_y + dy, in_z))

    return neighbours


####################################################
# ADD LAYERS
####################################################
def add_layers(in_state):
    in_state['zmax'] += 1
    in_state['zmin'] -= 1

    for x in range(5):
        for y in range(5):
            if not (x == 2 and y == 2):
                in_state[(x, y, in_state['zmax'])] = "."
                in_state[(x, y, in_state['zmin'])] = "."

    return in_state


####################################################
# TIME STEP
####################################################
def next_step(in_state):
    in_state = add_layers(in_state)

    new_state = {
        'x': in_state['x'],
        'y': in_state['y'],
        'mins': in_state['mins'] + 1,
        'zmin': in_state['zmin'],
        'zmax': in_state['zmax']
    }

    for key, value in in_state.items():
        if type(key) is tuple:
            x, y, z = key
            count_adjacent_bugs = 0
            ns = get_neighbours(x, y, z)
            for n in ns:
                if n in in_state:
                    if in_state[n] == "#":
                        count_adjacent_bugs += 1

            if in_state[key] == "#" and count_adjacent_bugs != 1:
                new_state[key] = "."
            elif in_state[key] == "." and (count_adjacent_bugs == 1 or count_adjacent_bugs == 2):
                new_state[key] = "#"
            else:
                new_state[key] = in_state[key]

    return new_state


####################################################
# COUNT BUGS
####################################################
def count_bugs(in_state):
    bugs = 0

    for value in in_state.values():
        if value == '#':
            bugs += 1

    return bugs


####################################################
# STATE TO STRING
####################################################
def state_to_string(in_state):
    state_string = "After {} mins\n ".format(in_state['mins'])
    for z in range(in_state['zmin'], in_state['zmax'] + 1):
        state_string += "Depth {}\n ".format(z)
        for y in range(in_state['y'] + 1):
            for x in range(in_state['x'] + 1):
                if (x, y, z) in in_state:
                    state_string += in_state[(x, y, z)]
                else:
                    state_string += "?"
            state_string += "\n "
        state_string += "\n"

    return state_string


###########################################
# Load initial state from file
###########################################
instructionsFile = "input24.txt"
lines = [line.strip() for line in open(instructionsFile, 'r').readlines()]
state = parse_input(lines)
print(state_to_string(state))
print()

for i in range(200):
    state = next_step(state)

#print(state_to_string(state))
print(count_bugs(state))
