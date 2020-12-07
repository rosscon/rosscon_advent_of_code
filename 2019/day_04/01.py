

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
    for digit in password:
        if int(digit) == previousDigit:
            return True
        previousDigit = int(digit)

    return False


validPasswordCount = 0

for password in range (_lowValue, _highValue + 1, 1):
    if validate_password(password):
        validPasswordCount += 1
        print ("Valid : ", password)