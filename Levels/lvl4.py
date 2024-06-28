import csv
from objects import Line
import constants as c

## Init Level variables
numberOfLines =  3
goal = "Teleport"
lines_list = list()
lvldesc = "Level 4 \nYou add ingredients \nand drag them to a \nposition on the \nrecipe line. \nTo entangle wires, \ndrag a special \ningredient to a \nline, and drag the \nsecond part to \nanother line. \nYour goal is to \ntransfer the state \nfrom the first line \nto the second one"
potion_buttons = ["H", "barrier", "measure_z", "CNOT", "CZ"]
potdesc = ["Tilted potion: \nUsed to slightly \ntilt the kettle\n and steer angled.","Protective Foil: \nUse to keep parts \nof the recipe \nseperated.","Tongue Extract: \nUsed to taste \nthe current state \nof a potion.","Red entangle Potion: \nReverse the second \npotion, but only if \nthe first catches.","Blue Entangle Potion: \nFlip the second \npotion, but only if \nthe first catches."]
current_score = 0
measure = "measure_x q[2]"

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
def getMeasure():
    return measure

## Adds results to show in the progress graph to the lvldata file
# Currently not implemented
def appendpoints(result,time):
    X,Y = [],[]
    with open("Levels/lvl4data.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            X.append(row["X"])
            Y.append(row["Y"])
        X.append(time)
        Y.append(result['1'])
    with open("Levels/lvl4data.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["X", "Y"])  # Write header row
        for x, y in zip(X, Y):
            writer.writerow([x, y])

## Returns the points to show in progress graph
# currently unused
def loadpoints(X,Y):
    with open("Levels/lvl4data.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            X.append(float(row["X"]))
            Y.append(float(row["Y"]))
    return X,Y

## Calculate a score, based on the result
#Lvl 4: the state in q1 should be nearing 1
def calculatescore(result,runtime):
    global current_score
    x = result['1'] + result['5']
    score = 0
    score = 100000 * ((x - 0.75) / 0.25) ** 10 if x >=0.75 else 0
    current_score = round(score)

## Returns the desctiptions of potion {index} for Almanac
def getPotDescription(index):
    return potdesc[index]

## Returns the leveldescription for Almanac
def getLvlDescription():
    return lvldesc