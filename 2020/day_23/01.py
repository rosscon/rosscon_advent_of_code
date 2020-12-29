# -*- coding: utf-8 -*-


#cupsState = [3, 8, 9, 1, 2, 5, 4, 6, 7]
cupsState = [3, 1, 8, 9, 4, 6, 5, 7, 2]
maxCup = 9

moves = 100
pickCups = 3

currentCupIndex = 0

for i in range(moves):

    print("-- Move {} --".format(i + 1))
    for cup in cupsState:
        print(cup, " ", end = '')
    print()
    for m in range(currentCupIndex):
        print("   ", end = '')
    print ("^")


    # Pick cups
    pickup = []
    for j in range (pickCups):
        if (currentCupIndex + 1) < len(cupsState):
            pickup.append(cupsState.pop(currentCupIndex + 1))
        else:
            pickup.append(cupsState.pop(0))
            currentCupIndex -= 1

    print("Pick up : ", end = '')
    for cup in pickup:
        print(cup, " ", end = '')
    print()


    # Find destination index
    cupVal = cupsState[currentCupIndex] - 1
    destIndex = -1
    while destIndex == -1:
        try:
            index = cupsState.index(cupVal)
            destIndex = index
        except:
            cupVal -= 1
            if cupVal <= 0:
                cupVal = maxCup
            destIndex = - 1
    print("Destination: ", cupVal)

    # Insert at destination
    if (destIndex + 1) < len(cupsState):
        cupsState = cupsState[:destIndex + 1] + pickup + cupsState[destIndex + 1:]
    else:
        cupsState = cupsState[:destIndex + 1] + pickup

    if destIndex < currentCupIndex:
        currentCupIndex += pickCups

    currentCupIndex += 1
    if currentCupIndex >= len(cupsState):
        currentCupIndex = 0

    print()

print("-- Final {} --".format(i + 1))
for cup in cupsState:
    print(cup, " ", end = '')
print()
for m in range(currentCupIndex):
    print("   ", end = '')
print ("^")