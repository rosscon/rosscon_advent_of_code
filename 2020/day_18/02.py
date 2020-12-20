import re


# Given an index of a char in string, fonds the index of the coresponding
# closing bracket
def find_closing_bracket_index(expression, openIndex):

    unresolvedBrackets = 1
    index = openIndex + 1

    while unresolvedBrackets != 0:

        if index >= len(expression):
            print('No closing bracket found within expression')
            return -1

        if expression[index] == '(':
            unresolvedBrackets += 1
        elif expression[index] == ')':
            unresolvedBrackets -= 1

        index += 1

    return index


def find_opening_bracket_index(expression, closeIndex):

    unresolvedBrackets = 1
    index = closeIndex - 1

    while unresolvedBrackets != 0:

        if index <0:
            print('No closing bracket found within expression')
            return -1

        if expression[index] == ')':
            unresolvedBrackets += 1
        elif expression[index] == '(':
            unresolvedBrackets -= 1

        index -= 1

    return index


def perform_operator(a, b, operator):

    answer = -1

    if operator == '*':
        answer = a * b
    elif operator == '+':
        answer = a + b
    else:
        print ('Unexpected operator: ', operator)

    #print("op: {} {} {} = {}".format(a, operator, b, answer))
    return answer;


def solve_expression(expression):

    #print ('expression: ', expression)

    expressionLength = len(expression)
    currentChar = 0

    answer = 0
    operator = '+'

    while currentChar < expressionLength:
        if expression[currentChar] == ' ':
            #print ('space')
            currentChar += 1

        elif expression[currentChar].isdigit():
            #print ('digit: ', expression[currentChar])
            answer = perform_operator(answer, int(expression[currentChar]), operator)
            currentChar += 1

        elif expression[currentChar] == '(':
            #print ('bracket: ', expression[currentChar])
            closing = find_closing_bracket_index(expression, currentChar)
            #print ('sub: ', expression[currentChar + 1: closing])
            subAnswer = solve_expression(expression[currentChar + 1: closing - 1])
            answer = perform_operator(answer, subAnswer, operator)
            currentChar = closing + 1

        elif expression[currentChar] in ['+', '*']:
            #print ('operator: ', expression[currentChar])
            operator = expression[currentChar]
            currentChar += 1

        else:
            print ('unexpected char: ', expression[currentChar])
            return "ERROR"

    return answer


def solve_addition (addition):
    a = int(addition.split(' + ')[0])
    b = int(addition.split(' + ')[1])
    return a + b

def solve_multiplication (multiplication):
    a = int(multiplication.split(' * ')[0])
    b = int(multiplication.split(' * ')[1])
    return a * b


def solve_addition_first (expression):

    expressionChanged = True

    expression = '(' + expression +')'

    while expressionChanged:
        expressionChanged = False

        # Extract isolated results in brackets e.g. (9)
        while re.search(r'\([0-9]+\)', expression) != None:
            #print ('Reduce Bracket:')
            match = list(re.search(r'\([0-9]+\)', expression).span())
            #print (expression[match[0]:match[1]])
            r = expression[match[0] + 1 :match[1] - 1]
            expression = expression[:match[0]] + str(r) + expression[match[1]:]
            expressionChanged = True
            #print (expression)

        # Do standalone additions
        while re.search(r'[0-9]+.\+.[0-9]+', expression) != None:
            #print ('Reduce Addition')
            match = list(re.search(r'[0-9]+.\+.[0-9]+', expression).span())
            #print (expression[match[0]:match[1]])
            r = solve_addition(expression[match[0]:match[1]])
            expression = expression[:match[0]] + str(r) + expression[match[1]:]
            expressionChanged = True
            #print (expression)

        # Do Standalone multiplications
        while re.search(r'\([0-9]+.\*.[0-9]+[\ \)](?!\+)', expression) != None:
            #print ('Reduce Multiplication')
            match = list(re.search(r'\([0-9]+.\*.[0-9]+[\ \)](?!\+)', expression).span())
            #print (expression[match[0] + 1 : match[1] - 1])
            r = solve_multiplication(expression[match[0] + 1:match[1] - 1])
            expression = expression[:match[0] + 1] + str(r) + expression[match[1] - 1:]
            expressionChanged = True
            #print (expression)
            break

    return int(expression)



_fileName = "input18.txt"

#Parse input file
infile = open(_fileName, 'r')
rows = [line.rstrip() for line in infile.readlines()]

testRows = [
        '1 + 2 * 3 + 4 * 5 + 6',
        #'1 + (2 * 3) + (4 * (5 + 6))',
        #'2 * 3 + (4 * 5)',
        #'5 + (8 * 3 + 9 + 3 * 4 * 3)',
        #'5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))',
        #'(5) * ((9) * (((7) * (3) * ((3 + 9) * (3 + ((8 + 6) * (4)))))))',
        #'((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2',
        #'(((((2 + 4) * (9))) * (((6 + 9) * (8 + 6))) + 6) + 2 + 4) * (2)',
        #'((((((2 + 4) * 9) * ((6 + 9) * (8 + 6))) + 6) + 2) + 4) * 2'
        #'(5 + 7) * 2 * 4 + 6 + 7 + (2 + 2 + 6 + (9 + 3 + 7 * 3))',
        #'1 * (4 + (4 + 5 + 4) * 7)',
        #'(4 * 8 + 2 * (7 + 6 + 7) * 2) + ((4 * 2 + 4) + (6 + 7 * 2 * 3) + 5 * 2) * (4 + (4 + 5 + 4) * 7 * 8 * 4 + (7 * 7 + 5 * 3 * 6)) + 8'
        #'1 + 2 * 3 + 4 * 5 + 6',
        #'1',
        '4 + 2 + 2 + 3 + (7 * 5 + 3 + 7 + (6 + 6 * 7))',
        ]



totalOrig = 0
totalAddFirstAns = 0

for row in rows:

    origAns = solve_expression(row)
    addFirstAns = solve_addition_first(row)
    wrapped = '[' + row + ']'

    totalOrig += origAns
    totalAddFirstAns += addFirstAns

    print ('{} = {}\n{} = {}'.format(row, origAns, row, addFirstAns))
    print()





print ('Original Total: {}\nAdd First Total: {}'.format(totalOrig, totalAddFirstAns))


