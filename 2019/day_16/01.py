

def build_patterns ( basePattern, length ):
    patterns = { 1: basePattern }

    for i in range(2, length + 1):
        tmpPattern = []
        for d in basePattern:
            for j in range(i):
                tmpPattern.append(d)
        patterns[i] = tmpPattern

    return patterns

def execute_phase ( patterns, signal ):
    newSignal = []

    for i in range(len(signal)):
        pattern = patterns[i + 1]
        tot = 0

        for j in range(len(signal)):
            p = pattern[(j + 1) % len(pattern)]
            tot += signal[j] * p

        newSignal.append(int(str(tot)[-1]))

    return newSignal





fileName = "input16.txt"
infile = open(fileName, 'r')
signal = [int(c) for c in infile.read().rstrip()]
#signal = [int(c) for c in "80871224585914546619083218645595"]
#signal = [int(c) for c in "19617804207202209144916044189917"]
#signal = [int(c) for c in "69317163492948606335995924319873"]
#signal = [int(c) for c in "12345678"]

basePattern = [0, 1, 0, -1]

patterns = build_patterns(basePattern, len(signal))


print ("Input signal: ", ''.join(str(e) for e in signal))

numPhases = 100
count = 0

while count < numPhases:
    count += 1

    signal = execute_phase(patterns, signal)

    print ("After phase {}: {}".format(count, ''.join(str(e) for e in signal[:20])))


print ("After all phases: ", ''.join(str(e) for e in signal[:8]))

