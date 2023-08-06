from algorith.utils.math.ncr import ncr
import numpy as np


link = ("https://math.stackexchange.com/questions/3990877\
       /fast-method-to-\
       convert-catalan-path-to-lexicographic\
       -position/3992082#3992082")


def n_catalan(k, t):
    if t < 0:
        return 0
    elif t == 0:
        return 1
    else:
        return abs(ncr(k+2*t-1, t) - ncr(k+2*t-1, t-1))


def n_catalan2(h, t):
    if t < 0:
        return 0
    elif t == 0:
        return 1
    else:
        return abs(ncr(h+t-1, t) - ncr(h+t-1, t-1))

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
            ix += n_catalan2(h, t-1)
            h -= 1
        else:
            t -= 1
    return ix


def ix_to_path(ix, h, t):
    """
    Given an index, returns the Dyck path.
    args:
        ix: The index to be converted.
        t: The number of tails in the path.
        h: The number of heads in the path.
    """
    v = ix
    path = np.zeros(t + h)
    for i in range(t+h):
        tail_paths = n_catalan2(h, t-1)
        if v >= tail_paths:
            path[i] = 1
            h -= 1
            v -= tail_paths
            if h == 0:
                break
        else:
            t -= 1
    return path


if __name__ == "__main__":
    path = ix_to_path(3, 3, 4)
    print(path)
    ix = path_to_ix([1, 0, 1, 0, 1, 0, 0])
    print(ix)
    ix = path_to_ix([1, 0, 1, 1, 0, 0, 0])
    print(ix)
    ix = path_to_ix([1, 1, 0, 0, 1, 0, 0])
    print(ix)
