#
# Parse the puzzle input
#
import sys

fileName = "input.txt"

infile = open(fileName, 'r')
input_data = [int(x) for x in infile.read().strip().split(',')]

NEW_FISH_VAL = 8
FISH_RESET_VAL = 6

DAYS = 256

# Setup initial state
state_counts = {
}

for i in range(NEW_FISH_VAL + 2):
    state_counts[i] = 0

for fish in input_data:
    if fish not in state_counts:
        state_counts[fish] = 0
    state_counts[fish] = state_counts[fish] + 1

for d in range(DAYS):

    # add new fish for zeros
    state_counts[NEW_FISH_VAL + 1] = state_counts[0]

    # move zero count fish to reset day + 1
    state_counts[FISH_RESET_VAL + 1] = state_counts[FISH_RESET_VAL + 1] + state_counts[0]

    #move each value down one
    for i in range(NEW_FISH_VAL + 1):
        state_counts[i] = state_counts[i + 1]


    total = 0
    for i in range(NEW_FISH_VAL + 1):
        total += state_counts[i]

    print("Day: " + str(d + 1) + "\tFish: " + str(total))




