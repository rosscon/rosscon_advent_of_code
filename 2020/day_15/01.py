#Setting up the input

startingNumbers = "0,14,6,20,1,4"
lastNumber = 2020

numbersSpoken = [int(number) for number in startingNumbers.split(',')]

def get_number_age(numbersSpoken, number):

    age = 0

    for i in range(len(numbersSpoken) - 2, -1, -1):
        age += 1
        if(numbersSpoken[i]) == number:
            return age

    return 0


while len(numbersSpoken) < lastNumber:
    lastNumberSpoken = numbersSpoken[-1]
    numberAge = get_number_age(numbersSpoken, lastNumberSpoken)
    numbersSpoken.append(numberAge)

print ('Final number:', numbersSpoken[-1])