fileName = "input.txt"

infile = open(fileName, 'r')
binary_array = [line.strip() for line in infile.readlines()]
binary_array = [[char for char in row] for row in binary_array]

sum_array = []

for binary_num in binary_array:
    for i in range(len(binary_num)):
        if len(sum_array) < (i + 1):
            sum_array.append(0)

        if binary_num[i] == '1':
            sum_array[i] += 1
        else:
            sum_array[i] -= 1

gamma_array = ['1' if (x > 0) else '0' for x in sum_array]
epsilon_array = ['1' if (x <= 0) else '0' for x in sum_array]

gamma = int(''.join(gamma_array), 2)
epsilon = int(''.join(epsilon_array), 2)

print("gamma: " + str(gamma))
print("epsilon: " + str(epsilon))

result = gamma * epsilon
print("result:" + str(result))

