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
#numberOfCards = 10007
#deck = []
#
#for i in range(numberOfCards):
#    deck.append(i)

###########################################
# Load instructions from file
###########################################
instructionsFile = "input22.txt"
lines = [line.strip() for line in open(instructionsFile, 'r').readlines()]


###########################################
# modpow :(ax+b)^m % n
# f(x) = ax+b
# g(x) = cx+d
# f^2(x) = a(ax+b)+b = aax + ab+b
# f(g(x)) = a(cx+d)+b = acx + ad+b
# https://github.com/metalim/metalim.adventofcode.2019.python/blob/master/22_cards_shuffle.ipynb
###########################################
def polypow(in_a, in_b, in_m, in_n):
    if in_m == 0:
        return 1, 0
    if in_m % 2 == 0:
        return polypow(in_a * in_a % in_n, (in_a * in_b + in_b) % in_n, in_m // 2, in_n)
    else:
        c, d = polypow(in_a, in_b, in_m - 1, in_n)
        return in_a * c % in_n, (in_a * d + in_b) % in_n


###########################################
# Execute instructions
# For part 2 it is apparent that this
# cannot be brute forced. instead need to
# use linear polynomials to solve
# first need to convert the rules into a
# a linear polynomial, stepping through the
# instructions in reverse order.
###########################################
numberOfCards = 119315717514047
position = 2020
shuffles = 101741582076661

a, b = 1, 0
for line in lines[::-1]:
    if "deal into new stack" in line:
        a = -a
        b = numberOfCards - b - 1
    elif "cut" in line:
        n = int(line[3:])
        b = (b + n) % numberOfCards
    elif "deal with increment" in line:
        n = int(line[19:])
        z = pow(n, numberOfCards - 2, numberOfCards)
        a = a * z % numberOfCards
        b = b * z % numberOfCards

a, b = polypow(a, b, shuffles, numberOfCards)
answer = (position * a + b) % numberOfCards
print(answer)
