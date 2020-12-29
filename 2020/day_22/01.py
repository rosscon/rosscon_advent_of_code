

def parse_decks(inDecks):

    decks = {}

    for d in inDecks:
        splitDeck = d.split('\n')
        player = splitDeck[0]
        cards = [int(c) for c in splitDeck[1:]]
        decks[player] = cards

    return decks


def play_round(decks, players):

    p1Card = decks[players[0]].pop(0)
    p2Card = decks[players[1]].pop(0)

    if p1Card > p2Card:
        decks[players[0]].extend([p1Card, p2Card])
    elif p2Card > p1Card:
        decks[players[1]].extend([p2Card, p1Card])
    else:
        print('ERROR')

    return decks

def calculate_score(deck):
    score = 0

    for i in range(len(deck)):
        pos = i + 1
        cVal = deck[::-1][i]

        score += (pos * cVal)

    return score




_fileName = "input22.txt"
lines = ""
_players = ['Player 1:', 'Player 2:']

with open(_fileName) as file:
    lines = file.read().rstrip()

decks = lines.split("\n\n")
decks = parse_decks(decks)


rounds = 1


while len(decks[_players[0]]) > 0 and len(decks[_players[1]]) > 0:

    print("-- Round {} --".format(rounds))
    for p in _players:
        print("{} - {}".format(p, decks[p]))

    decks = play_round(decks, _players)

    rounds +=1
    print()

print("-- End --")
for p in _players:
    print("{} - {}\n\tScore: {}".format(p, decks[p], calculate_score(decks[p])))