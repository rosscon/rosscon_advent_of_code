# Read in input file line by line
fileName="input01.txt"

infile = open(fileName, 'r')
numbers = [int(line) for line in infile.readlines()]

target=2020
multiplied = -1

for num1 in numbers:
    for num2 in numbers:
        added = num1 + num2
        print (num1, " + ", num2, " = ", + added)
        if added == target:
            multiplied = num1 * num2
            print (num1, " * ", num2, " = ", multiplied)
            break

    if multiplied > 0:
        break

if multiplied == -1:
    print("No solution found")