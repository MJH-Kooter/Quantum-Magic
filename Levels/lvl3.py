import csv
from objects import Line
import constants as c

## Init Level variables
numberOfLines =  2
goal = "Entangle"
lines_list = list()
lvldesc = "Level 3 \nYou add ingredients \nand drag them to a \nposition on the \nrecipe line. \nTo entangle wires, \ndrag a special \ningredient to a \nline, and drag the \nsecond part to \nanother line."
potion_buttons = ["H", "CNOT", "CZ"]
potdesc = ["Tilted potion: \nUsed to slightly \ntilt the kettle\n and steer angled.","Red entangle Potion: \nReverse the second \npotion, but only if \nthe first catches.","Blue Entangle Potion: \nFlip the second \npotion, but only if \nthe first catches."]
current_score = 0
measure = ["measure_z q[0,2]","measure_x q[0,2]"]
first_result = 0
count = -1

## Init the working lines for the level
def create_lines():
    for X in range(numberOfLines):
        line = Line(X,c.Length)
        lines_list.append(line)
    return


## Returns the score of the level
def getScore():
    return current_score

## Returns the way of measuring the circuit
# Iterates between Measuring X and Z in this level
def getMeasure():
    global count
    count += 1
    if count == 0:
        count = -1
    return measure[count]

## Adds results to show in the progress graph to the lvldata file
# currently not implemented
def appendpoints(result,time):
    X,Y = [],[]
    with open("Levels/lvl3data.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            X.append(row["X"])
            Y.append(row["Y"])
        X.append(time)
        Y.append(result['1'])
    with open("Levels/lvl3data.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["X", "Y"])  # Write header row
        for x, y in zip(X, Y):
            writer.writerow([x, y])

## Returns the points to show in progress graph
# currently unused
def loadpoints(X,Y):
    with open("Levels/lvl3data.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            X.append(float(row["X"]))
            Y.append(float(row["Y"]))
    return X,Y


## Stores the result of the first calculation
# Because of hardware 2 seperate mearures must be made
def storescore(result):
    global first_result
    first_result = result['0']
    first_result += result['5']

## Calculate a score, based on the result
#Lvl 3: Combination of meassures should be nearing 1
def calculatescore(result,runtime):
    global current_score
    global first_result
    results = 0
    results += result['0']
    results += result['5']
    x = results * first_result
    score = 100000 * ((x - 0.75) / 0.25) ** 10 if x >=0.75 else 0
    current_score = round(score)

## Returns the desctiptions of potion {index} for Almanac
def getPotDescription(index):
    return potdesc[index]

## Returns the leveldescription for Almanac
def getLvlDescription():
    return lvldesc