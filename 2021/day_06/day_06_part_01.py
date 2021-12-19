#
# Parse the puzzle input
#
import sys

fileName = "input.txt"

infile = open(fileName, 'r')
input_data = [int(x) for x in infile.read().strip().split(',')]

NEW_FISH_VAL = 8
FISH_RESET_VAL = 6

DAYS = 80

fish_data = input_data

for d in range(DAYS):
    new_fish_data = []
    new_fish_count = 0

    for fish in fish_data:
        if fish == 0:
            fish = FISH_RESET_VAL
            new_fish_count = new_fish_count + 1
        else:
            fish = fish - 1

        new_fish_data.append(fish)

    for n in range(new_fish_count):
        new_fish_data.append(NEW_FISH_VAL)

    fish_data = new_fish_data

    print("Day: " + str(d + 1) + "\tFish: " + str(len(fish_data)))




