import math
import csv
from objects import Line
import constants as c

## Init Level variables
numberOfLines =  1
goal = "Brew time"
lines_list = list()
lvldesc = "Level 1 \nYou add ingredients \nand drag them to a \nposition on the \nrecipe line. I \nremember starting this \nrecipe with a reversed \npotion. After that \nI would add \nhourglasses to cook \nfor the exact right \ntime."
potion_buttons = ["X","wait, 2 μs", "wait, 0.5 μs"]
potdesc = ["Reversed potion: \nReverse the state","Hourglass: \nWait for 2 μs", "Mini Hourglass: \nWait for 0.5 μs"]
current_score = 0
measure = "measure_z q[0]"

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
def appendpoints(result,time):
    X,Y = [],[]
    with open("Levels/lvl1data.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            X.append(row["X"])
            Y.append(row["Y"])
        X.append(time)
        Y.append(result['1'])
    with open("Levels/lvl1data.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["X", "Y"])  # Write header row
        for x, y in zip(X, Y):
            writer.writerow([x, y])

## Returns the points to show in progress graph
def loadpoints(X,Y):
    with open("Levels/lvl1data.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            X.append(float(row["X"]))
            Y.append(float(row["Y"]))
    return X,Y

## Calculate a score, based on the result
#Lvl 1: Get as close to 0.5 as possible, but below you're done
def calculatescore(result,runtime):
    global current_score
    score = 0

    if result['1'] >= 0.5:
        score = 100000 * math.exp((-2 * math.log(100000))*(result['1'] - 0.5))
    current_score = round(score)
    appendpoints(result,runtime)

## Returns the desctiptions of the potions for Almanac
def getPotDescription(index):
    return potdesc[index]

## Returns the leveldescription for Almanac
def getLvlDescription():
    return lvldesc