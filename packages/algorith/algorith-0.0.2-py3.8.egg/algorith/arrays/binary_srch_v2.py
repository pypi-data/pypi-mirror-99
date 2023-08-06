## Based on methods in Wikipedia article:
# https://en.wikipedia.org/wiki/Binary_search_algorithm

def binary_srch_exact_alt(a,t,lo,hi):
    while lo!=hi:
        mid=(lo+hi)//2
        if a[mid]<t:
            lo=mid+1
        else:
            hi=mid
    if a[lo]==t: return lo
    else: return -1


def binary_srch_left(a,t,lo,hi):
    while lo<hi:
        mid=(lo+hi)//2
        if a[mid]<t:
            lo=mid+1
        else:
            hi=mid
    if a[lo]==t: return lo
    else: return -1


def binary_srch_right(a,t,lo,hi):
    while lo<hi:
        mid=(lo+hi)//2
        if a[mid]>t:
            hi=mid
        else:
            lo=mid+1
    if a[lo-1]==t: return lo-1
    else: return -1


def binary_srch_right_v2(a,t,lo,hi):
    while lo<hi:
        mid=(lo+hi)//2+(lo+hi)%2
        if a[mid]>t:
            hi=mid-1
        else:
            lo=mid
    if a[hi]==t: return hi
    else: return -1


def tst2():
    a=[0,1,2,4,5,6,7]
    res=binary_srch_exact_alt(a,3,0,len(a))
    print(res)
    res=binary_srch_exact_alt(a,5,0,len(a))
    print(res)
    a=[0,1,2,2,3,3,3,3,3,4,5,6]
    res=binary_srch_left(a,3,0,len(a))
    print(res)
    res=binary_srch_right(a,3,0,len(a))
    print(res)
    res=binary_srch_right_v2(a,3,0,len(a))
    print(res)


if __name__=="__main__":
    tst2()

