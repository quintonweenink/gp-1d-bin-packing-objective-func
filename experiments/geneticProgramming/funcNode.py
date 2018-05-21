import random

from experiments.geneticProgramming.node import Node
from experiments.geneticProgramming.termNode import TermNode

class FuncNode(Node):
    def __init__(self, tree, prev, depth):
        super(FuncNode, self).__init__(tree, prev, depth)
        self.function = None
        self.numEdges = None
        self.funcStr = None
        self.edges = []

    def copy(self, prev, depth):
        copy = FuncNode(self.tree, prev, depth)
        copy.function = self.function
        copy.numEdges = self.numEdges
        copy.funcStr = self.funcStr
        for edge in self.edges:
            copy.edges.append(edge.copy(copy, depth + 1))

        return copy

    def reindex(self, depth):
        super(FuncNode, self).reindex(depth)
        for edge in self.edges:
            edge.reindex(depth + 1)

    def grow(self):
        self.assignFunc()
        if self.depth == self.tree.createDepth - 1:
            for i in range(self.numEdges):
                self.addTermNode()
        else:
            for i in range(self.numEdges):
                draw = random.random()
                if draw > 0.3:
                    funcNode = FuncNode(self.tree, self, self.depth + 1)
                    funcNode.grow()
                    self.edges.append(funcNode)
                else:
                    self.addTermNode()

    def full(self):
        self.assignFunc()
        if self.depth == self.tree.createDepth - 1:
            for i in range(self.numEdges):
                self.addTermNode()
        else:
            for i in range(self.numEdges):
                funcNode = FuncNode(self.tree, self, self.depth + 1)
                funcNode.full()
                self.edges.append(funcNode)


    def assignFunc(self):
        funcIdx = random.randint(0, len(self.tree.funcSet) - 1)
        self.function = self.tree.funcSet[funcIdx][0]
        self.numEdges = self.tree.funcSet[funcIdx][1]
        self.funcStr = self.tree.funcSet[funcIdx][2]

    def addTermNode(self):
        termNode = TermNode(self.tree, self, self.depth + 1)
        termNode.full()
        self.edges.append(termNode)

    def execute(self):
        results = [i.execute() for i in self.edges]
        return self.function(results)

    def toString(self):
        treeStr = '[' + str(self.depth) + '](' + str(self.index) + ')   ' + self.funcStr + '\t' + self.edges[0].toString()
        for i, edge in enumerate(self.edges):
            if not i == 0:
                treeStr += '\t' * (self.depth + 1)
                treeStr += self.edges[i].toString()
        return treeStr