from algorith.sequencegen.catalan.next_dyck import ix_to_path, n_catalan2
from algorith.sequencegen.catalan.dyck_to_tree import print_tree


def ix_to_tree(ix, n):
    """
    Converts index to lexicographic binary search tree.
    args:
        ix: The index.
        n: The number of nodes in the tree.
    """
    path = ix_to_path(ix, n, n+1)
    # The last entry is a redundant tail. So, remove it.
    tree_nd = print_tree(path[:len(path)-1])
    return tree_nd, path


def print_all_trees(n=3):
    n_trees = n_catalan2(n, n+1)
    for ix in range(n_trees):
        tn, path = ix_to_tree(ix, n)
        print("---n="+str(ix)+"---")
        tn.display()
        print(path)


class Tr1():
    def __init__(self, root):
        self.root = root
        self.arr = []
        self.tree_to_array(root)

    def tree_to_array(self, tn):
        """
        Converts tree to leetcode array.
        """
        if tn is not None:
            self.arr.append(tn.key)
        else:
            self.arr.append(None)
        if tn is not None and\
           (tn.left is not None or tn.right is not None):
            self.tree_to_array(tn.left)
            self.tree_to_array(tn.right)


if __name__ == "__main__":
    tree_nd = ix_to_tree(2, 3)
    tree_nd.display()
    # It's not the middle tree.
    # total trees are 1430.
    tn = ix_to_tree(916, 8)
    tn.display()
    tn = ix_to_tree(280, 7)
    tn.display()
    # For n=6 its 58, 86, 89, 90.
