
# Perform a BFS to all reachable points from a given point
def bfs_from_point (point, maze):
    sx, sy = point
    visited = set([(sx, sy)])
    queue = [(sx, sy, 0, "")]
    routeinfo = {}

    for (x, y, dist, route) in queue:
        c = maze[y][x]
        if c not in ".@£&$#" and dist > 0:
            routeinfo[c] = (dist, route)
            route = route + c
        visited.add((x,y))

        for d in [(1,0),(0,1),(-1,0),(0,-1)]:
            newx, newy = x+d[0], y+d[1]
            if maze[newy][newx]!='#' and (newx,newy) not in visited:
                queue.append((newx,newy, dist+1, route))
    return routeinfo


# finds all possible routes from each key, door or start location
def find_routes (maze, keys):
    routes = {}

    for y in range(len(maze)):
        for x in range(len(maze[0])):
            cell = maze[y][x]
            if cell in keys or cell in '@£&$':
                routes[cell] = bfs_from_point ((x, y), maze)
    return routes


fileName = "input18_p2.txt"
infile = open(fileName, 'r')
maze = [l.rstrip() for l in infile.readlines()]
keys = [chr(c) for c in range(97, 123)]

routes = find_routes(maze, keys)
keys = [k for k in routes.keys() if k in keys]
info = {(('@', '£', '&', '$'),frozenset()):0}

for k in range(len(keys)):
    nextI = {}
    for item in info:
        currentLocations = item[0]
        currentKeys = item[1]
        currentDist = info[item]


        for newKey in keys:
            if newKey not in currentKeys:
                for robot in range(4):
                    if newKey in routes[currentLocations[robot]]:
                        dist, route = routes[currentLocations[robot]][newKey]
                        reachable = all((c in currentKeys or c.lower() in currentKeys) for c in route)

                        if reachable:

                            newDistance = currentDist + dist
                            newKeys = frozenset(currentKeys | set((newKey,)))
                            newLocations = list(currentLocations)
                            newLocations[robot] = newKey
                            newLocations = tuple(newLocations)

                            if (newLocations, newKeys) not in nextI or newDistance < nextI[(newLocations, newKeys)]:
                                nextI[(newLocations,newKeys)] = newDistance
    info = nextI
print("Best total distance:",min(info.values()))

# Thanks to https://repl.it/@joningram/AOC-2019#day18.py