# Global Consts
neighbours = [[-1, 0], [0, 1], [1, 0], [0, -1]]


def coord_to_key(x, y):
    return "{0},{1}".format(x, y)


def coord_to_key_level(x, y, z):
    return "{0},{1},{2}".format(x, y, z)


def key_to_coord(i_key):
    return int(i_key.split(',')[0]), int(i_key.split(',')[1])


def key_to_coord_level(i_key):
    return int(i_key.split(',')[0]), int(i_key.split(',')[1]), int(i_key.split(',')[2])


# Parses the input maze file into a series of cells and portals
def parse_input_lines(lines):
    l_cells = {}
    l_portals = {}

    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == '.':  # Passable cell
                key = coord_to_key(x, y)
                l_cells[key] = {}
            elif lines[y][x].isalpha():  # Portal cell
                # Check neighbouring cells for a passable cell and other half of portal_id
                key = ""
                portal_id = lines[y][x]

                for n in neighbours:
                    x1 = x + n[0]
                    y1 = y + n[1]

                    if not (x1 < 0 or y1 < 0 or y1 >= (len(lines)) or x1 >= len(lines[y1])):
                        if lines[y1][x1] == '.':  # Only process from the cell that is adjacent to the maze
                            key = coord_to_key(x1, y1)
                        elif lines[y1][x1].isalpha():
                            if x1 < x or y1 < y:  # Determine portal_id order
                                portal_id = lines[y1][x1] + portal_id
                            else:
                                portal_id = portal_id + lines[y1][x1]

                if key != "":  # Only want to process the cell was adjacent to maze
                    if portal_id not in l_portals.keys():
                        l_portals[portal_id] = []
                    l_portals[portal_id].append(key)

    return l_cells, l_portals


# Builds a graph structure from the parsed input
def build_graph(i_cells, i_portals, i_x, i_y):
    # Link cells that share a portal
    for p_key, portal in i_portals.items():
        if len(portal) > 1:  # Need to avoid the entry/exit portals
            i_cells[portal[0]]['children'] = [portal[1]]
            i_cells[portal[1]]['children'] = [portal[0]]

            # Determine which cell is inner and which is outer
            t_x, t_y = key_to_coord(portal[0])
            if t_x == 2 or t_x == i_x - 3 or t_y == 2 or t_y == i_y - 3:  # Outer
                i_cells[portal[0]]['level'] = -1
                i_cells[portal[1]]['level'] = 1
            else:  # Inner
                i_cells[portal[0]]['level'] = 1
                i_cells[portal[1]]['level'] = -1

    # Link Cells to each other
    for c_key, cell in i_cells.items():
        x, y = key_to_coord(c_key)
        for n in neighbours:
            x1 = x + n[0]
            y1 = y + n[1]
            t_key = coord_to_key(x1, y1)
            if t_key in i_cells:
                if 'children' not in cell:
                    cell['children'] = []
                cell['children'].append(t_key)

    return i_cells


# Perform a breadth first search on the graph of connected cells
def bfs_recursive(i_cells, start, end):
    visited = {start}
    queue = [start]

    t_parents = {}

    while queue:
        c_key = queue.pop(0)
        if c_key == end:
            break

        x, y, z = key_to_coord_level(c_key)
        t_cell = i_cells[coord_to_key(x, y)]

        for neighbour in t_cell['children']:
            n_x, n_y = key_to_coord(neighbour)
            n_z = z * 1
            if abs(x - n_x) > 1 or abs(y - n_y) > 1:  # step greater than 1 mean portal used
                n_z += t_cell['level']
                # if n_z % 1000 == 0:
                print("Jump to level: ", n_z, " - ", neighbour, " - ", len(queue), " - ", len(visited))

            n_key = coord_to_key_level(n_x, n_y, n_z)

            if n_z >= 0 and n_key not in visited:
                visited.add(n_key)
                queue.append(n_key)
                t_parents[n_key] = c_key
    return t_parents


# Starting from the end cell work backwards to find the optimal path to end
def get_route_from_parents(i_parents, end):
    t_route = [end]
    while end in i_parents:
        end = i_parents[end]
        t_route.append(end)
    return t_route[::-1]


def print_maze(i_cells, max_x, max_y):
    s_maze = ""

    for y in range(max_y):
        for x in range(max_x):
            if coord_to_key(x, y) in i_cells:
                cell = i_cells[coord_to_key(x, y)]
                if "level" in cell:
                    s_maze += "+"
                else:
                    s_maze += "."
            else:
                s_maze += '#'
        s_maze += "\n"
    print(s_maze)


fileName = "input20t3.txt"
infile = open(fileName, 'r')
maze = [line.rstrip() for line in infile.readlines()]
cells, portals = parse_input_lines(maze)
cells = build_graph(cells, portals, len(maze[0]), len(maze))

print_maze(cells, len(maze[4]), len(maze))

parents = bfs_recursive(cells, portals['AA'][0] + ",0", portals['ZZ'][0] + ",0")
route = get_route_from_parents(parents, portals['ZZ'][0] + ",0")

print(len(route) - 1)
