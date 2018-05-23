

class Node(object):
    def __init__(self, tree, prev, depth):
        self.tree = tree
        self.prev = prev
        self.depth = depth
        self.index = None

    def copy(self, tree, prev, depth):
        raise NotImplemented

    def reindex(self, depth):
        self.depth = depth
        self.index = self.tree.index
        self.tree.index += 1
        self.tree.nodes.append(self)

    def grow(self):
        raise NotImplemented

    def full(self):
        raise NotImplemented

    def execute(self):
        raise NotImplemented