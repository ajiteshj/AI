#!/usr/bin/python
import sys
from copy import deepcopy
from random import random, randint, choice
import re
import itertools

query= []
sortedVariable = []
variables = {}
variablesObject = {}
queryNodes = {}
givenNodes = {}
target = open('output.txt','w')


class node(object):
    nodeName = ""
    parents = []
    probability = {}
    isDecision = 0

    def __init__(self):
        nodeName = ""
        self.parents = []
        self.probability = {}

    def setName(self, name):
        self.nodeName = name

    def setDecision(self):
        self.isDecision = 1

    def getDecision(self):
        return self.isDecision

    def setParents(self, parents):
        self.parents = parents

    def getParents(self):
        return self.parents

    def setProbability(self, parentValues, probabilityValue):
        if parentValues == [] :
            self.probability[tuple("+")] = probabilityValue
            return
        self.probability[tuple(parentValues)] = probabilityValue

    def getProbability(self, parentValues):
        if parentValues == [] :
            return self.probability[tuple("+")]
        return self.probability[tuple(parentValues)]

    def getDict(self):
        return self.probability


def readInput():
    global query
    global variables
    global variablesObject
    global sortedVariable
    f = open("input.txt","r")
    line = f.readlines()

    for i in range(0, len(line), 1):
        line[i] = line[i].strip("\n")
        line[i] = line[i].strip("\r")

    while True:
        i = 0
        if line[i] == "******":
            break
        else:
            query.append(line[i])
            line.remove(line[i])

    counter = 0
    i = 0
    variablesObject[counter] = node()
    while i < len(line):
        if line[i] == "***" or line[i] == "******":
            dist = (line[i+1]).split("|")
            variables[dist[0].strip(" ")] = counter
            sortedVariable.append(dist[0].strip(" "))
            variablesObject[counter].setName(dist[0].strip(" "))
            if(len(dist) > 1):
                parents = dist[1].split(" ")
                variablesObject[counter].setParents(parents[1:])
            i = i + 2
        line[i] = line[i].strip(" ")
        prob = line[i].split(" ")

        if line[i] != "decision":
            variablesObject[counter].setProbability(prob[1:], float(prob[0]))
        else:
            variablesObject[counter].setDecision()
            variablesObject[counter].setProbability([], float(1))

        if i == (len(line) - 1) or line[i+1] == "***" or line[i+1] == "******":
            counter = counter + 1
            if i != (len(line) - 1):
                variablesObject[counter] = node()
        i = i + 1

def setQueryNodes(queryVars):
    global queryNodes
    for i in range(0, len(queryVars)):
        temp = queryVars[i].split("=")
        nodeElem = temp[0].strip(" ")
        valElem = temp[1].strip(" ")
        queryNodes[nodeElem] = valElem

def setGivenNodes(givenVars):
    global givenNodes
    for i in range(0, len(givenVars)):
        temp = givenVars[i].split("=")
        nodeElem = temp[0].strip(" ")
        valElem = temp[1].strip(" ")
        givenNodes[nodeElem] = valElem

def getParentTuple(parents):
    global givenNodes

    if(len(parents) == 0):
        return []

    parentVals = []
    for i in range(0, len(parents)):
        if parents[i] in givenNodes:
            parentVals.append(givenNodes[parents[i]])

    return parentVals

def enumerateAll(vars):
    global givenNodes
    global queryNodes
    global variables
    global variablesObject

    if(len(vars) == 0):
        return 1.0

    first = vars[0]
    if first in givenNodes:
        probNode = variablesObject[variables[first]]
        parents = probNode.getParents()
        if givenNodes[first] == "+"  or probNode.getDecision() == 1:
            return probNode.getProbability(getParentTuple(parents)) * enumerateAll(vars[1:])
        else:
            return (1-probNode.getProbability(getParentTuple(parents))) * enumerateAll(vars[1:])
    else:
        probNode = variablesObject[variables[first]]
        parents = probNode.getParents()
        givenNodes[first] = "+"
        prob1 = probNode.getProbability(getParentTuple(parents)) * enumerateAll(vars[1:])
        givenNodes[first] = "-"
        prob2 = (1 - probNode.getProbability(getParentTuple(parents))) * enumerateAll(vars[1:])
        del givenNodes[first]
        return  prob1 + prob2

def normalize(QX, val):
    for key in QX.keys():
        if (QX[key] + val) != 0:
            QX[key] = QX[key]/(QX[key] + val)
    return QX

def enumerationNonBayes(n):
    global givenNodes
    global queryNodes
    global sortedVariable
    Q = {}
    for key in queryNodes.iterkeys():
        givenNodes[key] = queryNodes[key]
        Q[key] = enumerateAll(sortedVariable)
        del givenNodes[key]
    if n == 1:
        key = list(queryNodes.keys())[0]
        if queryNodes[key] == "+":
            givenNodes[key] = "-"
        else:
            givenNodes[key] = "+"
        val = enumerateAll(sortedVariable)
        del givenNodes[key]
        Q = normalize(Q, val)
    prob = 1
    for i in Q.iterkeys():
        prob = prob * Q[i]
    return prob

