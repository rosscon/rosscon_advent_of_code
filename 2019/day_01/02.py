import math

fileName="input01.txt"

infile = open(fileName, 'r')
lines = [int(line) for line in infile.readlines()]

def calculate_fuel_req(mass=0):
    fuel = 0
    while math.floor(mass/3) -2 > 0:
        tmpFuel = math.floor(mass/3) -2
        fuel +=tmpFuel
        mass=tmpFuel

    return fuel

fuelCounter=0

for line in lines:
    fuelCounter += calculate_fuel_req(mass=line)

print("Total fuel = ", fuelCounter)