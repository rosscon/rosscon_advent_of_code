#Setting up the input

startingNumbers = "0,14,6,20,1,4"
lastNumber = 30000000

#Chanfed to using a dictionary of when each number was last spoken to improve speed

numbersSpokenDict = {
        0 : 0,
        14 : 1,
        6 : 2,
        20 : 3,
        1 : 4,
        }

lastSpokenNumber = 4

for turn in range(5, (lastNumber - 1)):

    tmpLastSpokenNumber = lastSpokenNumber

    if not tmpLastSpokenNumber in numbersSpokenDict:
        lastSpokenNumber = 0
    else:
        lastSpokenNumber = turn - numbersSpokenDict[lastSpokenNumber]

    numbersSpokenDict[tmpLastSpokenNumber] = turn

print ('Final number:', lastSpokenNumber)