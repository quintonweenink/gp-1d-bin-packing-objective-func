import random

from experiments.geneticProgramming.node import Node

class TermNode(Node):
    def __init__(self, tree, prev, depth):
        super(TermNode, self).__init__(tree, prev, depth)
        self.value = None

    def copy(self, tree, prev, depth):
        copy = TermNode(tree, prev, depth)
        copy.value = self.value
        return copy

    def grow(self):
        self.assign()

    def full(self):
        self.assign()

    def assign(self):
        self.value = random.randint(0, len(self.tree.termSet) - 1)

    def execute(self):
        return self.tree.termSet[self.value]

    def toString(self):
        return '[' + str(self.depth) + '](' + str(self.index) + ')   ' + str(self.tree.termSet[self.value]) + '\n'