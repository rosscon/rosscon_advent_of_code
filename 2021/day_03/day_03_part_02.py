fileName = "input.txt"

infile = open(fileName, 'r')
binary_array = [line.strip() for line in infile.readlines()]
o2_array = [[char for char in row] for row in binary_array]
co_array = [[char for char in row] for row in binary_array]

number_length = len(binary_array[0])

for i in range(number_length):
    print(i)
    if len(o2_array) > 1:
        ones = len([x for x in o2_array if x[i] == '1'])
        zeros = len([x for x in o2_array if x[i] == '0'])
        most_common = '1' if (ones >= zeros) else '0'
        o2_array = [x for x in o2_array if x[i] == most_common]

    if len(co_array) > 1:
        ones = len([x for x in co_array if x[i] == '1'])
        zeros = len([x for x in co_array if x[i] == '0'])
        least_common = '0' if (zeros <= ones) else '1'
        co_array = [x for x in co_array if x[i] == least_common]

o2 = int(''.join(o2_array[0]), 2)
co = int(''.join(co_array[0]), 2)

print("O2: " + str(o2))
print("C0: " + str(co))

result = o2 * co
print("result:" + str(result))

