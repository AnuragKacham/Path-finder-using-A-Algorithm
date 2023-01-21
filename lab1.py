"""
Lab 1 program
Author: @Anurag Kacham ak4579
"""

import math
import sys
from sys import argv
from PIL import Image

areasWithColor = {(248, 148, 18): "openLand", (255, 192, 0): "roughMeadow", (255, 255, 255): "easyMoveForest",
                  (2, 208, 60): "slowRunForest", (2, 136, 40): "walkForest", (5, 73, 24): "impassibleVegetation",
                  (0, 0, 255): "lakeSwamp", (71, 51, 3): "pavedRoad", (0, 0, 0): "footpath",
                  (205, 0, 101): "outOfBounds"}

areasWithSpeed = {"openLand": 2, "roughMeadow": 0.25, "easyMoveForest": 1.25, "slowRunForest": 1, "walkForest": 0.75,
                  "impassibleVegetation": 0, "lakeSwamp": 0, "pavedRoad": 2, "footpath": 2, "outOfBounds": 0}

terrains = []
elevation = []
wayToTarget = []


class pixelAttributes:
    def __init__(self, x, y):
        self.nodeType = None
        self.elevNode = None
        self.ifVis = None
        self.total = float("inf")
        self.x = x
        self.y = y


def getNeighbors(st, mapUnit):
    xVal = st.x
    yVal = st.y
    listOfNeighbors = []

    if xVal == 499:
        if yVal == 0:
            if areasWithSpeed[mapUnit[xVal][yVal + 1].nodeType] != 0:
                listOfNeighbors.append(mapUnit[xVal][yVal + 1])
            if areasWithSpeed[mapUnit[xVal - 1][yVal].nodeType] != 0:
                listOfNeighbors.append(mapUnit[xVal - 1][yVal])
        if yVal == 394:
            if areasWithSpeed[mapUnit[xVal - 1][yVal].nodeType] != 0:
                listOfNeighbors.append(mapUnit[xVal - 1][yVal])
            if areasWithSpeed[mapUnit[xVal][yVal - 1].nodeType] != 0:
                listOfNeighbors.append(mapUnit[xVal][yVal - 1])
        if 0 < yVal < 394:
            if areasWithSpeed[mapUnit[xVal][yVal - 1].nodeType] != 0:
                listOfNeighbors.append(mapUnit[xVal][yVal - 1])
            if areasWithSpeed[mapUnit[xVal][yVal + 1].nodeType] != 0:
                listOfNeighbors.append(mapUnit[xVal][yVal + 1])
            if areasWithSpeed[mapUnit[xVal - 1][yVal].nodeType] != 0:
                listOfNeighbors.append(mapUnit[xVal - 1][yVal])
    elif xVal == 0:
        if yVal == 0:
            if areasWithSpeed[mapUnit[xVal][yVal + 1].nodeType] != 0:
                listOfNeighbors.append(mapUnit[xVal][yVal + 1])
            if areasWithSpeed[mapUnit[xVal + 1][yVal].nodeType] != 0:
                listOfNeighbors.append(mapUnit[xVal + 1][yVal])
        if yVal == 394:
            if areasWithSpeed[mapUnit[xVal][yVal - 1].nodeType] != 0:
                listOfNeighbors.append(mapUnit[xVal][yVal - 1])
            if areasWithSpeed[mapUnit[xVal + 1][yVal].nodeType] != 0:
                listOfNeighbors.append(mapUnit[xVal + 1][yVal])
        if 0 < yVal < 394:
            if areasWithSpeed[mapUnit[xVal][yVal - 1].nodeType] != 0:
                listOfNeighbors.append(mapUnit[xVal][yVal - 1])
            if areasWithSpeed[mapUnit[xVal][yVal + 1].nodeType] != 0:
                listOfNeighbors.append(mapUnit[xVal][yVal + 1])
            if areasWithSpeed[mapUnit[xVal + 1][yVal].nodeType] != 0:
                listOfNeighbors.append(mapUnit[xVal + 1][yVal])
    elif 0 < xVal < 499 and yVal == 394:
        if areasWithSpeed[mapUnit[xVal + 1][yVal].nodeType] != 0:
            listOfNeighbors.append(mapUnit[xVal + 1][yVal])
        if areasWithSpeed[mapUnit[xVal][yVal - 1].nodeType] != 0:
            listOfNeighbors.append(mapUnit[xVal][yVal - 1])
        if areasWithSpeed[mapUnit[xVal - 1][yVal].nodeType] != 0:
            listOfNeighbors.append(mapUnit[xVal - 1][yVal])
    elif 0 < xVal < 499 and yVal == 0:
        if areasWithSpeed[mapUnit[xVal + 1][yVal].nodeType] != 0:
            listOfNeighbors.append(mapUnit[xVal + 1][yVal])
        if areasWithSpeed[mapUnit[xVal][yVal + 1].nodeType] != 0:
            listOfNeighbors.append(mapUnit[xVal][yVal + 1])
        if areasWithSpeed[mapUnit[xVal - 1][yVal].nodeType] != 0:
            listOfNeighbors.append(mapUnit[xVal - 1][yVal])
    else:
        if areasWithSpeed[mapUnit[xVal + 1][yVal].nodeType] != 0:
            listOfNeighbors.append(mapUnit[xVal + 1][yVal])
        if areasWithSpeed[mapUnit[xVal - 1][yVal].nodeType] != 0:
            listOfNeighbors.append(mapUnit[xVal - 1][yVal])
        if areasWithSpeed[mapUnit[xVal][yVal - 1].nodeType] != 0:
            listOfNeighbors.append(mapUnit[xVal][yVal - 1])
        if areasWithSpeed[mapUnit[xVal][yVal + 1].nodeType] != 0:
            listOfNeighbors.append(mapUnit[xVal][yVal + 1])
    return listOfNeighbors


