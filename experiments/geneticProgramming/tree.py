import random

from experiments.geneticProgramming.funcNode import FuncNode


class Tree(object):
    def __init__(self, maxDepth, createDepth, funcSet, termSet):
        self.maxDepth = maxDepth
        self.createDepth = createDepth
        self.root = None

        self.funcSet = funcSet
        self.termSet = termSet
        self.termSetRep = ['S_i', 'F_i', 'W_i', 'F_n', 'C', '1', '1']

        self.index = 0
        self.nodes = []

    def copy(self):
        copy = Tree(self.maxDepth, self.createDepth, self.funcSet, self.termSet)
        copy.root = self.root.copy(copy, None, 0)
        copy.reindex()

        return copy

    def reindex(self):
        self.index = 0
        self.nodes = []

        self.root.reindex(0)

    def grow(self):
        self.root = FuncNode(self, None, 0)
        self.root.grow()
        self.root.reindex(0)

    def full(self):
        self.root = FuncNode(self, None, 0)
        self.root.full()
        self.root.reindex(0)

    def getBranch(self, tree):
        branchIdx = random.randint(0, len(self.nodes) - 1)
        return self.nodes[branchIdx].copy(tree, None, 0)

    def setBranch(self, branch):
        branchIdx = random.randint(0, len(self.nodes) - 1)
        rep = self.nodes[branchIdx]
        prev = rep.prev
        if prev is not None:
            for i, edge in enumerate(prev.edges):
                if edge.index == rep.index:
                    prev.edges[i] = branch

        self.reindex()

    def execute(self, sequences, terms):
        sum = 0
        for y in range(len(sequences[0])):
            self.termSet = terms
            for x in range(len(sequences)):
                self.termSet.append(sequences[x][y])
            sum += self.root.execute()
        return sum

    def toString(self):
        treeStr = 'Number nodes: ' + str(len(self.nodes)) + '\n'
        treeStr += 'Create depth: ' + str(self.maxDepth) + '\n'
        treeStr += 'Max depth: ' + str(self.maxDepth) + '\n'
        return treeStr + self.root.toString()