import numpy as np

## Sub-optimal solution results in time limit exceeded.
def coin_change(a,ix,s):
    a.sort(reverse=True)
    if s==0:
        return 0
    if ix == len(a)-1:
        if s%a[ix]==0:
            return int(s/a[ix])
        else:
            return np.inf
    min_coins = np.inf
    for i in range(int(s/a[ix]),-1,-1):
    #i = int(s/a[ix])
        min_coins = min(min_coins,i+coin_change(a,ix+1,s-i*a[ix]))
    return min_coins

## Much worse than previous recursive soln.. but can be memoized.
def coin_change_v2(c,u):
    if u==0:
        return 0
    q=np.inf
    for i in range(len(c)):
        if u>=c[i]:
            q = min(q,coin_change_v2(c,u-c[i]))
    return q+1

def memoised_coin_chg(c,u):
    r=np.ones(u+1)*np.inf
    r[0]=0
    return memoised_coin_chg_aux(c,u,r)

def memoised_coin_chg_aux(c,u,r):
    if r[u]<np.inf:
        return r[u]
    if u==0:
        q=0
    else:
        q=np.inf
        for i in range(len(c)):
            if u >= c[i]:
                q=min(q,memoised_coin_chg_aux(c,u-c[i],r))
    r[u]=q+1
    return q+1

def bottom_up_coin_chg(c,u):
    r=np.ones(u+1)*np.inf; r[0]=0
    for j in range(1,u+1):
        q=np.inf
        for i in range(len(c)):
            if j>=c[i]:
                q=min(q,r[j-c[i]])
        r[j]=q+1
    return r[u]


def tst():
    res=coin_change([1,2,5],0,11)
    print(res)
    res=coin_change([2],0,3)
    print(res)
    res=coin_change([1,2147483647],0,2)
    print(res)
    res=coin_change([27,40,244,168,383],0,6989)
    print(res)
    res = coin_change([186,419,83,408],0,6249)
    print(res)
    res = coin_change([282,116,57,239,103,89,167],0,4856)
    print(res)

def tst2():
    res=coin_change_v2([1,2,5],11)
    print(res)
    res=coin_change_v2([2],3)
    print(res)
    res=coin_change_v2([1,2147483647],2)
    print(res)
    
def tst3():
    res=memoised_coin_chg([1,2,5],11)
    print(res)
    res=memoised_coin_chg([2],3)
    print(res)
    res=memoised_coin_chg([1,2147483647],2)
    print(res)
    res=memoised_coin_chg([27,40,244,168,383],6989)
    print(res)
    res = memoised_coin_chg([186,419,83,408],6249)
    print(res)
    res = memoised_coin_chg([282,116,57,239,103,89,167],4856)
    print(res)

def tst4():
    res=bottom_up_coin_chg([1,2,5],11)
    print(res)
    res=bottom_up_coin_chg([2],3)
    print(res)
    res=bottom_up_coin_chg([1,2147483647],2)
    print(res)
    res=bottom_up_coin_chg([27,40,244,168,383],6989)
    print(res)
    res = bottom_up_coin_chg([186,419,83,408],6249)
    print(res)
    res = bottom_up_coin_chg([282,116,57,239,103,89,167],4856)
    print(res)


if __name__=="__main__":
    tst()
    print("##Now the new method##")
    tst2()
    print("##Now the bottom-up version##")
    tst4()

