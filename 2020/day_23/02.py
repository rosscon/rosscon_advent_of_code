# -*- coding: utf-8 -*-


#cupsState = [3, 8, 9, 1, 2, 5, 4, 6, 7]
cupsState = [3, 1, 8, 9, 4, 6, 5, 7, 2]

moves = 10000000
pickCups = 3



cupsDict = {} # Use a dictionary to update list order

# Expand the cup array

for i in range(10, 1000001):
    cupsState.append(i)

maxCup = cupsState [-1]
#maxCup = 9

previousCup = cupsState[-1]
for cup in cupsState:
    cupsDict[previousCup] = cup
    previousCup = cup

currentCup = cupsState[0]


for i in range(moves):


    """print("-- Move {} --".format(i + 1))
    tmpCurrentCup = cupsDict[currentCup]
    print(currentCup, " ", end = '')
    while tmpCurrentCup != currentCup:
        print(tmpCurrentCup, " ", end = '')
        tmpCurrentCup = cupsDict[tmpCurrentCup]
    print()"""


    # Pick cups
    pickup = []
    tmpCurrentCup = currentCup
    for j in range (pickCups):
        pickup.append(cupsDict[tmpCurrentCup])
        tmpCurrentCup = cupsDict[tmpCurrentCup]

    # Remove cups
    cupsDict[currentCup] = cupsDict[tmpCurrentCup]

    """print("Pick up : ", end = '')
    for cup in pickup:
        print(cup, " ", end = '')
    print()"""

    # Find Destination cup
    destination = currentCup - 1
    while destination in pickup:
        destination -= 1
        if destination <= 0 :
            destination = maxCup
    if destination <= 0 :
            destination = maxCup

    #print("Destination: ", destination)

    # Insert at destination
    cupsDict[pickup[-1]] = cupsDict[destination]
    cupsDict[destination] = pickup[0]

    currentCup = cupsDict[currentCup]

    """print()"""

pickup = []
tmpCurrentCup = 1
for j in range (2):
    pickup.append(cupsDict[tmpCurrentCup])
    tmpCurrentCup = cupsDict[tmpCurrentCup]

answer = pickup[0] * pickup[1]

print ('Answer: ', answer)


"""print("-- Final {} --".format(i + 1))
currentCup = 1
tmpCurrentCup = cupsDict[currentCup]
print(currentCup, " ", end = '')
while tmpCurrentCup != currentCup:
    print(tmpCurrentCup, " ", end = '')
    tmpCurrentCup = cupsDict[tmpCurrentCup]"""



