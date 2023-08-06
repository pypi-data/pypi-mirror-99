import numpy as np

def eta(s,t,i,j):
    if j==0:
        return sum([s[k]==t[0] for k in range(i+1)])
    if i==0:
        return 0
    res = eta(s,t,i-1,j)
    if s[i]==t[j]:
        res+=eta(s,t,i-1,j-1)
    return res

def memoized_eta_strt(s,t):
    if len(s)==0 or len(t)==0:
        return 0
    arr = np.ones((len(s),len(t)))*np.inf
    return memoized_eta(s,t,len(s)-1,len(t)-1,arr)

def memoized_eta(s,t,i,j,arr):
    if arr[i,j]<np.inf:
        return arr[i,j]
    if j==0:
        arr[i,j]= sum([s[k]==t[0] for k in range(i+1)])
        return arr[i,j]
    if i==0:
        arr[i,j]=0
        return 0
    res = memoized_eta(s,t,i-1,j,arr)
    if s[i]==t[j]:
        res+=memoized_eta(s,t,i-1,j-1,arr)
    arr[i,j] = res
    return int(res)


if __name__=="__main__":
    s1="rabbbit"
    t1="rabbit"
    res=eta(s1,t1,len(s1)-1,len(t1)-1)
    print(res)
    s2="babgbag"
    t2="bag"
    res=eta(s2,t2,len(s2)-1,len(t2)-1)
    print(res)
    res = memoized_eta_strt(s1,t1)
    print(res)
    res = memoized_eta_strt(s2,t2)
    print(res)

