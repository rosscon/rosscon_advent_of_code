# Read in input file line by line
fileName="input01.txt"

infile = open(fileName, 'r')
numbers = [int(line) for line in infile.readlines()]

#For optimisation, start with smallest, when greater than target break
numbers.sort()

target=2020
multiplied = -1

#Brute forcing to power of 3 will take a long time without optimisation
for num1 in numbers:
    for num2 in numbers:
        for num3 in numbers:
            added = num1 + num2 + num3
            print (num1, " + ", num2, " + ", num3, " = ", + added)
            if added == target:
                multiplied = num1 * num2 * num3
                print (num1, " * ", num2, " * ", num3, " = ", multiplied)
                break
            if added > target:
                #as list of numbers is sorted low to high remianing answers will also be > target
                break

        if multiplied > 0:
            break

    if multiplied > 0:
        break

if multiplied == -1:
    print("No solution found")

