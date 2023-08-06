import numpy as np

def binary_search(a, d, lo, hi, asc_order=True):
    if a[lo]>d:
        return lo-1
    elif a[hi]<d:
        return hi
    while lo < hi:
        mid = (lo+hi)//2
        midval = a[mid]
        if midval < d:
            if asc_order:
                lo = mid+1
            else:
                hi = mid-1
        elif midval > d:
            if asc_order:
                hi = mid-1
            else:
                lo = mid+1
        else:
            return mid
    if a[lo]<=d:
        return lo
    else:
        return int(lo-(asc_order-0.5)*2)

"""
Proof that this works:
1) At every iteration, either we find what we were looking for
or lo goes down by atleast 1 or hi goes up by atleast 1. They go
down by only 1 if mid evaluates to lo.
2) So, there is no way that hi and lo can both be the same in two 
consecutive iterations.
3) Hence, eventually hi and lo have to become equal to each other 
pr cross each other.
"""
def binary_srch_exact(a,t,lo,hi):
    """
    Here, a is a rotated sorted array.
    """
    while hi>=lo:
        mid=(lo+hi)//2
        if a[mid]==t:
            return mid
        elif a[mid]<t:
            lo=mid+1
        elif a[mid]>t:
            hi=mid-1
    return -1



def binary_search_lo(a,d,lo,hi):
    """
    Created for leetcode prob 34
    """
    if d!=a[hi]:
        raise Exception("d should be a[hi]")
    while hi>lo:
        mid=(lo+hi)//2
        if a[mid]==d:
            hi=mid
        else:
            lo=mid+1
    if a[lo]==d:
        return lo
    else:
        return hi

def binary_search_hi(a,d,lo,hi):
    """
    Created for leetcode prob 34
    """
    if d!=a[lo]:
        raise Exception("d should be a[lo]")
    while hi>lo:
        mid=(lo+hi)//2+1
        if a[mid]==d:
            lo=mid
        else:
            hi=mid-1
    if a[hi]==d:
        return hi
    else:
        return lo

def binary_search_oprns(a, d, lo, hi, asc_order=True,\
                        oprns=[0]):
    """
    Binary search, but counts the 
    number of operations for complexity analysis.
    """
    if a[lo]>d:
        oprns[0]+=1
        return lo-1
    elif a[hi]<d:
        oprns[0]+=1
        return hi
    while lo < hi:
        oprns[0]+=1
        mid = (lo+hi)//2
        oprns[0]+=1
        midval = a[mid]
        if midval < d:
            oprns[0]+=1
            if asc_order:
                lo = mid+1
            else:
                hi = mid-1
        elif midval > d:
            oprns[0]+=1
            if asc_order:
                hi = mid-1
            else:
                lo = mid+1
        else:
            return mid
    if a[lo]<=d:
        oprns[0]+=1
        return lo
    else:
        return int(lo-(asc_order-0.5)*2)


def tst():
    re = binary_search([1,2,3,4,5],2.6,0,4)
    print("Test-1: "+str(re==1))    
    re = binary_search([1,2,3],2,0,2)
    print(re)
    res=binary_search_lo([1,2,3,3,3,3],3,0,5)
    print(res)
    res=binary_search_lo([1,1,1,3,3,3,3,4,5],3,0,6)
    print(res)
    res=binary_search_lo([3,3,3,3,4,5],3,0,3)
    print(res)
    res=binary_search_hi([3,3,3,3,4,5,5,5],3,0,3)
    print(res)


if __name__=="__main__":
    tst()

