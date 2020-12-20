
def parse_rules(lines):
    rules = {}

    for line in lines:
        key = line.split(': ')[0]
        rules[key] = []

        for rs in line.split(': ')[1].split(' | '):
            rules[key].append(rs.split(' '))



    return rules



def rule_matches(message, sequence):

    if ( len(message) == 0 or len(sequence) == 0 ):
        if len(message) == 0 and len(sequence) == 0:
            return True
        else:
            return False

    #print(sequence[0])
    rule = rules[sequence[0]]


    if '"' in rule[0][0]:
        #print(rule[0][0], " - ", message[0])
        if rule[0][0][1] == message[0]:
            #print(rule[0][0], " matches ", message[0])
            return rule_matches(message[1:], sequence[1:])
        else:
            return False
    else:
        for t in rule:
            if(rule_matches(message, t + sequence[1:])) : return True

    #return False



_fileName = "input19p2.txt"
lines = ""

with open(_fileName) as file:
    lines = file.read()

rules = lines.split("\n\n")[0].split("\n")
messages = lines.split("\n\n")[1].rstrip().split("\n")


rules = parse_rules(rules)

validCount = 0
invalidCount = 0

#for message in messages[10:12]:
for message in messages:

    matches = rule_matches(message, ['0'])

    if matches:
        print (message, ' : Valid ', matchLen)
        validCount += 1
    else:
        print (message, ' : Invalid ', matchLen)
        invalidCount += 1

print ("\nValid: {}\tInvalid: {}".format(validCount, invalidCount))




