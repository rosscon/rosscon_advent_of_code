import pandas as pd
import shapely
from shapely.geometry import LineString, Point

_fileName="input03.txt"


def wire_to_coordinates(path, origin=[0,0]):
    coordinates=[[0,0]]
    for p in path:
        direction = p[0]
        length = int(p[1:])
        #print("Direction : ", direction, " Length: ", length)

        if direction == "U":
            coordinates.append([coordinates[-1][0],(coordinates[-1][1] + length)])
        elif direction == "D":
            coordinates.append([coordinates[-1][0],(coordinates[-1][1] - length)])
        elif direction == "L":
            coordinates.append([(coordinates[-1][0] - length), coordinates[-1][1]])
        elif direction == "R":
            coordinates.append([(coordinates[-1][0] + length), coordinates[-1][1]])

    return coordinates



def find_intersection(line1, line2):

    line1 = LineString(line1)
    line2 = LineString(line2)

    if line1.crosses(line2):
        intersection = line1.intersection(line2)
        return [int(intersection.x), int(intersection.y)]

    return False



def find_intersections(wire1Coordinates, wire2Coordinates):
    intersections = []

    previousW1Coordinate = [0,0]

    for w1Coordinate in wire1Coordinates:
        previousW2Coordinate = [0,0]

        for w2Coordinate in wire2Coordinates:
            w1 = [previousW1Coordinate, w1Coordinate]
            w2 = [previousW2Coordinate, w2Coordinate]

            intersection = find_intersection(w1, w2)

            if intersection != False:
                intersections.append(intersection)

            previousW2Coordinate = w2Coordinate

        previousW1Coordinate = w1Coordinate

    return intersections

def find_manhattan_distance(point1, point2):

    dx = abs(point1[0] - point2[0])
    dy = abs(point1[1] - point2[1])

    return dx + dy



wires = pd.read_csv(_fileName, sep=',', header=None)

wiresCoordinates = []

for index, row in wires.iterrows():
    wiresCoordinates.append(wire_to_coordinates(row))

intersections = find_intersections(wiresCoordinates[0], wiresCoordinates[1])
distances = []

for intersection in intersections:
    distances.append(find_manhattan_distance([0,0], intersection))

distances.sort()




