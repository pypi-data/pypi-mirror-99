import operator as op
from functools import reduce

## Taken from: https://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function-in-python

def ncr(n, r):
    if r<0:
        return 0
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom  # or / in Python 2

def tst():
    print(ncr(4,2))

if __name__=="__main__":
    tst()
