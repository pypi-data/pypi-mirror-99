from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> bool:
      ix = binary_srch(nums,target,0,len(nums)-1)
      if ix==-1:
          return False
      else:
          return True

def find_pivot(a,lo,hi):
    if (a[hi]>a[lo]):
        return -1
    else:
        while lo<hi:
            mid=(lo+hi)//2
            if (a[mid]<a[hi]):
                hi=mid
            else:
                lo=mid+1
        return lo

def find_pivot2(a,lo,hi):
    if (a[hi]>a[lo]):
        return -1
    else:
        while lo<hi:
            mid=(lo+hi)//2+(lo+hi)%2
            if (a[mid]<=a[hi]):
                hi=mid-1
            else:
                lo=mid
        return hi

def map_sorted_to_rotated(x,pv,a):
    n=len(a)
    return a[(x+pv+1)%n]

def binary_srch(a,t,lo,hi):
    pv=find_pivot(a,lo,hi)
    while lo!=hi:
        mid=(lo+hi)//2
        val=map_sorted_to_rotated(mid,pv,a)
        if val<t:
            lo=mid+1
        else:
            hi=mid
    if map_sorted_to_rotated(lo,pv,a)==t:
        return (lo+pv+1)%len(a)
    else: return -1


if __name__=="__main__":
    nums = [2,5,6,0,0,1,2]; target = 0
    pv = find_pivot(nums,0,len(nums)-1)
    print(pv)
    nums = [2,2,2,0,0,1,2]; target = 0
    pv = find_pivot(nums,0,len(nums)-1)
    print(pv)
    nums=[2,5,6,0,0,1,2]
    ix = binary_srch(nums,0,0,len(nums)-1)
    print(ix)
    nums=[2,2,2,0,2,2]
    pv1=find_pivot(nums,0,len(nums)-1)
    pv2=find_pivot2(nums,0,len(nums)-1)
    print(str(pv1)+","+str(pv2))
    nums=[4,5,6,7,0,1,2]
    pv1=find_pivot(nums,0,len(nums)-1)
    pv2=find_pivot2(nums,0,len(nums)-1)
    print(str(pv1)+","+str(pv2))
    ix = binary_srch(nums,0,0,len(nums)-1)
    print(ix)

