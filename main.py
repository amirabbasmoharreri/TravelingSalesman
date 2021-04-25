import math
import operator
import time
import matplotlib.pyplot as plt
import numpy as np
from random import randint


class Point():

    def __init__(self, x, y, color='#4ca3dd', size=50, add_coordinates=True):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.add_coordinates = add_coordinates
        self.y_offset = 0.2
        self.items = np.array([x, y])
        self.len = 2

    def __getitem__(self, index):
        return self.items[index]

    def __str__(self):
        return "Point(%.2f,%.2f)" % (self.x, self.y)

    def __repr__(self):
        return "Point(%.2f,%.2f)" % (self.x, self.y)

    def __len__(self):
        return self.len

    def draw(self):
        plt.scatter([self.x], [self.y], color=self.color, s=self.size)

        # Add the coordinates if asked by user
        if self.add_coordinates:
            plt.text(
                self.x, self.y + self.y_offset,
                        "(%.1f,%.1f)" % (self.x, self.y),
                horizontalalignment='center',
                verticalalignment='bottom',
                fontsize=12
            )


class City():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + x + ", " + y + ")"


class Coromozom():
    destination = 0

    def __init__(self, array):
        self.array = array
        self.destination = None

    def __setitem__(self, value):
        self.destination = value


###   Correct

def population(n):
    p = []
    num = n * 5
    counterpop = 0
    while counterpop < num:
        history = []
        counter = 0
        while counter < n:
            adad = randint(0, n - 1)
            if not (adad in history):
                history.append(adad)
                counter += 1
                # print(counter)
        crom = Coromozom(history)
        p.append(crom)
        counterpop += 1

    # print("Population")
    # print(p)
    return p


def fitnessFunction(lists, city):
    croms = computingTotalDestination(lists, city)
    croms.sort(key=operator.attrgetter('destination'))
    return croms


###      Correct

def crossover(n):
    ra = []
    for i in range(2):
        a = randint(0, n - 1)
        if not (a in ra):
            ra.append(a)
    rand = (min(ra), max(ra))

    # print("Crossover  numbers")
    # print(rand)

    return rand


def muta(n):
    randindex = []
    for i in range(n):
        a = randint(0, n - 1)
        if not (a in randindex):
            if len(randindex) == 2:
                break
            randindex.append(a)
    return randindex

###   Correct

def parentSelection(allpop, rate):
    p = []
    history = []
    popsize = len(allpop)
    pecent = (rate / 100)
    crosssize = int(popsize * pecent)

    parents = []
    i = 0
    while i < 2:
        fmparent = []
        counter = 0
        while counter < crosssize:
            num = randint(0, popsize - 1)
            if not (num in history):
                history.append(num)
                fmparent.append(num)
                counter += 1
        parents.append(fmparent)
        i += 1
    j = 0
    while j < 2:
        c = []
        for i in range(0, crosssize):
            c.append(allpop[parents[j][i]])
        p.append(c)
        j += 1

    # print("Parent Selection")
    # print(p)
    return p


def surviveSelection(allpop, n):
    allpop.sort(key=operator.attrgetter('destination'))
    num = n * 5
    percent = (50 / 100)
    popsize = int(len(allpop) * percent)
    best = allpop[0:popsize + 1]
    while len(best) < num:
        rand = randint(popsize + 1, len(allpop) - 1)
        best.append(allpop[rand])
    return best


###   Correct

def mutation(childs, rate):
    popsize = len(childs)
    lens = len(childs[0].array)
    randcrom = []
    randindex = []
    pecent = (rate / 100)
    musize = int(popsize * pecent)
    # random coromozoms for mutation
    for i in range(musize):
        randcrom.append(randint(0, popsize - 1))

    for i in randcrom:
        randindex = muta(lens)
        item1 = childs[i].array[randindex[0]]
        item2 = childs[i].array[randindex[1]]
        childs[i].array[randindex[0]] = item2
        childs[i].array[randindex[1]] = item1

    return childs


###   Correct

def computingDestination2x2(point1, point2):
    return math.sqrt(((point1[0] - point2[0]) ** 2) + ((point1[1] - point2[1]) ** 2))


###   Correct

def computingTotalDestination(croms, city):
    sum1 = 0
    sumlist = []
    for j in range(len(croms)):
        if not (croms[j].destination == 0):
            for i in range(len(croms[0].array) - 1):
                index11 = croms[j].array[i]
                index12 = croms[j].array[i + 1]
                point1 = (city[index11].x, city[index11].y)
                point2 = (city[index12].x, city[index12].y)
                # total of destination cromozom
                sum1 += computingDestination2x2(point1, point2)
            croms[j].destination = sum1

    return croms


