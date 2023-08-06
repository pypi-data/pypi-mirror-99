import numpy as np

def cut_rod(p,n):
    if n==0:
        return 0
    q=-np.inf
    for i in range(1,n+1):
        q=max(q,p[i-1]+cut_rod(p,n-i))
    return q

def memoized_cut_rod(p,n):
    r=np.ones(n+1)*-np.inf
    r[0]=0
    return memoized_cut_rod_aux(p,n,r)

def memoized_cut_rod_aux(p,n,r):
    if r[n]>=0:
        return r[n]
    if n==0:
        q=0
    else: 
        q=-np.inf
        for i in range(1,n+1):
            q=max(q,p[i-1]+memoized_cut_rod_aux(p,n-i,r))
    r[n]=q
    return q

def bottom_up_cut_rod(p,n):
    r = np.ones(n+1)*-np.inf
    r[0]=0
    for i in range(1,n+1):
        q=-np.inf
        for j in range(1,i+1):
            q=max(q,p[j-1]+r[i-j])
        r[i]=q
    return r


if __name__=="__main__":
    p=[1,5,8,9,10,17,17,20,24,30,31,31,33,34,37,37,37,38]
    r0 = cut_rod(p,len(p))
    print(r0)
    r1=memoized_cut_rod(p,len(p))
    print(r1)
    r2 = bottom_up_cut_rod(p,len(p))
    print(r2)

