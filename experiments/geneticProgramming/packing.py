import pandas as pd
import numpy as np

class Packing(object):
    def getMappedFitness(self, chromosome):
        mappedChromosome = self.items[chromosome]
        spaces = np.zeros(len(mappedChromosome), dtype=int)
        result = np.cumsum(mappedChromosome) - self.BIN_CAPACITY
        index_of_old_bin = 0
        binsRequired = 0
        spacesLeftOpen = []
        consumedSpaces = []
        itemsInBin = []
        while True:
            binsRequired += 1
            max_accumulate = np.maximum.accumulate(np.flipud(result <= 0))
            index_of_new_bin = self.PROBLEM_SIZE - next((idx for idx, val in np.ndenumerate(max_accumulate) if val == True))[0] - 1
            space_left_open = np.abs(result[index_of_new_bin])
            spaces[index_of_new_bin] = space_left_open
            result += space_left_open

            spacesLeftOpen.append(space_left_open)
            consumedSpaces.append(self.BIN_CAPACITY - space_left_open)
            itemsInBin.append(index_of_new_bin - index_of_old_bin)
            index_of_old_bin = index_of_new_bin
            if np.max(result) <= 0:
                break
            result -= self.BIN_CAPACITY
        exec_result = self.fitTree.execute([spacesLeftOpen, consumedSpaces, itemsInBin], [binsRequired, self.BIN_CAPACITY, 1, 2])
        return exec_result, binsRequired

    def toStringMappedFitness(self, chromosome):
        result = np.cumsum(self.problemSet[chromosome]) - self.BIN_CAPACITY
        output = ''
        while True:
            max_accumulate = np.maximum.accumulate(np.flipud(result <= 0))
            index_of_new_bin = self.PROBLEM_SIZE - next((idx for idx, val in np.ndenumerate(max_accumulate) if val == True))[
                0] - 1
            space_left_open = np.abs(result[index_of_new_bin])
            result += space_left_open
            output += '|'
            output += (self.BIN_CAPACITY - space_left_open - 2) * 'X'
            output += '|'
            output += '_' * space_left_open
            output += '\n'
            if np.max(result) <= 0:
                break
            result -= self.BIN_CAPACITY
        return output

    def tournamentSelector(self, population, reverse=False):
        random_indicies = np.random.randint(self.POPULATION_SIZE, size=self.TOURNAMENT_SIZE).tolist()
        tournament = []
        for idx, val in np.ndenumerate(random_indicies):
            tournament.append(population[val])
        results = []
        for val in tournament:
            result, bin = self.getMappedFitness(val)
            results.append(result)

        results = np.array(results)
        if not reverse:
            pos = np.argmin(results)
        else:
            pos = np.argmax(results)
        return population[random_indicies[pos]], random_indicies[pos], results[pos]

    def multipleSwapCrossover(self, p1, p2, swaps=4):
        draws = np.random.randint(self.PROBLEM_SIZE, size=swaps)

        c1 = p1.copy()
        c2 = p2.copy()

        for i, val in enumerate(draws):
            c1item = c1[val]
            c2item = c2[val]
            c1 = np.delete(c1, np.where(c1 == c2item))
            c2 = np.delete(c2, np.where(c2 == c1item))
            c1 = np.insert(c1, val, c2item)
            c2 = np.insert(c2, val, c1item)

        return c1, c2

    def multipleMutator(self, p, swaps=4):
        draws = np.random.randint(self.PROBLEM_SIZE, size=(swaps, 2))

        child = p.copy()

        for i, val in enumerate(draws):
            tmp = child[val[0]]
            child = np.delete(child, val[0])
            child = np.insert(child, val[1], tmp)

        return child

    def tryMutate(self, population):
        draw = np.random.rand()
        if draw < self.MUTATION_RATE:
            p, pos, fit = self.tournamentSelector(population)
            _, kpos, _ = self.tournamentSelector(population, reverse=True)

            c = self.multipleMutator(p, 1)

            population[kpos] = c
        return population

    def tryCrossover(self, population):
        draw = np.random.rand()
        if draw < self.CROSSOVER_RATE:
            p1, p1pos, p1fit = self.tournamentSelector(population)
            p2, p2pos, p2fit = self.tournamentSelector(population)

            if any(p1 != p2):
                _, k1pos, _ = self.tournamentSelector(population, reverse=True)
                _, k2pos, _ = self.tournamentSelector(population, reverse=True)

                c1, c2 = self.multipleSwapCrossover(p1, p2, 3)

                population[k1pos] = c1
                population[k2pos] = c2
            else:
                p1 = self.multipleMutator(p1, swaps=int(self.PROBLEM_SIZE / 5))

                population[p1pos] = p1

        return population

    def run(self, fitTree, binFile, minBins):
        self.problemSet = pd.read_csv(binFile, header=None).values.tolist()

        self.PROBLEM_SIZE = self.problemSet.pop(0)[0]
        self.BIN_CAPACITY = self.problemSet.pop(0)[0]
        self.POPULATION_SIZE = 50
        self.TOURNAMENT_SIZE = 4
        self.GENERATIONS = 250
        self.SAMPLES = 1
        self.SAMPLE_RATE = 50

        self.MUTATION_RATE = 0.3
        self.CROSSOVER_RATE = 1

        self.items = pd.DataFrame(self.problemSet)
        self.items = np.array(self.items[0])

        self.organisedChromosome = np.arange(self.items.size)

        assert self.PROBLEM_SIZE == len(self.items)

        self.fitTree = fitTree

        population = []
        chromosome = np.arange(self.PROBLEM_SIZE)
        for i in range(self.POPULATION_SIZE):
            np.random.shuffle(chromosome)
            population.append(chromosome.copy())

        foundMin = False
        # Mutate and crossover for each generation
        for idx, generation in enumerate(range(self.GENERATIONS)):

            if foundMin == False:
                population = self.tryMutate(population)
                population = self.tryCrossover(population)

            if idx % self.SAMPLE_RATE == 0:
                bins = []
                fitness = []
                for chromosome in population:
                    result, bin = self.getMappedFitness(chromosome)
                    bins.append(bin)
                    fitness.append(result)

                position = int(np.argmin(fitness))
                if bins[position] == minBins:
                    foundMin = True

        bins = []
        fitness = []
        for chromosome in population:
            result, bin = self.getMappedFitness(chromosome)
            bins.append(bin)
            fitness.append(np.array(result))

        position = int(np.argmin(fitness))

        return fitness[position], bins[position]

