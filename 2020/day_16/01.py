_fileName = "input16.txt"

lines = ""

with open(_fileName) as file:
    lines = file.read()

notes = lines.split("\n\n")


def parse_tickets(tickets):
    ts = []
    for ticket in tickets:
        ts.append([int(t.rstrip()) for t in ticket.split(',')])
    return ts


def parse_fields(fields):
    fs = {}

    for field in fields:

        name = field.split(': ')[0]

        ranges = field.split(': ')[1].split(' or ')
        ranges = [[int (val) for val in r.split('-')] for r in ranges]

        fs[name] = ranges

    return fs


def parse_notes(notes):

    notes = {
            'fields': parse_fields(notes[0].split('\n')),
            'tickets': parse_tickets(notes[2].split('\n')[1:-1]),
            'myTicket' : parse_tickets(notes[1].split('\n')[1:])[0]
            }

    return notes


def validate_ticket(fields, ticket):

    sumInvalidFields = 0

    for val in ticket:

        valueValid = False

        for fieldValues in fields.values():
            for r in fieldValues:
                if val >= r[0] and val <= r[1]:
                    valueValid =  True

        if not valueValid:
            sumInvalidFields += val

    return sumInvalidFields


notes = parse_notes(notes)

validTickets = []
invalidTickets = []

sumValidations = 0;

for ticket in notes['tickets']:

    validateOutcome = validate_ticket(notes['fields'], ticket)
    sumValidations += validateOutcome

    if validateOutcome == 0:
        validTickets.append(ticket)
    else:
        invalidTickets.append(ticket)


print('Answer: ', sumValidations)

