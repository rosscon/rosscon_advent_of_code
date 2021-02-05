def get_neighbours(i_center):
    return [
        (i_center[0] + 1, i_center[1]),
        (i_center[0], i_center[1] - 1),
        (i_center[0] - 1, i_center[1]),
        (i_center[0], i_center[1] + 1)
    ]


def parse_input_lines(i_lines):
    height = len(i_lines)
    t_cells, t_portals = set(), {}
    for i in range(height):
        width = len(i_lines[i])
        for j in range(width):
            if i_lines[i][j] == '.':
                t_cells.add((i, j))
            elif i_lines[i][j].isupper():
                if i < height - 1 and j < len(i_lines[i + 1]) and i_lines[i + 1][j].isupper():
                    t = (i - 1, j) if i_lines[i - 1][j] == '.' else (i + 2, j)
                    if i_lines[i][j] + i_lines[i + 1][j] in t_portals:
                        t_portals[i_lines[i][j] + i_lines[i + 1][j]].append(t)
                    else:
                        t_portals[i_lines[i][j] + i_lines[i + 1][j]] = [t]
                elif j < width - 1 and i_lines[i][j + 1].isupper():
                    t = (i, j - 1) if i_lines[i][j - 1] == '.' else (i, j + 2)
                    if i_lines[i][j] + i_lines[i][j + 1] in t_portals:
                        t_portals[i_lines[i][j] + i_lines[i][j + 1]].append(t)
                    else:
                        t_portals[i_lines[i][j] + i_lines[i][j + 1]] = [t]
    return t_cells, t_portals


# Builds a graph structure from the parsed input
def build_graph(i_cells, i_portals, i_maze):
    height, width = len(i_maze), len(i_maze[0])
    t_graph = {}
    for cell in i_cells:
        neigh = []
        for x in get_neighbours(cell):
            if x in i_cells:
                neigh.append((x, 0))
        for portal in i_portals.values():
            if len(portal) == 2 and cell in portal:
                if cell[0] in [2, height - 3] or cell[1] in [2, width - 3]:
                    neigh.append((portal[(portal.index(cell) + 1) % 2], -1))
                else:
                    neigh.append((portal[(portal.index(cell) + 1) % 2], 1))
        t_graph[cell] = neigh
    return t_graph


# Perform a breadth first search on the graph of connected cells
# changed from part 1 to use tuples and keep track of step count in tuple
def bfs(i_graph, start, end):
    queue = [(start, 0, 0)]
    visited = set([(start, 0)])
    while queue:
        v = queue.pop(0)
        if v[0] == end and v[1] == 0:
            return v[2]
        for n in i_graph[v[0]]:
            if v[1] + n[1] < 0:
                continue
            if (n[0], v[1] + n[1]) not in visited:
                queue.append((n[0], v[1] + n[1], v[2] + 1))
                visited.add((n[0], v[1] + n[1]))


fileName = "input20.txt"
maze = open(fileName).read().split('\n')[:-1]
cells, portals = parse_input_lines(maze)
graph = build_graph(cells, portals, maze)
steps = bfs(graph, portals['AA'][0], portals['ZZ'][0])

print(steps)
