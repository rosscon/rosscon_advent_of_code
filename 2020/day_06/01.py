# Read in input file line by line
_fileName = "input06.txt"

lines = ""

with open(_fileName) as file:
    lines = file.read()

customsForms = lines.split("\n\n")

def group_to_questions_answered(group):
    lines = group.split("\n")

    questions = {}

    for line in lines:
        for q in line:
            questions[q] = 1

    return questions


questions = []
sumOfCounts = 0;

for form in customsForms:
    questions.append(group_to_questions_answered(form))

for question in questions:
    sumOfCounts += len(question)

print ("Sum of question counts : ", sumOfCounts)