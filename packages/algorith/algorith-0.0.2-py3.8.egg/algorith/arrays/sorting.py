import numpy as np
from importlib import reload


class MergeSort():
    def __init__(self, a):
        self.arr = a

    @staticmethod
    def merge(a1, a2):
        a = np.zeros(len(a1)+len(a2))
        i=0; j=0; k=0
        while i<len(a1) or j<len(a2):
            if i<len(a1) and (j==len(a2) or a1[i]<a2[j]):
                a[k] = a1[i]
                k+=1
                i+=1
            elif j<len(a2) and (i==len(a1) or a1[i]>=a2[j]):
                a[k] = a2[j]
                k+=1
                j+=1
        return a

    @staticmethod
    def merge2(a, i1, i2, j1, j2):
        return 1

    @staticmethod
    def mergesort(a):
        return 1

# Counting inversions.
# Sorting linked lists doesn't even require extra space.

class QuickSort():
    def __init__(self,a):
        self.arr=a

    @staticmethod
    def partition(a,p,r):
        x=a[r]
        i = p-1
        for j in range(p,r):
            if a[j]<=x:
                i+=1
                QuickSort.swap(a,i,j)
        QuickSort.swap(a,i+1,r)
        return i+1

    @staticmethod
    def sort(a,p,r):
        if p<r:
            q = QuickSort.partition(a,p,r)
            QuickSort.sort(a,p,q-1)
            QuickSort.sort(a,q+1,r)

    @staticmethod
    def swap(a,i,j):
        tmp=a[i]
        a[i]=a[j]
        a[j]=tmp

if __name__=="__main__":
    a=[6,5,4,3,2,1]
    QuickSort.sort(a,0,len(a)-1)
    print(a)

