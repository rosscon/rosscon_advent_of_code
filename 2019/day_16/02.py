
def execute_phase ( signal ):
    suffix_sum = 0
    for i in range(len(signal)-1, -1, -1):
        signal[i] = suffix_sum = (suffix_sum + signal[i]) % 10

    return signal


def get_multiplier(position, offset):
    base_pattern = [0, 1, 0, -1]
    if offset < position:
        return base_pattern[0]
    offset -= position
    return base_pattern[(offset // (position+1) + 1) % len(base_pattern)]





fileName = "input16.txt"
infile = open(fileName, 'r')
signal = [int(c) for c in infile.read().rstrip()]*10000
#signal = [int(c) for c in "03036732577212944063491565474664" * 10000]
#signal = [int(c) for c in "02935109699940807407585447034323" * 10000]
#signal = [int(c) for c in "03081770884921959731165446850517" * 10000]
#signal = [int(c) for c in "12345678"]

offset = int(''.join(str(e) for e in signal[:7]))

basePattern = [0, 1, 0, -1]

print ("Input signal: ", ''.join(str(e) for e in signal[:90]))


numPhases = 100
count = 0
tmpSignal = signal[offset:]

while count < numPhases:
    count += 1

    tmpSignal = execute_phase( tmpSignal )

    print ("After phase {}: {}".format(count, ''.join(str(e) for e in tmpSignal[:90])))


print ("After all phases: ", ''.join(str(e) for e in tmpSignal[:90]))


message = tmpSignal[: 8]
print ("Message: ", ''.join(str(e) for e in message))

