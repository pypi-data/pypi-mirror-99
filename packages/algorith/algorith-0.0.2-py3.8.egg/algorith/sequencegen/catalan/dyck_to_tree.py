import numpy as np
from algorith.data_structs.trees.bst_node import BstNode


def get_tree(path, start, end):
    if end <= start:
        return None
    targ = path[start]
    x = find_tar(path, targ, start)
    root = BstNode((x-start)/2)
    root.left = get_tree(path, start+1, x-1)
    root.right = get_tree(path, x, end)
    return root


def get_tree2(path):
    root = get_tree(path, 0, len(path)-1)
    # Fix the labels of the keys.
    Tr(root)
    return root


def find_tar(path, targ, start):
    i = start+1
    while path[i] != targ:
        i += 1
    return i


def print_tree(path=[1, 1, 1, 0, 0, 0]):
    for i in range(len(path)):
        if path[i] == 0:
            path[i] = -1
    path = np.concatenate(([0], np.cumsum(path)))
    tn = get_tree2(path)
    return tn


class Tr():
    def __init__(self, x):
        self.i = 1
        self.label_inorder(x)

    def label_inorder(self, x):
        if x is not None:
            self.label_inorder(x.left)
            x.key = self.i
            self.i += 1
            self.label_inorder(x.right)


if __name__ == "__main__":
    # print_tree([1, 1, -1, 1, -1, -1])
    # print_tree([1, 1, -1, -1, 1, -1])
    # print_tree([1, -1, 1, 1, -1, -1])
    print_tree([1, -1, 1, -1, 1, -1])
