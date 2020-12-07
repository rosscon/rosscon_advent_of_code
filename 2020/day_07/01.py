import sys
print(sys.getrecursionlimit())

#sys.setrecursionlimit(150000)

# Read in input file line by line
_fileName="input07.txt"

infile = open(_fileName, 'r')
bagRows = [line for line in infile.readlines()]

#Parses the second half of the bag contains string
def parse_contents(inContents):
    contents = {}

    tmpContents = inContents.split(", ")

    if "no other bags." in inContents:
        return contents

    for content in tmpContents:
        bagColor = content.split(" ", 1)[1]
        bagCount = int(content.split(" ", 1)[0])

        #sometimes the last item in the list contains a new line or '.' char
        bagColor = bagColor.replace(".","").replace("\n", "")

        #if keying on bag colour adding an s to singles will help
        if bagCount == 1:
            bagColor += "s"

        contents[bagColor] = bagCount

    return contents


#Does what it says, parses a bag string
def parse_bag(row):

    bag = {}
    color = row.split(" contain ")[0]

    contents = row.split(" contain ")[1]
    contents = contents.split(", ")

    bag ["contains"] = parse_contents(row.split(" contain ")[1])

    return color , bag


#Recursive functionto find all bags that could contain the target
def find_container_bags(bags, targetBag = "shiny gold bags"):
    containingBags = []

    #print("targetBag: ", targetBag)

    for bagKey, bagValue in bags.items():
        if targetBag in bagValue["contains"]:
            containingBags.append(bagKey)
            #print("nextBag: ", bagKey)
            containingBags.extend(find_container_bags(bags, targetBag = bagKey))
            #print("contained ", bag)


    return containingBags


#Main
bags = {}

for row in bagRows:
    bag = parse_bag(row)

    if bag[0] in bags:
        print("bag already exists : ", bag [0])

    bags[bag[0]] = bag[1]

containingBags = find_container_bags(bags, targetBag = "shiny gold bags")

containingBagsDict = {}

for bag in containingBags:
    if bag not in containingBagsDict:
        containingBagsDict[bag] = 1







