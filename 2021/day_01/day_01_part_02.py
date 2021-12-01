fileName = "input.txt"

infile = open(fileName, 'r')
numbers = [int(line) for line in infile.readlines()]

current_window = [numbers[0], numbers[1], numbers[2]]

increases = 0

for number in numbers[3:]:
    new_window = current_window[1:] + [number]
    current_window_total = current_window[0] + current_window[1] + current_window[2]
    new_window_total = new_window[0] + new_window[1] + new_window[2]
    current_window = new_window

    if new_window_total > current_window_total:
        increases += 1

print(increases)
