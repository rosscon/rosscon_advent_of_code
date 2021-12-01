fileName = "input.txt"

infile = open(fileName, 'r')
numbers = [int(line) for line in infile.readlines()]

current_number = numbers[0]

increases = 0

for number in numbers:
    if number > current_number:
        increases += 1

    current_number = number

print(increases)
