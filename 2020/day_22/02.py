import copy

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


def play_round_recursive(decks, players, gameId, rounds):

    p1Card = decks[players[0]].pop(0)
    p2Card = decks[players[1]].pop(0)

    if len(decks[players[0]]) >= p1Card and len(decks[players[1]]) >= p2Card:

        tmpDecks = copy.deepcopy(decks)
        tmpDecks[players[0]] = tmpDecks[players[0]][:p1Card]
        tmpDecks[players[1]] = tmpDecks[players[1]][:p2Card]

        outcome = play_game_recursive(tmpDecks, players, gameId = ("{}.{}".format(gameId,rounds)))

        if len(outcome[players[0]]) == 0:
            decks[players[1]].extend([p2Card, p1Card])
        elif len(outcome[players[1]]) == 0:
            decks[players[0]].extend([p1Card, p2Card])
        else:
            print('ERROR')

    else:
        if p1Card > p2Card:
            decks[players[0]].extend([p1Card, p2Card])
        elif p2Card > p1Card:
            decks[players[1]].extend([p2Card, p1Card])
        else:
            print('ERROR')

    return decks


def play_game_recursive(decks, players, gameId = '1'):

    print ("=== Game {} ===".format(gameId))

    rounds = 1
    history = {str(decks) : 1}

    while len(decks[players[0]]) > 0 and len(decks[players[1]]) > 0:

        #print("-- Game{} - Round {} --".format(gameId, rounds))
        #for p in _players:
        #    print("{} - {}".format(p, decks[p]))

        decks = play_round_recursive(decks, players, gameId, rounds)

        if str(decks) in history:
            print("Infinite Loop")
            decks[players[1]] = []
            return decks
        else:
            history[str(decks)] = 1

        rounds +=1
        #print()

    return decks



_fileName = "input22.txt"
lines = ""
_players = ['Player 1:', 'Player 2:']

with open(_fileName) as file:
    lines = file.read().rstrip()

decks = lines.split("\n\n")
decks = parse_decks(decks)


decks = play_game_recursive(decks, _players)

print("-- End --")
for p in _players:
    print("{} - {}\n\tScore: {}".format(p, decks[p], calculate_score(decks[p])))