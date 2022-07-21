import copy
import csv
import random


class Node:
    valueDomain = []
    neighbours = []
    chosenValue = 0

    def __init__(self, vecinList):
        self.neighbours = vecinList


def buildConstraints(domainList):
    maxList = []
    for value in domainList.values():
        for element in value:
            if element not in maxList:
                maxList.append(element)
    result = []
    for i in range(len(maxList) - 1):
        for j in range(i + 1, len(maxList)):
            result.append([maxList[i], maxList[j]])
    return result


class Graph:
    nodeList = {}
    domains = {}
    constraints = []

    def __init__(self, nList, dList, cList):
        self.nodeList = nList
        self.domains = dList
        for key, value in dList.items():
            self.nodeList[key].valueDomain = value
        self.constraints = cList


nodeInstance = {}

with open("nodes.csv") as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        nodeInstance[row[0]] = row[1:]

nodes = {}

for key, value in nodeInstance.items():
    # print(key, value)
    nodes[key] = Node(value)

# for key, value in nodes.items():
# print(key, value)

domainInstance = {}

with open("domain.csv") as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        domainInstance[row[0]] = row[1:]

graph = Graph(nodes, domainInstance, buildConstraints(domainInstance))



def isFinal(graph):
    for key in graph.nodeList:
        if graph.nodeList[key].chosenValue == 0:
            return False
    return True


def unassignedNodes(graph):
    result = []
    for key in graph.nodeList:
        if graph.nodeList[key].chosenValue == 0:
            result.append(key)
    return result


def backtracking(graph):
    if isFinal(graph):
        return graph
    possible = unassignedNodes(graph)
    rand = random.randint(0, len(possible) - 1)
    nextNode = graph.nodeList[possible[rand]]
    print(nextNode.neighbours)
    domainCopy = copy.deepcopy(nextNode.valueDomain)
    while len(domainCopy) > 0:
        rand2 = random.randint(0, len(domainCopy) - 1)
        value = domainCopy.pop(rand2)
        goodToGo = True
        for vecin in nextNode.neighbours:
            if graph.nodeList[vecin].chosenValue == 0:
                continue
            if not ([value, graph.nodeList[vecin].chosenValue] in graph.constraints or [
                graph.nodeList[vecin].chosenValue, value] in graph.constraints):
                goodToGo = False
                break
        if goodToGo:
            nextNode.chosenValue = value
            res = backtracking(graph)
            if res:
                return res
            else:
                nextNode.chosenValue = 0


def checkConstraint(graph, value, nextNode):
    for vecin in nextNode.neighbours:
        if graph.nodeList[vecin].chosenValue == 0 and \
                value in graph.nodeList[vecin].valueDomain \
                and len(graph.nodeList[vecin].valueDomain) == 1:
            return False
    return True


def updateConstraint(graph, value, nextNode):
    for vecin in nextNode.neighbours:
        if graph.nodeList[vecin].chosenValue == 0 and value in graph.nodeList[vecin].valueDomain:
            graph.nodeList[vecin].valueDomain.remove(value)
            graph.domains[vecin] = graph.nodeList[vecin].valueDomain


def forwardChecking2(graph):
    if isFinal(graph):
        return graph
    possible = unassignedNodes(graph)
    rand = random.randint(0, len(possible) - 1)
    nextNode = graph.nodeList[possible[rand]]
    print(nextNode.neighbours)
    domainCopy = copy.deepcopy(nextNode.valueDomain)
    while len(domainCopy) > 0:
        rand2 = random.randint(0, len(domainCopy) - 1)
        value = domainCopy.pop(rand2)
        graphCopy = copy.deepcopy(graph)
        if checkConstraint(graph, value, nextNode):
            updateConstraint(graph, value, nextNode)

            nextNode.chosenValue = value

            res = forwardChecking2(graph)
            if res:
                return res
            else:
                nextNode.chosenValue = 0
                for vecin in nextNode.neighbours:
                    graph.nodeList[vecin] = graphCopy.nodeList[vecin]
                graph.domains = graphCopy.domains


def MRV(graph):
    if isFinal(graph):
        return graph
    possible = unassignedNodes(graph)
    # rand = random.randint(0, len(possible) - 1)
    possible = sorted(possible, key=lambda x: len(graph.nodeList[x].valueDomain))
    nextNode = graph.nodeList[possible.pop(0)]
    print(nextNode.neighbours)
    domainCopy = copy.deepcopy(nextNode.valueDomain)
    while len(domainCopy) > 0:
        rand2 = random.randint(0, len(domainCopy) - 1)
        value = domainCopy.pop(rand2)
        graphCopy = copy.deepcopy(graph)
        if checkConstraint(graph, value, nextNode):
            updateConstraint(graph, value, nextNode)

            nextNode.chosenValue = value

            res = forwardChecking2(graph)
            if res:
                return res
            else:
                nextNode.chosenValue = 0
                for vecin in nextNode.neighbours:
                    graph.nodeList[vecin] = graphCopy.nodeList[vecin]
                graph.domains = graphCopy.domains




if __name__ == "__main__":
    MRV(graph)
    for node in graph.nodeList:
        print(graph.nodeList[node].chosenValue)
