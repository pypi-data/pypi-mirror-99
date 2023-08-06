import numpy as np
from algorith.sequencegen.catalan.next_tree import ix_to_tree
from algorith.sequencegen.catalan.next_dyck import n_catalan2


# Graph that makes me uncomfortable: Remarkable/math/math/pg56.
# The node 3 causes the path to go below the level
# and so is not a Dyck path.
# See also: https://cs.stackexchange.com/questions/136923

class TreeToDyck():
    def __init__(self, tree_node, n):
        # Initially create an array of 2n ones. All steps are set to "up".
        self.path = np.ones(2*n)
        # Now insert downs at appropriate places.
        self.tree_to_dyck(tree_node, 1)

    def tree_to_dyck(self, tree_node, start):
        if tree_node is None:
            return
        # Go down. Bear in mind the "path" array is 0-indexed.
        self.path[start+2*tree_node.key-2] = -1
        self.tree_to_dyck(tree_node.left, start+1)
        self.tree_to_dyck(tree_node.right, start)


def tst():
    nn = n_catalan2(6, 7)
    ix = np.random.choice(nn)
    print(ix)
    node, path = ix_to_tree(ix, 6)
    node.display()
    print(path)
    td = TreeToDyck(node, 6)
    print(td.path)


if __name__ == "__main__":
    tst()
