

_lowValue = 146810
_highValue = 612564


#Validate each password
def validate_password(password):
    password = str(password)

    previousDigit = 0

    #Check all digits are same or incremental
    for digit in password:
        if int(digit) >= previousDigit:
            previousDigit = int(digit)
        else:
            return False

    #Check if the string contains a double digit
    previousDigit = 0

    digitGroups = []
    tmpGroup = []

    for digit in password:
        if int(digit) == previousDigit:
            tmpGroup.append(digit)
        else:
            digitGroups.append(tmpGroup)
            tmpGroup = [digit]

        previousDigit = int(digit)

    digitGroups.append(tmpGroup)

    for group in digitGroups:
        if len(group) == 2:
            return True


    return False


validPasswordCount = 0
validPasswords = []

for password in range (_lowValue, _highValue + 1, 1):
    if validate_password(password):
        validPasswordCount += 1
        validPasswords.append(password)

print("Valid password found : ", validPasswordCount)