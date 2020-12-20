
def parse_rules(lines):
    rules = {}

    for line in lines:
        key = line.split(': ')[0]
        rules[key] = []

        for rs in line.split(': ')[1].split(' | '):
            rules[key].append(rs.split(' '))



    return rules



def rule_matches(message, ruleId, rules, index):

    if index >= len(message): return -1

    rule = rules[ruleId]
    #print ("Checking: {}\tindex: {}".format(rule, index))


    for r in rule:

        #print('r: ', r)

        checkIndex = index

        for v in r:
            if v.isdigit():
                #print('KEY: ', v)
                checkIndex = rule_matches(message, v, rules, checkIndex)
                if checkIndex == -1:
                    break

            else:
                #print('VALUE: ', v, ' : ', checkIndex, message[checkIndex])
                if message[checkIndex] == v[1]:
                    #print('MATCH')
                    return (checkIndex + 1)
                else:
                    #print('NO-MATCH')
                    return -1


        if checkIndex != -1:
            return checkIndex

    return -1




_fileName = "input19.txt"
lines = ""

with open(_fileName) as file:
    lines = file.read()

rules = lines.split("\n\n")[0].split("\n")
messages = lines.split("\n\n")[1].rstrip().split("\n")


rules = parse_rules(rules)

validCount = 0
invalidCount = 0

for message in messages:

    matchLen = rule_matches(message, '0', rules, 0)

    if matchLen == len(message):
        print (message, ' : Valid')
        validCount += 1
    else:
        print (message, ' : Invalid')
        invalidCount += 1

print ("\nValid: {}\tInvalid: {}".format(validCount, invalidCount))




