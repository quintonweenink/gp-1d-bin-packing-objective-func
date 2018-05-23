import numpy as np

from experiments.geneticProgramming.tree import Tree
from experiments.geneticProgramming.packing import Packing

from experiments.geneticProgramming.operations import add, multipy, devide, square, power, subtract

class ObjectiveFunction(object):
    def __init__(self):
        self.funcSet = [
            [add, 2, '+'],
            [subtract, 2, '-'],
            [multipy, 2, '*'],
            [devide, 2, '/'],
            [square, 1, '^2'],
            [power, 2, '^'],
        ]
        self.termSet = [None, None, None, None, None, None, None]

        self.population = []
        self.size = 30
        self.maxDepth = 5
        self.minDepth = 2
        self.tournamentSize = 3
        self.generations = 30

        self.problems = [
            ['experiments/problems/bin1data/N1C1W1_A.BPP', 25],
            ['experiments/problems/bin1data/N1C1W1_O.BPP', 32],
            ['experiments/problems/bin1data/N1C1W1_P.BPP', 26],
            ['experiments/problems/bin1data/N1C1W1_T.BPP', 28]
        ]

        self.testproblems = [
            ['experiments/problems/bin1data/N1C1W1_G.BPP', 25],
            ['experiments/problems/bin1data/N1C1W1_K.BPP', 26],
            ['experiments/problems/bin1data/N1C1W1_S.BPP', 28],
            ['experiments/problems/bin1data/N1C1W1_F.BPP', 27]
        ]


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
        # Make the tournament
        random_indicies = np.random.randint(len(self.population), size=self.tournamentSize).tolist()
        tournament = []
        for idx, val in np.ndenumerate(random_indicies):
            tournament.append(self.population[val])

        # Run the tournament
        results = []
        bins = []
        random_problem = np.random.randint(len(self.problems))
        for val in tournament:
            result, bin = self.getFitness(val, self.problems[random_problem])
            results.append(result)
            bins.append(bin)

        # Find the worst or best
        bins = np.array(bins)

        bestTorPos = np.argmin(bins)
        worstTorPos = np.argmax(bins)

        best = self.population[random_indicies[bestTorPos]]
        bestPos = random_indicies[bestTorPos]
        bestResult = bins[bestTorPos]

        worst = self.population[random_indicies[worstTorPos]]
        worstPos = random_indicies[worstTorPos]
        worstResult = bins[worstTorPos]

        return (best, bestPos, bestResult), (worst, worstPos, worstResult), bins / self.problems[random_problem][1]

    def getFitness(self, candidate, problem):
        packing = Packing()

        return packing.run(candidate, problem[0], problem[1])

    def addToList(self, results, arr):
        for i in arr:
            results.append(i)
        return results

    def doCrossover(self):
        results = []
        bestDetails1, worstDetails1, arr = self.tournamentSelector()
        results = self.addToList(results, arr)
        bestDetails2, worstDetails2, arr = self.tournamentSelector()
        results = self.addToList(results, arr)

        c1 = bestDetails1[0].copy()
        c2 = bestDetails2[0].copy()

        c1branch = c1.getBranch(c2)
        c2branch = c2.getBranch(c1)

        c1.setBranch(c2branch)
        c2.setBranch(c1branch)

        self.population[worstDetails1[1]] = c1
        self.population[worstDetails2[1]] = c2

        results = np.array(results)

        return results.mean(), results.std()

    def run(self):
        self.createPopulation()

        meanList = []
        for i in range(self.generations):
            mean, std = self.doCrossover()

            meanList.append(mean)

            print(mean)
            print('('+ str(std) +')')

        meanList = np.array(meanList)
        print("meanlist mean: ", meanList.mean())
        print("meanlist std: ", meanList.std())

        import matplotlib.pyplot as plt

        iterations = []
        for i in range(self.generations):
            iterations.append(i)

        plt.close()

        fig = plt.figure()
        plt.grid(1)
        plt.xlim([0, self.generations])
        plt.ion()
        plt.xlabel('Generations')
        plt.ylabel('Fitness')

        plots = []
        descriptions = []

        plots.append(plt.plot(iterations, meanList, 'b-', linewidth=1, markersize=3)[0])
        descriptions.append("Solve ratio")

        plt.legend(plots, descriptions)
        fig.savefig('Result.png')
        plt.show()

        plt.close()

        results = []
        bins = []
        random_problem = np.random.randint(len(self.testproblems))
        for val in self.population:
            result, bin = self.getFitness(val, self.testproblems[random_problem])
            results.append(result)
            bins.append(bin)

        bins = np.array(bins)
        pos = np.argmin(bins)

        print("testing mean: ", meanList.mean())
        print("testing std: ", meanList.std())

        print(self.population[pos].toString())
        print(pos)
        print(bins[pos], '/', self.problems[random_problem][1])

        return 0

oj = ObjectiveFunction()

oj.run()