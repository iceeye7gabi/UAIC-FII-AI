import copy
import math
import random
import time

class Bila:
    culoare = -1

    def __init__(self, color):
        self.culoare = color



class Joc:
    colorCount = 0 # n
    ballCount = 0 # m
    chosenLength = 0 # k
    ballList = []
    chosenBalls = []
    currentPick = []
    stepCount = 0

    def __init__(self, n, m, k):
        self.colorCount = n
        self.ballCount = m
        self.chosenLength = k
        for i in range(0, m):
            for j in range(0, n):
                self.ballList.append(Bila(j))


    def initRandomPick(self):
        ballsListCopy = copy.deepcopy(self.ballList)
        for i in range(0, self.chosenLength):
            rand = random.randint(0, len(ballsListCopy) - 1)
            self.chosenBalls.append(ballsListCopy[rand])
            ballsListCopy.remove(ballsListCopy[rand])

def isFinal(game):
    finalRound = False
    if game.stepCount >= 2 * game.colorCount:
       finalRound = True
    for i in range(0, len(game.chosenBalls)):
        if game.currentPick[i].culoare != game.chosenBalls[i].culoare:
            if finalRound:
                return 1
            else:
                return 0
    return 2

def compareColors(game):
    matches = 0
    for i in range(0, len(game.currentPick)):
        if game.currentPick[i].culoare == game.chosenBalls[i].culoare:
            matches += 1
    return matches


def compareColorsList(game, combination):
    matches = 0
    for i in range(0, len(game.currentPick)):
        if combination[i].culoare == game.chosenBalls[i].culoare:
            matches += 1
    return matches

def possibleCombinationCount(joc, expectedK, combinatie):
    if expectedK != compareColorsList(joc, combinatie):
        return -1
    i = len(combinatie) - expectedK
    return i * (joc.ballCount - 1)


def possibleValues(joc, ignoreValue, pick):
    newList = [x for x in range(0, joc.colorCount) if x != ignoreValue]
    filteredList = [x for x in newList if pick.count(x) < joc.ballCount]
    if len(filteredList) > 0:
        position = random.randint(0, len(filteredList) - 1)
        return Bila(filteredList[position])
    return Bila(-1)

def randomPick(joc):
    ballListCopy = copy.deepcopy(joc.ballList)
    newList = []
    for i in range(0, joc.chosenLength):
        rand = random.randint(0, len(ballListCopy) -1)
        newList.append(ballListCopy[rand])
        ballListCopy.remove(ballListCopy[rand])
    return newList

def generatePicks(joc, previousResults):
    #print(previousResults
    maxK = 0
    if len(previousResults) > 0:
        maxK = previousResults[0][0]
    bestPreviousPick = []
    previousCombinations = []

    for lst in previousResults:
        previousCombinations.append(lst[1])
        if lst[0] > maxK:
            maxK = lst[0]
            bestPreviousPick = lst[1]

    generatedPicks = []

    while len(generatedPicks) < (
            joc.colorCount ** (joc.chosenLength - maxK) * (math.comb(joc.chosenLength, joc.chosenLength - maxK))/2):
        if len(previousResults) == 0 or len(bestPreviousPick) == 0:
            newPick = randomPick(joc)
        else:
            checkedPositions = []
            newPick = copy.deepcopy(bestPreviousPick)

            while len(checkedPositions) != len(bestPreviousPick) - maxK:
                position = random.randint(0, len(bestPreviousPick) -1)
                if position not in checkedPositions:
                    checkedPositions.append(position)
                    newPick[position] = possibleValues(joc, newPick[position], newPick)
                else:
                    continue
        available = True
        for biluta in newPick:
            if biluta.culoare == -1:
                available = False
                break
        if newPick not in previousCombinations and available:
            if newPick not in generatedPicks:
                generatedPicks.append(newPick)
    return generatedPicks


def minimax(joc, depth, previousResults, alegere, expectedK, isFirst):
    if depth == 0:
        return possibleCombinationCount(joc, expectedK, alegere)
    if depth % 2 == 1:
        value = -1000
        for i in range(0, joc.chosenLength + 1):
            value = max(value, minimax(joc, depth - 1, previousResults, alegere, i, False))
        return value
    else:
        bestpick = []
        value = 10000
        previousValue = joc.colorCount * joc.chosenLength
        for pick in generatePicks(joc, previousResults):
            newPreviousResults = copy.deepcopy(previousResults)
            newPreviousResults.append([compareColorsList(joc, pick), pick])
            previousValue = value
            value = min(value, minimax(joc, depth -1, newPreviousResults, pick, -100, False))
            available = False
            previousCombinations = []
            for lst in previousResults:
                previousCombinations.append(lst[1])
            if value != previousValue and not pick in previousCombinations:
                previousValue = value
                bestpick = pick
        return bestpick

def alphaBeta(joc, depth, previousResults, alegere, expectedK, alfa, beta, isFirst):
    if depth == 0:
        return possibleCombinationCount(joc, expectedK, alegere)
    if depth % 2 == 1:
        value = -1000
        for i in range(0, joc.chosenLength + 1):
            value = max(value, alphaBeta(joc, depth - 1, previousResults, alegere, i, alfa, beta, False))
            if value > beta:
                break
            alfa = max(alfa, value)
        return value
    else:
        bestpick = []
        value = 10000
        previousValue = joc.colorCount * joc.chosenLength
        for pick in generatePicks(joc, previousResults):
            newPreviousResults = copy.deepcopy(previousResults)
            newPreviousResults.append([compareColorsList(joc, pick), pick])
            previousValue = value
            value = min(value, alphaBeta(joc, depth - 1, newPreviousResults, pick, -100, alfa, beta, False))
            if value < alfa:
                break
            beta = min(beta, value)
            available = False
            previousCombinations = []
            for lst in previousResults:
                previousCombinations.append(lst[1])
            if value != previousValue and not pick in previousCombinations:
                previousValue = value
                bestpick = pick
        return bestpick




joc = Joc(3,5,4)
joc.initRandomPick()

for bila in joc.chosenBalls:
    print(bila.culoare)

start_time = time.time()
cond = 0
previousResults = []
while cond == 0:
    lista = alphaBeta(joc, 2, previousResults, [], 69, -10000, 10000, True)
    print("------")
    joc.currentPick = lista
    joc.stepCount += 1
    for bila in lista:
        print(bila.culoare)
    print("scor = " + str(compareColors(joc)))
    cond = isFinal(joc)
    previousResults.append([compareColors(joc), lista])

if cond == 1:
    print("Jucatorul A a castigat")
else:
    if cond == 2:
        print("Jucatorul B a castigat")


print("Timp alphabeta: " + str(time.time() - start_time))



joc2 = Joc(3,5,4)
joc2.chosenBalls = []
joc2.initRandomPick()

for bila in joc2.chosenBalls:
    print(bila.culoare)

start_time = time.time()
cond2 = 0
previousResults2 = []
while cond2 == 0:
    lista = minimax(joc2, 2, previousResults2, [], 69, True)
    print("------")
    joc2.currentPick = lista
    joc2.stepCount += 1
    for bila in lista:
        print(bila.culoare)
    print("scor = " + str(compareColors(joc2)))
    cond2 = isFinal(joc2)
    previousResults.append([compareColors(joc2), lista])

if cond2 == 1:
    print("Jucatorul A a castigat")
else:
     print("Jucatorul B a castigat")


print("Timp minimax: " + str(time.time() - start_time))


