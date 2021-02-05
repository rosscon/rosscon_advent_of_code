# Global Consts
neighbours = [[-1, 0], [1, 0], [0, -1], [0, 1]]


def coord_to_key(x, y):
    return "{0},{1}".format(x, y)


def key_to_cood(i_key):
    return int(i_key.split(',')[0]), int(i_key.split(',')[1])


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
                    portal = {'id': portal_id}
                    #l_cells[key] = portal
                    if portal_id not in l_portals.keys():
                        l_portals[portal_id] = []
                    l_portals[portal_id].append(key)

    return l_cells, l_portals


# Builds a graph structure from the parsed input
def build_graph(i_cells, i_portals):
    # Link cells that share a portal
    for p_key, portal in i_portals.items():
        if len(portal) > 1:  # Need to avoid the entry/exit portals
            i_cells[portal[0]]['children'] = [portal[1]]
            i_cells[portal[1]]['children'] = [portal[0]]

    # Link Cells to each other
    for c_key, cell in i_cells.items():
        x, y = key_to_cood(c_key)
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
def bfs(i_cells, start):
    visited = {start}
    queue = [start]

    while queue:
        c_key = queue.pop(0)
        t_cell = i_cells[c_key]
        for neighbour in t_cell['children']:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
                i_cells[neighbour]['parent'] = c_key
    return i_cells


# Starting from the end cell work backwards to find the optimal path to end
def get_route(i_cells, end):
    cell = i_cells[end]
    t_route = [end]

    while 'parent' in cell:
        t_route.append(cell['parent'])
        cell = i_cells[cell['parent']]

    return t_route[::-1]


fileName = "input20.txt"
infile = open(fileName, 'r')
maze = [line.rstrip() for line in infile.readlines()]
cells, portals = parse_input_lines(maze)
cells = build_graph(cells, portals)
cells = bfs(cells, portals['AA'][0])
route = get_route(cells, portals['ZZ'][0])

print(len(route) - 1)
