


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






_fileName = "input18.txt"

#Parse input file
infile = open(_fileName, 'r')
rows = [line.rstrip() for line in infile.readlines()]

testRows = [
        '2 * 3 + (4 * 5)',
        '5 + (8 * 3 + 9 + 3 * 4 * 3)',
        '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))',
        '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2',
        ]


total = 0;
for row in rows:
    exAnswer = solve_expression(row)
    total += exAnswer
    print (row, ' = ', exAnswer)
    print()

print ('Total: ', total)



