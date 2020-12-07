# Read in input file line by line
import re

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


def validate_byr(byr):
    if not byr.isnumeric():
        return False

    byr = int(byr)
    if byr >= 1920 and byr <= 2002:
        return True
    else:
        return False


def validate_iyr(iyr):
    if not iyr.isnumeric():
        return False

    iyr = int(iyr)
    if iyr >= 2010 and iyr <= 2020:
        return True
    else:
        return False


def validate_eyr(eyr):
    if not eyr.isnumeric():
        return False

    eyr = int(eyr)
    if eyr >= 2020 and eyr <= 2030:
        return True
    else:
        return False


def validate_hgt(hgt):
    cmMatch = re.match(r"[0-9]{3}cm", hgt)
    inMatch = re.match(r"[0-9]{2}in", hgt)

    if not (cmMatch or inMatch):
        return False

    if cmMatch:
        value = int(hgt.split("cm")[0])
        return (value >= 150 and value <= 193)

    if inMatch:
        value = int(hgt.split("in")[0])
        return (value >= 59 and value <= 76)

    return False


def validate_hcl(hcl):
    return re.match(r"^#[0-9 a-f]{6}$", hcl)


def validate_ecl(ecl):

    validEcls = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

    for validEcl in validEcls:
        if ecl == validEcl:
            return True

    return False


def validate_pid(pid):
    return re.match(r"^[0-9]{9}$", pid)


def validate_passport(passport, reqiredFields):

    for requiredField in reqiredFields:
        if requiredField not in passport:
            return False
        else:
            if requiredField == "byr":
                if not validate_byr(passport[requiredField]):
                    return False

            if requiredField == "iyr":
                if not validate_iyr(passport[requiredField]):
                    return False

            if requiredField == "eyr":
                if not validate_eyr(passport[requiredField]):
                    return False

            if requiredField == "hgt":
                if not validate_hgt(passport[requiredField]):
                    return False

            if requiredField == "hcl":
                if not validate_hcl(passport[requiredField]):
                    return False

            if requiredField == "ecl":
                if not validate_ecl(passport[requiredField]):
                    return False

            if requiredField == "pid":
                if not validate_pid(passport[requiredField]):
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