import numpy as np

from experiments.geneticProgramming.tree import Tree
from experiments.geneticProgramming.packing import Packing

from experiments.geneticProgramming.operations import add, multipy, devide, square, power, subtract

class ObjectiveFunction(object):
    def __init__(self):
        self.funcSet = [
            [add, 2, '+'],
            [multipy, 2, '*'],
            [devide, 2, '/'],
            [square, 1, '^2'],
            [power, 2, '^'],
            [subtract, 2, '-'],
        ]
        self.termSet = [1, 3, 4]
        self.population = []
        self.size = 30
        self.maxDepth = 5
        self.minDepth = 2
        self.tournamentSize = 3
        self.generations = 50

    def createPopulation(self):
        perlayer = int(self.size / (self.maxDepth - self.minDepth) / 2)

        for x in range(self.minDepth, self.maxDepth):
            for y in range(perlayer):
                fullTree = Tree(x, x, self.funcSet, self.termSet)
                fullTree.full()
                self.population.append(fullTree)

                growTree = Tree(x, x, self.funcSet, self.termSet)
                growTree.grow()
                self.population.append(growTree)

    def tournamentSelector(self, reverse=False):
        random_indicies = np.random.randint(len(self.population), size=self.tournamentSize).tolist()

        tournament = []
        for idx, val in np.ndenumerate(random_indicies):
            tournament.append(self.population[val])

        results = []
        bins = []
        for val in tournament:
            result, bin = self.getFitness(val)
            results.append(result)
            bins.append(bin)

        bins = np.array(bins)
        if not reverse:
            pos = np.argmin(bins)
        else:
            pos = np.argmax(bins)
        return self.population[random_indicies[pos]], random_indicies[pos], bins[pos]

    def getFitness(self, candidate):
        packing = Packing()

        return packing.run(candidate)

    def run(self):
        self.createPopulation()

        for i in range(self.generations):
            p1, p1pos, p1result = self.tournamentSelector()
            p2, p2pos, p2result = self.tournamentSelector()

            _, c1pos, c1result = self.tournamentSelector(reverse=True)
            _, c2pos, c2result = self.tournamentSelector(reverse=True)

            c1 = p1.copy()
            c1branch = c1.getBranch()
            c2 = p2.copy()
            c2branch = c2.getBranch()

            c1.setBranch(c2branch)
            c2.setBranch(c1branch)

            self.population[c1pos] = c1
            self.population[c2pos] = c2

        results = []
        bins = []
        for val in self.population:
            result, bin = self.getFitness(val)
            results.append(result)
            bins.append(bin)

        results = np.array(bins)
        pos = np.argmin(bins)

        print(self.population[pos].toString())
        print(pos)
        print(bins[pos])

        return 0

oj = ObjectiveFunction()

oj.run()