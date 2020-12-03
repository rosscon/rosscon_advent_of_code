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
    policyLimits = policy.split(" ")[0]
    policyLetter = policy.split(" ")[1]

    #Extract upper and lower bounds from limits
    policyLowCount = int(policyLimits.split("-")[0])
    policyHighCount = int(policyLimits.split("-")[1])

    letterCount = password.count(policyLetter)

    if letterCount >= policyLowCount and letterCount <= policyHighCount:
        validPasswords += 1
    else:
        invalidPasswords +=1



print ("Valid Passwords = ", validPasswords)
print ("Invalid Passwords = ", invalidPasswords)