import numpy as np
from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        return binary_srch(nums,target,0,len(nums)-1)

def map_sorted_to_rotated(x,piv,n):
    if piv>=0:
        return (x+piv+1)%n
    else:
        return x

def find_pivot(a,lo,hi):
    while hi>lo:
        if a[hi]>a[lo]:
            return -1
        elif hi-lo<=1:
            return lo
        else:
            mid=(hi+lo)//2
            if a[mid]<a[lo]:
                hi=mid
            elif a[hi]<a[mid]:
                lo=mid
    return -1

def binary_srch(a,t,lo,hi):
    """
    Here, a is a rotated sorted array.
    """
    piv=find_pivot(a,lo,hi)
    while hi>lo:
        mid=(lo+hi)//2
        nu_mid = map_sorted_to_rotated(mid,piv,len(a))
        if a[nu_mid]==t:
            return nu_mid
        elif a[nu_mid]<t:
            lo=mid+1
        elif a[nu_mid]>t:
            hi=mid-1
    nu_lo = map_sorted_to_rotated(lo,piv,len(a))
    if a[nu_lo]==t:
        return nu_lo
    else:
        return -1


if __name__=="__main__":
    nums=[4,5,6,7,0,1,2]
    target=3
    piv=find_pivot(nums,0,len(nums)-1)
    print(piv)
    mp2 = map_sorted_to_rotated(4,piv,len(nums))
    print(mp2)
    ix = binary_srch(nums,target,0,len(nums)-1)
    print(ix)
    nums=[1]
    target=1
    piv=find_pivot(nums,0,len(nums)-1)
    print(piv)
    ix = binary_srch(nums,target,0,len(nums)-1)
    print(ix)
    nums=[3,1]
    target=3
    ix = binary_srch(nums,target,0,len(nums)-1)
    print(ix)
    nums=[1,2,3]
    piv=find_pivot(nums,0,len(nums)-1)
    nums=[1,3]
    target=1
    ix = binary_srch(nums,target,0,len(nums)-1)
    print(ix)
