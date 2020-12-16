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

    for val in ticket:

        valueValid = False

        for fieldValues in fields.values():
            for r in fieldValues:
                if val >= r[0] and val <= r[1]:
                    valueValid =  True

        if not valueValid:
            return False

    return True


def value_valid_for_ranges(value, ranges):

    for r in ranges:
        if r[0] <= value and r[1] >= value:
            #print ('Value: ', value, ' in Range: ', r)
            return True

    #print ('Value: ', value, ' not in Ranges: ', ranges)
    return False


#determine which ticket field index is valid for each field by elimination
#very similar to sudoku solvers, need to eliminate values and positions
def find_field_indexes(fields, tickets):

    mappedIndexes = {}

    unsolvedIndexes = list(range(len(fields)))
    unsolvedFields = fields.copy()

    previousLength = len(unsolvedFields)

    while (len(unsolvedFields)) > 0:

        #Find potential indexes for field
        for unsolvedField,unsolvedRange in unsolvedFields.items():

            potentialIndexes = [];

            for unsolvedIndex in unsolvedIndexes:

                validForAllTickets = True

                for ticket in tickets:
                    if not value_valid_for_ranges(ticket[unsolvedIndex], unsolvedRange):
                        validForAllTickets = False

                if validForAllTickets:
                    potentialIndexes.append(unsolvedIndex)

            if len(potentialIndexes) == 1:
                print('Index Elimination')
                print ('Unsolved Fields: ', len(unsolvedFields))
                print ('Unsolved Indexes: ', unsolvedIndexes)
                print (potentialIndexes)
                mappedIndexes[unsolvedField] = potentialIndexes[0]
                unsolvedIndexes.remove(potentialIndexes[0])
                unsolvedFields.pop(unsolvedField)
                print ('Unsolved Fields: ', len(unsolvedFields))
                print ('Unsolved Indexes: ', unsolvedIndexes)
                print('')
                break
            else :
                print('Index Elimination')
                print (potentialIndexes)
                print()

        #find potential fields for indexes
        for unsolvedIndex in unsolvedIndexes:

            potentialFields = [];

            for unsolvedField,unsolvedRange in unsolvedFields.items():

                validForAllTickets = True

                for ticket in tickets:
                    if not value_valid_for_ranges(ticket[unsolvedIndex], unsolvedRange):
                        validForAllTickets = False

                if validForAllTickets:
                    potentialFields.append(unsolvedField)

            if len(potentialFields) == 1:
                print('Field Elimination')
                print ('Unsolved Fields: ', len(unsolvedFields))
                print ('Unsolved Indexes: ', unsolvedIndexes)
                print (potentialFields)
                mappedIndexes[potentialFields[0]] = unsolvedIndex
                unsolvedIndexes.remove(unsolvedIndex)
                unsolvedFields.pop(potentialFields[0])
                print ('Unsolved Fields: ', len(unsolvedFields))
                print ('Unsolved Indexes: ', unsolvedIndexes)
                print('')
                break
            else:
                print('Field Elimination')
                print (potentialFields)
                print()


        if len(unsolvedFields) == previousLength:
            print ('Infinite loop detected')
            break
        previousLength =  len(unsolvedFields)


    return mappedIndexes




def decode_ticket(fieldIndexes, ticket):
    decodedTicket = {}

    for field,index in fieldIndexes.items():
        decodedTicket[field] = ticket[index]

    return decodedTicket



notes = parse_notes(notes)

validTickets = []
invalidTickets = []


for ticket in notes['tickets']:

    validateOutcome = validate_ticket(notes['fields'], ticket)

    if validateOutcome:
        validTickets.append(ticket)
    else:
        invalidTickets.append(ticket)


fieldIndexes = find_field_indexes(notes['fields'], validTickets)
decodedTicket = decode_ticket(fieldIndexes, notes['myTicket'])

multiplied = 1

for key,value in decodedTicket.items():
    if key.startswith('departure'):
        multiplied *= value

print ('Answer: ', multiplied)


