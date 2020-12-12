# Read in input file line by line
_fileName="input10.txt"

infile = open(_fileName, 'r')
adaptors = [int(line) for line in infile.readlines()]


def find_differences(adaptors):
    differences = {};

    for i in range(1, len(adaptors)):
        diff = adaptors[i] - adaptors[i-1]
        diff = str(diff)

        if diff in differences:
            differences[diff] += 1
        else:
            differences[diff] = 1

    return differences



adaptors.append(0) #Source
adaptors.sort()
adaptors.append(adaptors[-1] + 3) #device

differences = find_differences(adaptors)
answer = differences["1"] * differences["3"]
print(answer)