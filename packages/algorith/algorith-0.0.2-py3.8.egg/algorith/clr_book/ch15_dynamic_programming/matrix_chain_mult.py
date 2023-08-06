import numpy as np

def opt_mult_recurse(a,p,q):
    if q-p<2:
        return 0
    minn = np.inf
    for i in range(p+1,q):
        minn = min(minn,\
            opt_mult_recurse(a,p,i)+opt_mult_recurse(a,i,q)\
                +a[p]*a[i]*a[q])
    return minn


def opt_mult_top_dwn(a,p,q,m):
    if q-p<2:
        return 0
    if m[p,q] < np.inf:
        return m[p,q]
    minn = np.inf
    for i in range(p+1,q):
        minn = min(minn,\
                opt_mult_top_dwn(a,p,i,m)+opt_mult_top_dwn(a,i,q,m)\
                    +a[p]*a[i]*a[q])
    m[p,q] = minn
    return m[p,q]


def opt_mult_top_dwn_v2(a,p,q,m,s):
    if q-p<2:
        return 0, s
    if m[p,q] < np.inf:
        return m[p,q], s
    minn = np.inf; min_ix=0
    for i in range(p+1,q):
        minn1 = min(minn,\
                opt_mult_top_dwn_v2(a,p,i,m,s)[0]+\
                opt_mult_top_dwn_v2(a,i,q,m,s)[0]\
                    +a[p]*a[i]*a[q])
        if minn1<minn:
            minn = minn1; min_ix = i
    m[p,q] = minn
    s[p,q] = int(min_ix)
    return m[p,q], s


def opt_mult_top_dwn_strt(a):
    n = len(a)
    m=np.ones((n,n+1))*np.inf
    return opt_mult_top_dwn(a,0,len(a)-1,m)


def opt_mult_top_dwn_strt_v2(a):
    n = len(a)
    m=np.ones((n,n+1))*np.inf
    s=np.zeros((n,n+1)).astype(int)
    return opt_mult_top_dwn_v2(a,0,len(a)-1,m,s)

def print_opt_parenth(s,p,q):
    if q-p<2:
        print("A_"+str(q)+' ',end='')
    else:
        print("(",end='')
        print_opt_parenth(s,p,s[p,q])
        print_opt_parenth(s,s[p,q],q)
        print(")",end='')


# https://wbd.ms/share/v2/aHR0cHM6Ly93aGl0ZWJvYXJkLm1pY3Jvc29mdC5jb20vYXBpL3YxLjAvd2hpdGVib2FyZHMvcmVkZWVtLzA2YjJmZTQ0YWJkYTQ1ZjNiM2NkMTI0OWZmMjExYmY3X0JCQTcxNzYyLTEyRTAtNDJFMS1CMzI0LTVCMTMxRjQyNEUzRA==
def opt_mult_bottom_up(a):
    # The number of matrices
    n = len(a)-1
    m = np.zeros((n,n+1))
    for d_i in range(2,n+1):
        for p in range(n):
            q=p+d_i
            if q>n:
                break
            minn = np.inf
            for i in range(p+1,q):
                minn=min(minn,m[p,i]+m[i,q]+a[p]*a[i]*a[q])
            m[p,q] = minn
    return int(m[0,n])


if __name__=="__main__":
    a = np.arange(4)+2
    res = opt_mult_bottom_up(a)
    print(res)
    res = opt_mult_recurse(a,0,len(a)-1)
    print(res)
    res = opt_mult_top_dwn_strt(a)
    print("Top down version: " + str(res))
    a = [30,35,15,5,10,20,25]
    res=opt_mult_bottom_up(a)
    print(res)
    res = opt_mult_top_dwn_strt(a)
    print(res)
    res, s = opt_mult_top_dwn_strt_v2(a)
    print(s)
    print_opt_parenth(s,0,len(a)-1)

