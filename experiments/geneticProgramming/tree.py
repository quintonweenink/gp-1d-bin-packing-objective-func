import random

from experiments.geneticProgramming.funcNode import FuncNode

class Tree(object):
    def __init__(self, maxDepth, createDepth, funcSet, termSet):
        self.maxDepth = maxDepth
        self.createDepth = createDepth
        self.root = None

        self.funcSet = funcSet
        self.termSet = termSet

        self.index = 0
        self.nodes = []

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

    def crossover(self, branch):
        branchIdx = random.randint(0, len(self.nodes) - 1)
        self.nodes[branchIdx] = branch

    def getBranch(self):
        branchIdx = random.randint(0, len(self.nodes) - 1)
        return self.nodes[branchIdx].copy(None, 0)

    def execute(self):
        return self.root.execute()

    def toString(self):
        treeStr = 'Number nodes: ' + str(len(self.nodes)) + '\n'
        treeStr += 'Create depth: ' + str(self.maxDepth) + '\n'
        treeStr += 'Max depth: ' + str(self.maxDepth) + '\n'
        return treeStr + self.root.toString()