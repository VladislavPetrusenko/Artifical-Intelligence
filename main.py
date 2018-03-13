import operator
import math

class MyNode:
    def __init__ (self, name, x, y):
        self.name = name
        self.x = float(x)   # changes the string to a float
        self.y = float(y)   # changes the string to a float
        self.connection = []

myNetwork = {}      # A dictionary


dataFile = open('locations2016.csv', 'r')   # Open a file and stores it in variable, r for read authorisation
for dataLine in dataFile.readlines()[1:]:   # [1:] Skips the first line
    datastring = dataLine[:-1]              # [:-1} Skips the last sign in row (\n)

    datastring1 = datastring.split(';')     # Splits the strings at ;
    # name, x, y = datastring.split(';')    # Alternative to datastring 1 =....

    Node = MyNode(datastring1[0], datastring1[1], datastring1[2])   # Saves the datastrings of the split accordingly to class MyNode in node
    # Node = MyNode(name, x, y)                                     # Alternativ way to save the strings according to class MyNode

    myNetwork[datastring1[0]] = Node    # Connects the nodes information to the name of the node (name as referens/callsign)
    # myNetwork[name] = Node            # Alternative way to connect the nodes information to the name of the node (name as referens/callsign)

    # print(Node.name, Node.x, Node.y)  # Just a print for confirmation of data

dataFile.close()    # Closes the file
del dataFile        # Deletes the variable (we already have all its information


dataFile = open('connections2016.csv', 'r')     # Open a file and stores it in variable, r for read authorisation
for dataLine in dataFile.readlines()[1:]:       # [1:] Skips the first line
    datastring = dataLine[:-1]                  # [:-1} Skips the last sign in row (\n)

    datastring1 = datastring.split(';')         # Splits the strings at ;

    From, To = datastring1  # Saves the forst value as From and the second as To
    myNetwork[From].connection.append(myNetwork[To])

    # for i in myNetwork:               #For loop for myNetwork as a list and not as a dictionary
    #     if (datastring1[0] == i.name):
    #         From = i
    #     if (datastring1[1] == i.name):
    #         To = i
    # From.connection.append(To)

dataFile.close()
del dataFile

# Prints name of the connections in each node
# for obj in Node:
#     print(obj.name, ':')
#     for obj2 in obj.connection:
#         print('-', obj2.name)


def iterativeDeepeningSearch(startNode, stopNode):  # strings as parameters
    depth = 0
    begin = myNetwork[startNode]
    end = myNetwork[stopNode]
    while True:
        depth += 1
        result = depthLimitedSearch(begin, end, depth)
        if result != False:
            for obj in result:
                print(obj.name)
            return result


def depthLimitedSearch(startNode, stopNode, maxDepth):
    frontier = [startNode]
    depthList = {}
    depthList[startNode] = 0
    cameFrom = {}
    visitedList = []

    while True:
        if not frontier:
            return False
        node = frontier[0]
        frontier.remove(node)
        visitedList.append(node)
        if not depthList[node] > maxDepth:
            if node == stopNode:
                return reconstruct(cameFrom, startNode, stopNode)
            for nextNode in node.connection:
                if nextNode not in visitedList and nextNode not in frontier:
                    #frontier.append(nextNode)
                    frontier.insert(0, nextNode)
                    depthList[nextNode] = depthList[node] + 1
                    cameFrom[nextNode] = node


def reconstruct(cameFrom, startNode, stopNode):  # s13
    path = []
    node = stopNode
    while True:
        if node == startNode:
            path.append(node)           #Adds the startNode to the end of the list path
            path.reverse()              #Reverses th path list.
            return path
#            return path.__reversed__() # Alternative: Returns and prints the reconstructed list backwards
        else:
            path.append(node)
            node = cameFrom[node]


def heuristic(nextNode, stopNode):  # Calculates the hyp between the next node and end node
    hX = nextNode.x - stopNode.x
    hY = nextNode.y - stopNode.y
    hX = math.pow(hX, 2)
    hY = math.pow(hY, 2)
    hH = math.sqrt(hX+hY)
    return(hH)


def bestNode(frontier, stopNode, heuristicCost):
    score = {}
    for obj in frontier:
        score[obj] = (heuristicCost[obj]+heuristic(obj, stopNode))
    return min(frontier, key=lambda x: score[x])


def aStar(startNode, stopNode):
    begin = myNetwork[startNode]
    end = myNetwork[stopNode]
    frontier = [begin]
    cameFrom = {}
    costToNode = {begin : 0}
    visitedList = []

    while True:
        if not frontier:
            return False
        currentNode = bestNode(frontier, end, costToNode)
        frontier.remove(currentNode)
        visitedList.append(currentNode)

        if currentNode == end:
            path = reconstruct(cameFrom, begin, end)
            for obj in path:
                print(obj.name)
            return True
#            return reconstruct(cameFrom, begin, end)

        else:
            for nextNode in currentNode.connection:
                if nextNode not in visitedList and nextNode not in frontier:
                    frontier.append(nextNode)
                    cameFrom[nextNode] = currentNode
                    costToNode[nextNode] = costToNode[currentNode] + heuristic(currentNode, nextNode)

                if nextNode in visitedList:
                    if (costToNode[currentNode] + heuristic(currentNode, nextNode)) < costToNode[nextNode]:
                        cameFrom[nextNode] = currentNode
                        costToNode[nextNode] = costToNode[currentNode] + heuristic(currentNode, nextNode)
                        frontier.append(nextNode)
                        visitedList.remove(nextNode)

                if nextNode in frontier:
                    if (costToNode[currentNode] + heuristic(currentNode, nextNode)) < costToNode[nextNode]:
                        cameFrom[nextNode] = currentNode
                        costToNode[nextNode] = costToNode[currentNode] + heuristic(currentNode, nextNode)

# Function for input for the iterative deepening search-function

print('')
Start = input('Enter start: ')
End = input('Enter end: ')

print('\nIterative Deepening Search')
print('--------------------------')
iterativeDeepeningSearch(Start, End)
print('--------------------------')

# Function for input for the iterative deepening search-function
print('\nA* Search')
print('--------------------------')
aStar(Start, End)
print('--------------------------')
