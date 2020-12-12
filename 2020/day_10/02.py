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


def find_sequences_of_gaps(adaptors, gapSize = 1):
    gapCounts = {}

    currentSequenceCount = 0

    for i in range(1, len(adaptors)):
        diff = adaptors[i] - adaptors[i-1]

        if diff > gapSize:

            if currentSequenceCount in gapCounts:
                gapCounts[currentSequenceCount] += 1
            else:
                gapCounts[currentSequenceCount] = 1

            currentSequenceCount = 0
        else:
           currentSequenceCount += 1

    return gapCounts

    #return arrangements

# Brute forcing will take too long even recursively so need to
# solve matematically, follows tribonacci sequence 0, 0, 1, 1, 2, 4, 7, 13, 24
# Groups of gap 1 in a row [. = gap, * = adaptor]
# 2 in a row can have 2 combinations
#   .*
#   *.
#
# 3 in a row can have 4 combinations
#   **.
#   .*.
#   *.*
#   .**
# 4 in a row can have 7 combinations
#   ***.
#   **.*
#   *.**
#   .***
#   *.*.
#   .*.*
#   *..*
#
# Formula 7^(num 4 1's in row) * 4^(num 3 1's in row) * 2^(num 2 1's in row)


adaptors.append(0) #Source
adaptors.sort()
adaptors.append(adaptors[-1] + 3) #device

differences = find_differences(adaptors)
sequenceGaps = find_sequences_of_gaps(adaptors)

answer = pow(7, sequenceGaps[4]) * pow(4, sequenceGaps[3]) * pow(2, sequenceGaps[2])

