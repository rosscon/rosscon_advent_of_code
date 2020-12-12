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


for i in range(preamble, len(numbers)):
    if not number_is_valid(numbers, preamble, i):
        print (numbers[i])