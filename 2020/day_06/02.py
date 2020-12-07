# Read in input file line by line
_fileName = "input06.txt"

lines = ""

with open(_fileName) as file:
    lines = file.read()

customsForms = lines.split("\n\n")

def group_to_questions_all_answered(group):
    lines = group.strip().split("\n")

    questions = {}

    allAnsweredQuestions = []

    for line in lines:
        for q in line:
            if q in questions:
                questions[q] += 1
            else:
                questions[q] = 1

            if questions[q] == len(lines):
                allAnsweredQuestions.append(q)


    return allAnsweredQuestions



questions = []
sumOfCounts = 0;

for form in customsForms:
    questions.append(group_to_questions_all_answered(form))

for question in questions:
    sumOfCounts += len(question)

print ("Sum of question counts : ", sumOfCounts)