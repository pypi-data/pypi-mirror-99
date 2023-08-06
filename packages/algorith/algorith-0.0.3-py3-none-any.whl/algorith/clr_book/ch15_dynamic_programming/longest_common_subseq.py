import numpy as np

def longest_subseq_recur(x,y,i,j):
    if i==-1 or j==-1:
        return 0
    elif x[i]==y[j]:
        return longest_subseq_recur(x,y,i-1,j-1)+1
    else:
        return max(longest_subseq_recur(x,y,i-1,j),\
                longest_subseq_recur(x,y,i,j-1))


def lcs_len_topdwn_strt(x,y):
    m=len(x); n=len(y)
    c = np.ones((m+1,n+1))*np.inf
    return lcs_len_topdwn(x,y,m-1,n-1,c)


def lcs_len_topdwn(x,y,i,j,c):
    if c[i,j] < np.inf:
        return c[i,j]
    elif i==-1 or j==-1:
        c[i,j]=0
    elif x[i]==y[j]:
        c[i,j]=lcs_len_topdwn(x,y,i-1,j-1,c)+1
    else:
        c[i,j] = max(lcs_len_topdwn(x,y,i,j-1,c),\
            lcs_len_topdwn(x,y,i-1,j,c))
    return c[i,j]


def lcs_len_bottom_up(x,y):
    m=len(x)
    n=len(y)
    c=np.zeros((m+1,n+1))
    for i in range(1,m+1):
        for j in range(1,n+1):
            if x[i-1]==y[j-1]:
                c[i,j]=c[i-1,j-1]+1
            elif c[i-1,j]>=c[i,j-1]:
                c[i,j]=c[i-1,j]
            else:
                c[i,j]=c[i,j-1]
    return c[m,n]


def lcs_bottom_up(x,y):
    m=len(x)
    n=len(y)
    c=np.zeros((m+1,n+1)); b=np.copy(c)
    for i in range(1,m+1):
        for j in range(1,n+1):
            if x[i-1]==y[j-1]:
                c[i,j]=c[i-1,j-1]+1
                b[i,j]=-1#top-left
            elif c[i-1,j]>=c[i,j-1]:
                c[i,j]=c[i-1,j]
                b[i,j]=1#up
            else:
                c[i,j]=c[i,j-1]
                b[i,j]=0#left
    return c, b


def print_lcs(b,x,i,j):
    if i==0 or j==0:
        return
    if b[i,j]==-1:
        print_lcs(b,x,i-1,j-1)
        print(x[i-1],end='')
    elif b[i,j]==1:
        print_lcs(b,x,i-1,j)
    else:
        print_lcs(b,x,i,j-1)


if __name__=="__main__":
    x="abcbdab"
    y="bdcaba"
    res = longest_subseq_recur(x,y,len(x)-1,len(y)-1)
    print(res)
    c,b=lcs_bottom_up(x,y)
    print(b)
    print_lcs(b,x,len(x),len(y)); print()
    res = lcs_len_bottom_up(x,y)
    print(res)
    res = lcs_len_topdwn_strt(x,y)
    print(res)
    x="ACCGGTCGAGTGCGCGGAAGCCGGCCGAA"
    y="GTCGTTCGGAATGCCGTTGCTCTGTAAA"
    res = lcs_len_bottom_up(x,y)
    print(res)
    res = lcs_len_topdwn_strt(x,y)
    print(res)
    c,b=lcs_bottom_up(x,y)
    print_lcs(b,x,len(x),len(y)); print()
    #print(b)

