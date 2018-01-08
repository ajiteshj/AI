#!/usr/bin/python
import sys
from copy import deepcopy
from random import random, randint, choice
import re

Clause = []
Sentence = []
NoOfGuests = []
NoOfTables = []
Relations = []
ClauseList = []
literals = []
target = open('output.txt','w')

def addToLiteral(x):
    if x not in literals:
        literals.append(x)


def clauseTab1():
    global Clause
    global Sentence

    for g in range(1, int(NoOfGuests) + 1):
        for t in range(1, int(NoOfTables) + 1):
            Clause.append("X" + str(g) + ','+ str(t))
            addToLiteral("X" + str(g) + ','+ str(t))
        Sentence.append(Clause)
        Clause = []

    for i in range(len(Relations)):
        if Relations[i][4] == 'F':
            for tab in range(1, int(NoOfTables) + 1):
                Clause.append("~" + "X" + str(Relations[i][0]) +','+ str(tab))
                Clause.append("X" + str(Relations[i][2]) +','+ str(tab))
                addToLiteral("~" + "X" + str(Relations[i][0]) +','+ str(tab))
                addToLiteral("X" + str(Relations[i][2]) +','+ str(tab))
                Sentence.append(Clause)
                Clause = []
                Clause.append("X" + str(Relations[i][0]) +','+ str(tab))
                Clause.append("~" + "X" + str(Relations[i][2]) +','+ str(tab))
                addToLiteral("X" + str(Relations[i][0]) +','+ str(tab))
                addToLiteral("~" + "X" + str(Relations[i][2]) +','+ str(tab))
                Sentence.append(Clause)
                Clause = []
        elif Relations[i][4] == 'E':
            for tab in range(1, int(NoOfTables) + 1):
                Clause.append("~" + "X" + str(Relations[i][0]) +','+str(tab))
                Clause.append("~" + "X" + str(Relations[i][2]) +',' +str(tab))
                addToLiteral("~" + "X" + str(Relations[i][0]) +','+str(tab))
                addToLiteral("~" + "X" + str(Relations[i][2]) +',' +str(tab))
                Sentence.append(Clause)
                Clause = []



    return


def clauseDef():
    global Clause
    global Sentence

    for g in range(1, int(NoOfGuests) + 1):
        for t in range(1, int(NoOfTables) + 1):
            for s in range(t+1, int(NoOfTables) + 1):
                Clause.append("~" + "X" + str(g) + ',' + str(t))
                addToLiteral("~" + "X" + str(g) + ',' + str(t))
                Clause.append("~" + "X" + str(g) + ',' + str(s))
                addToLiteral("~" + "X" + str(g) + ',' + str(s))
                Sentence.append(Clause)
                Clause = []

    for g in range(1, int(NoOfGuests) + 1):
        for t in range(1, int(NoOfTables) + 1):
            Clause.append("X" + str(g) + ','+ str(t))
            addToLiteral("X" + str(g) + ','+ str(t))
        Sentence.append(Clause)
        Clause = []

    for i in range(len(Relations)):
        if Relations[i][4] == 'F':
            for tab in range(1, int(NoOfTables) + 1):
                Clause.append("~" + "X" + str(Relations[i][0]) +','+ str(tab))
                Clause.append("X" + str(Relations[i][2]) +','+ str(tab))
                addToLiteral("~" + "X" + str(Relations[i][0]) +','+ str(tab))
                addToLiteral("X" + str(Relations[i][2]) +','+ str(tab))
                Sentence.append(Clause)
                Clause = []
                Clause.append("X" + str(Relations[i][0]) +','+ str(tab))
                Clause.append("~" + "X" + str(Relations[i][2]) +','+ str(tab))
                addToLiteral("X" + str(Relations[i][0]) +','+ str(tab))
                addToLiteral("~" + "X" + str(Relations[i][2]) +','+ str(tab))
                Sentence.append(Clause)
                Clause = []
        elif Relations[i][4] == 'E':
            for tab in range(1, int(NoOfTables) + 1):
                Clause.append("~" + "X" + str(Relations[i][0]) +','+str(tab))
                Clause.append("~" + "X" + str(Relations[i][2]) +',' +str(tab))
                addToLiteral("~" + "X" + str(Relations[i][0]) +','+str(tab))
                addToLiteral("~" + "X" + str(Relations[i][2]) +',' +str(tab))
                Sentence.append(Clause)
                Clause = []



    return

def checkInequality(resolvents, new):
    for i in range(0, len(new)):
        if len(new[i]) == len(resolvents):
            arr1 = deepcopy(new[i])
            arr2 = deepcopy(resolvents)
            if set(arr1) == set(arr2):
                return False
    return True


