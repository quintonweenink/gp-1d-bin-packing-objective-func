binFile = 'experiments/problems/bin1data/N1C1W1_A.BPP'
minBins = 26

import pandas as pd
import numpy as np

problemSet = pd.read_csv(binFile, header=None).values.tolist()

PROBLEM_SIZE = problemSet.pop(0)[0]
BIN_CAPACITY = problemSet.pop(0)[0]
POPULATION_SIZE = 50
TOURNAMENT_SIZE = 4
GENERATIONS = 500
SAMPLES = 1
SAMPLE_RATE = 50

MUTATION_RATE = 0.3
CROSSOVER_RATE = 1

items = pd.DataFrame(problemSet)
items = np.array(items[0])

organisedChromosome = np.arange(items.size)

assert PROBLEM_SIZE == len(items)

class Packing(object):
    def getMappedFitness(self, chromosome):
        mappedChromosome = items[chromosome]
        spaces = np.zeros(len(mappedChromosome), dtype=int)
        result = np.cumsum(mappedChromosome) - BIN_CAPACITY
        binsRequired = 0
        spacesLeftOpen = []
        while True:
            binsRequired += 1
            max_accumulate = np.maximum.accumulate(np.flipud(result <= 0))
            index_of_new_bin = PROBLEM_SIZE - next((idx for idx, val in np.ndenumerate(max_accumulate) if val == True))[
                0] - 1
            space_left_open = np.abs(result[index_of_new_bin])
            spaces[index_of_new_bin] = space_left_open
            result += space_left_open
            spacesLeftOpen.append(space_left_open)
            if np.max(result) <= 0:
                break
            result -= BIN_CAPACITY
        result = self.fitTree.execute(spacesLeftOpen, [binsRequired, BIN_CAPACITY, 4])
        return result, binsRequired

    def toStringMappedFitness(self, chromosome):
        result = np.cumsum(problemSet[chromosome]) - BIN_CAPACITY
        output = ''
        while True:
            max_accumulate = np.maximum.accumulate(np.flipud(result <= 0))
            index_of_new_bin = PROBLEM_SIZE - next((idx for idx, val in np.ndenumerate(max_accumulate) if val == True))[
                0] - 1
            space_left_open = np.abs(result[index_of_new_bin])
            result += space_left_open
            output += '|'
            output += (BIN_CAPACITY - space_left_open - 2) * 'X'
            output += '|'
            output += '_' * space_left_open
            output += '\n'
            if np.max(result) <= 0:
                break
            result -= BIN_CAPACITY
        return output

    def tournamentSelector(self, population, reverse=False):
        random_indicies = np.random.randint(POPULATION_SIZE, size=TOURNAMENT_SIZE).tolist()
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
        draws = np.random.randint(PROBLEM_SIZE, size=swaps)

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
        draws = np.random.randint(PROBLEM_SIZE, size=(swaps, 2))

        child = p.copy()

        for i, val in enumerate(draws):
            tmp = child[val[0]]
            child = np.delete(child, val[0])
            child = np.insert(child, val[1], tmp)

        return child

    def tryMutate(self, population):
        draw = np.random.rand()
        if draw < MUTATION_RATE:
            p, pos, fit = self.tournamentSelector(population)
            _, kpos, _ = self.tournamentSelector(population, reverse=True)

            c = self.multipleMutator(p, 1)

            population[kpos] = c
        return population

    def tryCrossover(self, population):
        draw = np.random.rand()
        if draw < CROSSOVER_RATE:
            p1, p1pos, p1fit = self.tournamentSelector(population)
            p2, p2pos, p2fit = self.tournamentSelector(population)

            if any(p1 != p2):
                _, k1pos, _ = self.tournamentSelector(population, reverse=True)
                _, k2pos, _ = self.tournamentSelector(population, reverse=True)

                c1, c2 = self.multipleSwapCrossover(p1, p2, 3)

                population[k1pos] = c1
                population[k2pos] = c2
            else:
                p1 = self.multipleMutator(p1, swaps=int(PROBLEM_SIZE / 5))

                population[p1pos] = p1

        return population

    def run(self, fitTree):

        self.fitTree = fitTree

        population = []
        chromosome = np.arange(PROBLEM_SIZE)
        for i in range(POPULATION_SIZE):
            np.random.shuffle(chromosome)
            population.append(chromosome.copy())

        foundMin = False
        # Mutate and crossover for each generation
        for idx, generation in enumerate(range(GENERATIONS)):

            if foundMin == False:
                population = self.tryMutate(population)
                population = self.tryCrossover(population)

            if idx % SAMPLE_RATE == 0:
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
        print('Best in generation: ', bins[position], fitness[position])

        return fitness[position], bins[position]