def bestWayToTarget(st, tar, tempMap):
    if areasWithSpeed[st.nodeType] == 0 or areasWithSpeed[tar.nodeType] == 0:
        print("Wrong st or tar")
        return
    st.total = 0
    temp = st
    added = []
    haveAdd = [temp]
    while len(haveAdd) != 0:
        bestDist = float("inf")
        bestVal = None
        for dot in haveAdd:
            if dot.total < bestDist:
                bestDist = dot.total
                bestVal = dot
        temp = bestVal
        if temp == tar:
            while temp.ifVis:
                row = [temp.x, temp.y]
                wayToTarget.append(row)
                temp = temp.ifVis
            row = [temp.x, temp.y]
            wayToTarget.append(row)
            return wayToTarget
        haveAdd.remove(temp)
        added.append(temp)
        nodeNeigh = getNeighbors(temp, tempMap)
        for each in nodeNeigh:
            if each not in added:
                if each in haveAdd:
                    f = fVal(tar, temp, each)
                    if f < each.total:
                        each.total = f
                        each.ifVis = temp
                else:
                    each.total = fVal(tar, temp, each)
                    each.ifVis = temp
                    haveAdd.append(each)
    print("Target not found")


def fVal(tar, temp, dot):
    """
    f(x) = g(x) + h(x)
    :param tar: target
    :param temp: temp pixel
    :param dot: neighbor
    :return: distance
    """
    if dot.x != temp.x:
        dist = gVal(False, temp, dot) + math.sqrt((dot.x - tar.x) ** 2 + (dot.y - tar.y) ** 2 +
                                                  (dot.elevNode - tar.elevNode) ** 2) / 2
    else:
        dist = gVal(True, temp, dot) + math.sqrt((dot.x - tar.x) ** 2 + (dot.y - tar.y) ** 2 +
                                                 (dot.elevNode - tar.elevNode) ** 2) / 2
    return dist


def gVal(flagCheck, st, tar):
    if flagCheck:
        dist = math.sqrt(((tar.elevNode - st.elevNode) * 10.29) ** 2)
    else:
        dist = math.sqrt(((tar.elevNode - st.elevNode) * 7.55) ** 2)
    gValue = dist / (areasWithSpeed[st.nodeType] + (st.elevNode - tar.elevNode) / 40)

    return gValue


def exec():
    ways = []
    arg1 = Image.open(argv[1])
    mapSnap = list(arg1.getdata())
    lines = []
    column = 0
    for dot in mapSnap:
        column += 1
        lines.append(dot)
        if column == 395:
            terrains.append(lines)
            lines = []
            column = 0
    f = open(argv[2], 'r')
    for line in f:
        word = line.strip().split()
        words = []
        for m in range(len(word)):
            words.append(float(word[m]))
        elevation.append(words)

    with open(argv[3]) as rf:
        for word in rf:
            pix = []
            w = word.strip().split()
            pix.append(int(w[1]))
            pix.append(int(w[0]))
            ways.append(pix)
    n = len(ways)
    for iter in range(n - 1):
        tempMap = []
        for m in range(500):
            word = []
            for n in range(395):
                temp = pixelAttributes(m, n)
                temp.nodeType = areasWithColor[terrains[m][n][:3]]
                temp.elevNode = elevation[m][n]
                word.append(temp)
            tempMap.append(word)
        st = ways[iter]
        tar = ways[iter + 1]
        bestWayToTarget(tempMap[st[0]][st[1]], tempMap[tar[0]][tar[1]], tempMap)
    length = 0
    l = len(wayToTarget)
    for iter in range(l - 1):
        arg1.putpixel((wayToTarget[iter][1], wayToTarget[iter][0]), (255, 0, 127))
        length = length + (math.sqrt(((wayToTarget[iter][1] - wayToTarget[iter + 1][1]) * 10.29) ** 2 +
                                     ((wayToTarget[iter][0] - wayToTarget[iter + 1][0]) * 7.55) ** 2 +
                                     (float(elevation[wayToTarget[iter][1]][wayToTarget[iter][0]]) -
                                      float(elevation[wayToTarget[iter + 1][1]][wayToTarget[iter + 1][0]])) ** 2))

    arg1.putpixel((wayToTarget[len(wayToTarget) - 1][1], wayToTarget[len(wayToTarget) - 1][0]), (255, 0, 127))
    arg1.save(argv[4])
    print(str(length) + " m")


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("There must be 4 valid files")
    else:
        exec()
