# Read in input file line by line
fileName="input02.txt"

infile = open(fileName, 'r')
lines = [line for line in infile.readlines()]

validPasswords = 0
invalidPasswords = 0

for line in lines:
    #Split policy from password string
    policy = line.split(": ")[0]
    password = line.split(": ")[1]

    #Split policy limits from policy letter
    policyPositions = policy.split(" ")[0].split("-")
    policyLetter = policy.split(" ")[1]

    count = 0

    #Extract upper and lower bounds from limits
    for position in policyPositions:
        if password[(int(position)-1):int(position)] != policyLetter:
            count += 1

    if count == 1:
        validPasswords += 1
        print("Valid : ", line)
    else:
        invalidPasswords +=1
        print("Invalid : ", line)



print ("Valid Passwords = ", validPasswords)
print ("Invalid Passwords = ", invalidPasswords)