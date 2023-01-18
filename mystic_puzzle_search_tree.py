class NonBinTree:

    def __init__(self, val):
        self.val = val
        self.nodes = []

    def add_node(self, val):
        self.nodes.append(NonBinTree(val))

    def __repr__(self):
        return f"NonBinTree({self.val}): {self.nodes}"


a = NonBinTree(0)
a.add_node(1)
a.add_node(3)
a.add_node(4)
a.nodes[2].add_node(2)

print(a)
