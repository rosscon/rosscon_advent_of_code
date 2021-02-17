###########################################
# Deal into new stack
# Essentially reverses the deck order
###########################################
def deal_into_new_stack(input_deck):
    return input_deck[::-1]


###########################################
# Cut the deck,
# Take top N cards for +n
# Take bottom N cards for -n
###########################################
def cut_deck(input_deck, input_n):
    new_deck = []

    if input_n == 0:
        return input_deck
    elif input_n > 0:
        top = input_deck[:input_n]
        bottom = input_deck[input_n:]
    else:
        top = input_deck[:input_n]
        bottom = input_deck[input_n:]

    new_deck.extend(bottom)
    new_deck.extend(top)

    return new_deck


###########################################
# Deal with increment
# Start with empty array,
# Deal top card to first element,
# Move n places then deal next card there,
#   If pass end of array wrap around
###########################################
def deal_with_increment(input_deck, input_n):
    new_deck = [-1] * len(input_deck)
    index = 0

    for card in input_deck:
        new_deck[index] = card
        index += input_n
        if index >= len(new_deck):
            index -= len(new_deck)

    return new_deck


###########################################
# Find the index of the card
###########################################
def find_card(input_deck, card):
    return input_deck.index(card)


###########################################
# Build the deck of cards
###########################################
numberOfCards = 10007
deck = []

for i in range(numberOfCards):
    deck.append(i)

###########################################
# Load instructions from file
###########################################
instructionsFile = "input22.txt"
lines = [line.strip() for line in open(instructionsFile, 'r').readlines()]

###########################################
# Execute instructions
###########################################
for line in lines:
    if "deal into new stack" in line:
        deck = deal_into_new_stack(deck)
    elif "cut" in line:
        n = int(line[3:])
        deck = cut_deck(deck, n)
    elif "deal with increment" in line:
        n = int(line[19:])
        deck = deal_with_increment(deck, n)

print(deck)
print(find_card(deck, 2019))
