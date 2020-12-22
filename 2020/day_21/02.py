

def parse_input(line):

    ingredients = line.split(" (contains ")[0].split(' ')
    allergens = line.split(" (contains ")[1][:-2].split(', ')

    return {'ingredients' : ingredients, 'allergens': allergens}


def parse_allergens(labels):
    allergens = {}

    for label in labels:
        for allergen in label['allergens']:
            if allergen in allergens:
                allergens[allergen] = [i for i in label['ingredients'] if i in allergens[allergen]]
            else:
                allergens[allergen] = label['ingredients']

    return allergens


def count_ingredients(labels):
    ingredientCounts = {}

    for label in labels:
        for ingredient in label['ingredients']:
            if ingredient in ingredientCounts:
                ingredientCounts[ingredient] += 1
            else:
                ingredientCounts[ingredient] = 1

    return ingredientCounts

def count_impossible(allergens, ingredients):

    count = 0

    for ingredient, c in ingredients.items():
        if all(ingredient not in v for v in allergens.values()):
            count += c

    return count

def unique_allergens(allergens):
    used = set()
    while any(len(a) > 1 for a in allergens.values()):
        for allergen, ingredient in allergens.items():
            if len(ingredient) == 1 and ingredient[0] not in used:
                used.add(ingredient[0])
            elif len(ingredient) > 1:
                for i in used:
                    if i in ingredient:
                        allergens[allergen].remove(i)
    return allergens

def allergens_to_csv(allergens):
    ingredients = []

    for k in sorted(allergens.keys()):
        ingredients.extend(allergens[k])

    return ','.join(ingredients)



_fileName = "input21.txt"
lines = ""

with open(_fileName) as file:
    lines = file.readlines()

labels = []

for line in lines:
    labels.append(parse_input(line))



allergens = parse_allergens(labels)
ingredientCounts = count_ingredients(labels)
count = count_impossible(allergens, ingredientCounts)

allergens = unique_allergens(allergens)

answer = allergens_to_csv(allergens)
