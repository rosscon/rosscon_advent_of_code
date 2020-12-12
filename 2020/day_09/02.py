# Read in input file line by line
_fileName="input09.txt"

infile = open(_fileName, 'r')
numbers = [int(line) for line in infile.readlines()]
preamble = 25

def number_is_valid(numbers, preamble, index):

    for j in range(index - preamble, index):
        for k in range (index - preamble, index):
            if j != k:
                if numbers[index] == (numbers[j] + numbers[k]):
                    return True

    return False


def sum_array(array):
    total = 0

    for item in array:
        total += item

    return total


def find_contiguois_range(numbers, number):
    cRange = [0,0]

    for j in range(len(numbers)):
        #print(j)
        for k in range(j, len(numbers)):
            tmpC = numbers[j:k]
            tmpSum = sum_array(tmpC)
            if tmpSum == number:
                return tmpC
            elif tmpSum > number:
                continue

    return cRange



weakNumber = -1

for i in range(preamble, len(numbers)):
    if not number_is_valid(numbers, preamble, i):
        weakNumber = numbers[i]
        break

cRange = find_contiguois_range(numbers, weakNumber)
cRange.sort()
answer = cRange[0] + cRange[-1]
total = sum_array(cRange)