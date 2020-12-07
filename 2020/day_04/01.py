# Read in input file line by line
_fileName = "input04.txt"

lines = ""

with open(_fileName) as file:
    lines = file.read()

passportsInput = lines.split("\n\n")

_requiredFields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
_optionalFields = ["cid"]

def parse_passport_strings(passportStrings):

    passports = []

    for passportString in passportsInput:
        passportFieldsStrings = passportString.split()

        passport = {}

        for fieldString in passportFieldsStrings:
            fieldName = fieldString.split(":")[0]
            fieldValue = fieldString.split(":")[1]
            passport[fieldName] =  fieldValue

        passports.append(passport)

    return passports


def validate_passport(passport, reqiredFields):

    for requiredField in reqiredFields:
        if requiredField not in passport:
            return False

    return True


passports = parse_passport_strings(passportsInput)

validPassports = []
invalidPassports = []

for passport in passports:
    if validate_passport(passport, _requiredFields):
        validPassports.append(passport)
    else:
        invalidPassports.append(passport)

print ("Valid passports : ", len(validPassports))
print ("Inalid passports : ", len(invalidPassports))