def enumerationAsk(n):
    global givenNodes
    global queryNodes
    global sortedVariable
    vars = []
    for i in range(0, len(sortedVariable)):
        if sortedVariable[i] in givenNodes.keys():
            vars.append(sortedVariable[i])
        else:
            check = 0
            for key in givenNodes.keys():
                node = variablesObject[variables[key]]
                if sortedVariable[i] in node.getParents() and check == 0:
                    vars.append(sortedVariable[i])
                    check = 1
        myNode = variablesObject[variables[sortedVariable[i]]]
        temp = myNode.getParents()
        for val in temp:
            if val not in vars:
                vars.append(val)
    vars2 = []
    for var in sortedVariable:
        if var in vars:
            vars2.append(var)
    prob = enumerateAll(vars2)
    return prob

def initEnum(query):
    global givenNodes
    global queryNodes
    queryvars = []
    givenvars = []
    val = 0.0
    toNormalize = 0
    temp = query.split("|")
    if len(temp[0].split(",")) > 1:
        givenvars = temp[0].split(",")
        if len(temp) > 1:
            toNormalize = 1
            queryvars = temp[1].split(",")
            givenvars.extend(temp[1].split(","))
        setQueryNodes(queryvars)
        setGivenNodes(givenvars)
        prob = enumerationAsk(toNormalize)
        if toNormalize == 1:
            givenNodes = {}
            setGivenNodes(queryvars)
            prob2 = enumerationAsk(toNormalize)
            if prob2 != 0:
                val = prob / prob2
            else:
                val = 0.0
        else:
            val = prob
    else:
        tempElem = temp[0].split(",")
        queryvars.append(tempElem[0])
        if len(temp) > 1:
            toNormalize = 1
            givenvars = temp[0].split(",")[1:]
            givenvars.extend(temp[1].split(","))
        else:
            givenvars = temp[0].split(",")[1:]
        setQueryNodes(queryvars)
        setGivenNodes(givenvars)
        prob = enumerationNonBayes(toNormalize)
        val = prob
    queryNodes = {}
    givenNodes = {}
    queryvars = []
    givenvars = []
    return val

def getEu(query):
    query = query[3:len(query) - 1]
    query = query.replace("|", ",")
    mynode = variablesObject[variables["utility"]]
    parent = mynode.getParents()
    dict = mynode.getDict()
    orig = deepcopy(query)
    val = 0.0
    for keys in dict.keys():
        check = 0
        mystr = deepcopy(orig)
        for i in range(0, len(parent)):
            if check == 0:
                mystr = parent[i] + "=" + keys[i] + "|" + mystr
                check = 1
            else:
                mystr = parent[i] + "=" + keys[i] + "," + mystr
        val = val + initEnum(mystr) * mynode.getProbability(keys)
    return val

def getMEU(query):
    query = query[4:len(query) - 1]
    query = query.replace("|", ",")
    varList = query.split(",")
    modStr = ""
    decList = []
    qList = []
    qList.append("")
    tempDict = {}
    for elem in varList:
        tempList = []
        if "=" not in elem:
            for i in range(0, len(qList)):
                if elem.strip(" ") not in decList:
                    decList.append(elem.strip(" "))
                modStr = qList[i]
                tempList.append(elem + "=+," + modStr)
                tempList.append(elem + "=-," + modStr)
        else:
            for i in range(0, len(qList)):
                modStr = qList[i]
                tempList.append(elem + "," + modStr)
        qList = tempList
    val = -100000.0
    str = ""
    for q in qList:
        q = q.replace(" ", "")
        if q[len(q) - 1] == ",":
            q = q[0:len(q) - 1]
        tempVal = getEu("EU("+q+")")
        if val < tempVal:
            tempDict = {}
            for i in range(0, len(q)):
                if q[i] in ["+", "-"] and q[i-2] in decList:
                    tempDict[q[i-2]] = q[i]
            val = tempVal
    for i in sorted(tempDict.keys()):
        str = str + tempDict[i] + " "
    sys.stdout.write(str)
    target.write(str)
    return val

def main():
    readInput()
    for i in range(0, len(query)):
        if query[i][0] == "P":
            query[i] = query[i][2:len(query[i]) - 1]
            a =format(round(initEnum(query[i]), 2), '.2f')
            target.write('%s\n'%(a))
        elif query[i][0] == "E":
            val = getEu(query[i])
            b = str(int(round(val)))
            target.write('%s\n' %(b))
        elif query[i][0] == "M":
            val = getMEU(query[i])
            c = str(int(round(val)))
            target.write('%s\n' %(c))

if __name__ == '__main__':
    main()
