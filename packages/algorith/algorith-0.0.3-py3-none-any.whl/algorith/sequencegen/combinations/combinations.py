import numpy as np
from algorith.leetc.backtracking.combinations import *
from algorith.utils.math.ncr import ncr


def path_to_ix(path):
    """
    path is an array of positions where we got heads.
    See remarkable/math/math/p50
    """
    h = int(sum(path))
    t = len(path) - h
    ix = 0
    for i in range(len(path)):
        if path[i] == 1:
            ix += ncr(h+t-1, t-1)
            h -= 1
        else:
            t -= 1
    return ix


if __name__ == "__main__":
    ix = path_to_ix([0, 0, 0, 1, 1, 1])
    print(ix)
    ix = path_to_ix([0, 0, 1, 0, 1, 1])
    print(ix)
    ix = path_to_ix([0, 0, 1, 1, 0, 1])
    print(ix)
    ix = path_to_ix([1, 0, 1, 0, 1, 0])
    print(ix)
    ix = path_to_ix([1, 0, 1, 1, 0, 0])
    print(ix)
    ix = path_to_ix([1, 1, 0, 0, 1, 0])
    print(ix)