def PLResolution(KB):
    global ClauseList
    Clauses = KB
    C1 = []
    C2 = []
    j = 0
    ClauseList = deepcopy(Clauses)
    count =0
    while True:
        new = []
        for i in range(0, len(ClauseList)):

            for j in range(i + 1, len(ClauseList)):

                C1 = deepcopy(ClauseList[i])
                C2 = deepcopy(ClauseList[j])
                resolvents = PLResolve(C1, C2)




                if resolvents == []:

                    return False
                if resolvents:
                    if checkInequality(resolvents, new):
                        new.append(resolvents)
                        count = count +1




                if count > 500:
                    #print "Exceeded count"
                    return True



        if not new:
            return True

        check = 0

        for k in range(len(new)):
            if checkInequality(new[k], ClauseList):
                ClauseList.append(new[k])
                check = 1

        if check == 0:
            #print "No new added"
            return True




def PLResolve(c1, c2):

    rclause = None
    for i in range(0, len(c1)):
        c = c1[i]

        for j in range(0, len(c2)):
            if '~' in c:
                if c2[j] == c.strip('~'):
                    c1.remove(c1[i])
                    c2.remove(c2[j])
                    for x in reversed(range(0, len(c1))):
                        for y in reversed(range(0, len(c2))):
                            if c1[x] == c2[y]:
                                c2.remove(c2[y])
                    rclause = c1 + c2
                    return rclause
            else:
                if c2[j] == '~' + str(c):
                    c1.remove(c1[i])
                    c2.remove(c2[j])
                    for x in reversed(range(0, len(c1))):
                        for y in reversed(range(0, len(c2))):
                            if c1[x] == c2[y]:
                                c2.remove(c2[y])
                    rclause = c1 + c2
                    return rclause

    return







def readInput():
    global NoOfGuests
    global NoOfTables
    global Relations
    f = open("input.txt","r")
    line = f.readline()
    line = line.split()
    # line = line.strip()
    NoOfGuests = line[0]
    NoOfTables = line[1]

    Relations = f.readlines()

    return

def randomAssignmentSymbols():
    model = {}
    for i in range(0, len(literals) ):
        if '~' in literals[i]:
            model[literals[i]] = choice([True, False])
            model[literals[i].strip('~')] = ( True, False )[model[literals[i]]]
        else:
            model[literals[i]] = choice([True, False])
            model['~' + literals[i]] = (True, False)[model[literals[i]]]
    return model

def checkModel(model):
    for i in range(0, len(Sentence)):
        check = 0
        for j in range(0, len(Sentence[i])):
            if model[Sentence[i][j]] :
                check = 1
        if check == 0:
            return False
    return True

def checkFalses(model):
    counter = 0
    for i in range(0, len(Sentence)):
        check = 0
        for j in range(0, len(Sentence[i])):
            if model[Sentence[i][j]] :
                check = 1
        if check == 0:
            counter = counter + 1
    return counter

def changeValue(model, literalToChange):
    # type: (object, object) -> object
    if '~' in literalToChange:
        model[literalToChange] = (True, False)[model[literalToChange]]
        model[literalToChange.strip('~')] = (True, False)[model[literalToChange]]
    else:
        model[literalToChange] = (True, False)[model[literalToChange]]
        model['~' + literalToChange] = (True, False)[model[literalToChange]]
    return model

def changeMinimumValue(model, index):
    min = 100000
    min_index = 0
    for i in range(0, len(Sentence[index])):
        model = changeValue(model, Sentence[index][i])
        temp_min = checkFalses(model)
        model = changeValue(model, Sentence[index][i])
        if(temp_min < min):
            min = temp_min
            min_index = i
    model = changeValue(model, Sentence[index][min_index])
    return model

def getRandomFalseClause(model):
    while True:
        index = randint(0, len(Sentence) - 1)
        check = 0
        for j in range(0, len(Sentence[index])):
            if model[Sentence[index][j]]:
                check = 1
        if check == 0:
            return index

def walkSAT(p, max_flips):
    model = randomAssignmentSymbols()
    for i in range(0, max_flips):
        if checkModel(model):
            return model
        index = getRandomFalseClause(model)
        if randint(0, 10) < (p * 10) :
            model = changeValue(model, Sentence[index][randint(0, len(Sentence[index]) - 1)])
        else:
            model = changeMinimumValue(model, index)
  #  return model

def printAssignment(keys):
    target.write('yes\n')
    for i in range(len(keys)):
        target.write('%s %s\n' %(str(keys[i][1]),str(keys[i][3])) )





def main():
    keys = []
    readInput()

    if NoOfTables == '1':

        clauseTab1()

    else:
        clauseDef()



    satisfiabilty = PLResolution(Sentence)
    if satisfiabilty == True:
        model = walkSAT(0.5, 1000)
        for key in model:
           if model[key] == True and '~' not in key:
               keys.append(key)
        keys = sorted(keys)
        printAssignment(keys)

    else:
        target.write('no')

    return 0


if __name__ == '__main__':
    main()