def recombination(allpop, parent):
    lens = len(parent[0][0].array)
    #cross = crossover(lens)
    recomsize = len(parent[0])
    childs = []
    for j in range(0, recomsize):
        cross = crossover(lens)
        child1 = []
        child2 = []
        for i in range(0, lens):
            child1.append(-1)
            child2.append(-1)
        p1 = parent[0][j].array
        p2 = parent[1][j].array

        # creating middle of cromozom childs

        for i in range(cross[0], cross[1] + 1):
            child1[i] = p1[i]
            child2[i] = p2[i]

        # print("central recombination")
        # print(child1)
        # print(child2)

        # creating next to the childs cromozom

        # creating left-side
        for i in range(0, cross[0]):
            if not p2[i] in child1:
                child1[i] = p2[i]
            if not p1[i] in child2:
                child2[i] = p1[i]

        # print("left recombination")
        # print(child1)
        # print(child2)

        # creating right-side
        for i in range(cross[1] + 1, lens):
            if not p2[i] in child1:
                child1[i] = p2[i]
            if not p1[i] in child2:
                child2[i] = p1[i]

        # print("right recombination")
        # print(child1)
        # print(child2)

        # completing childs
        for i in range(0, lens):

            index1 = [j for j in range(len(child2)) if child1[j] == -1]
            index2 = [j for j in range(len(child2)) if child2[j] == -1]
            # print(index1)
            # print(index2)
            if not p2[i] in child1:
                if not (len(index1) == 0):
                    child1[index1[0]] = p2[i]
            if not p1[i] in child2:
                if not (len(index2) == 0):
                    child2[index2[0]] = p1[i]

        childs.append(Coromozom(child1))
        childs.append(Coromozom(child2))

    return childs


def addchildstopopulation(allpop, childs):
    for i in range(0, len(childs)):
        allpop.append(childs[i])
    return allpop


def showCardesianPage(bestcrom):
    x = []
    y = []
    for i in range(0, len(bestcrom)):
        x.append(list_cities[bestcrom[i]].x)
        y.append(list_cities[bestcrom[i]].y)

    plt.scatter(x, y, s=100)
    plt.grid()
    plt.plot(x, y)
    plt.title("Cities")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()
    return


def showfitness(lists):
    plt.plot(lists)
    plt.title("ّFitness Function = " + str(lists[len(lists)-1]))
    plt.ylabel("Destination")
    plt.xlabel("Iteration")
    plt.show()
    return


##################### starting app from here  ######################


list_cities = []
list_x = [26,94,24,81,87,96,0,90,37,67,32,92,39,86,93,95,85,28,34,30,46,98,91,17,15,83]
list_y = [33,41,69,19,97,79,77,46,18,96,80,5,90,28,43,64,8,89,40,80,94,54,61,2,13,80]
bestcrom = []
bestfitness = []
start=0
print("Do you want calculate with random (1) city or with list of city (2)? ")
w = int(input())
if w == 1:
    print("enter number of cities 'minimum 10' ")
    while True:
        num = int(input())
        if num >= 10:
            break
        else:
            print("try again")

    # intializing Coordinates of cities with random
    start = time.time()
    for j in range(num):
        x = randint(0, 100)
        y = randint(0, 100)
        city = City(x, y)
        list_cities.append(city)
else:
    start = time.time()
    num = len(list_x)
    for i in range(0,len(list_x)):
        city = City(list_x[i],list_y[i])
        list_cities.append(city)

print("input mutation rates")
mutationRate = int(input())

print("input crossover rates")
crossRate = int(input())




print("list of Cities")
print(list_cities)

# ADT allgorithm

i = 0
j = 0
fit1 = 100
fit2 = 200
allPopulation = population(num)
allPopulation = fitnessFunction(allPopulation, list_cities)
bestfitness.append(allPopulation[0].destination)
evaluate = abs(fit1 - fit2)
while j < 800:
    if evaluate < 1:
        j += 1
    else:
        j = 0
    print("Generation " + str(i) + "  Fitness: " + str(fit2) + "  Count fitness not change: " + str(j))
    parent = parentSelection(allPopulation, crossRate)
    childs = recombination(allPopulation, parent)
    childs = mutation(childs, mutationRate)
    childs = fitnessFunction(childs, list_cities)
    allPopulation = addchildstopopulation(allPopulation, childs)
    allPopulation = surviveSelection(allPopulation, num)
    bestcrom.append(allPopulation[0])
    bestfitness.append(allPopulation[0].destination)
    fit2 = bestfitness[len(bestfitness) - 1]
    if len(bestfitness) > 1:
        fit1 = bestfitness[len(bestfitness) - 2]
    evaluate = abs(fit1 - fit2)
    i += 1
bestcrom.sort(key=operator.attrgetter('destination'))
showCardesianPage(bestcrom[0].array)
showfitness(bestfitness)
end = time.time()
print("Runtime of the program is " + str(end-start) + " seconds")