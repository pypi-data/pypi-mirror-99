import numpy as np
from algorith.arrays.binary_srch import binary_search


def find_k_ix(a1,i1,j1,a2,i2,j2,k):
    n1=j1-i1+1
    n2=j2-i2+1
    if k==0:
        return min(a1[i1],a2[i2])
    elif k==n1+n2-1:
        return max(a1[j1],a2[j2])
    elif k>n1+n2-1:
        raise Exception("Out of bounds")
    if n1<n2:
        n_s=n1; n_l=n2; i_s=i1; i_l=i2
        a_s=a1; a_l=a2; j_s=j1; j_l=j2
    else:
        n_s=n2; n_l=n1; i_s=i2; i_l=i1
        a_s=a2; a_l=a1; j_s=j2; j_l=j1
    if n_s==1:
        if a_l[k]<a_s[i_s] and a_s[i_s]<a_l[k+1]:
            return a_s[i_s]
        elif a_s[i_s]<a_l[k]:
            return a_l[k+1]
        else:
            return a_l[k]
    if k>=n_s:
        cand = a_l[i_l+k-n_s]
        ix = binary_search(a_s,cand,i_s,j_s)
        if ix==len(a_s)-1:
            return cand
        else:
            return find_k_ix(a_s,ix+1,j_s,a_l,i_l+k-n_s+1,j_l,n_s+i_s-ix-2)
    else:
        if a_s[i_s]<a_l[i_l]:
            return find_k_ix(a_s,i_s+1,i_s+k,a_l,i_l,i_l+k,k-1)
        else:
            return find_k_ix(a_s,i_s,i_s+k,a_l,i_l+1,i_l+k,k-1)

def find_median(a1,a2):
    n = len(a1)+len(a2)
    if n%2==1:
        return find_k_ix(a1,0,len(a1)-1,a2,0,len(a2)-1,n//2)
    else:
        num1=find_k_ix(a1,0,len(a1)-1,a2,0,len(a2)-1,n//2)
        num2=find_k_ix(a1,0,len(a1)-1,a2,0,len(a2)-1,n//2+1)
        return (num1+num2)/2


if __name__=="__main__":
    a11=np.array([ 3,  6,  8, 11, 13, 14])
    a21=np.array([ 0,  1,  2,  4,  5,  7,  9, 10, 12])
    mm1 = find_k_ix(a11,0,len(a11)-1,a21,0,len(a21)-1,5)
    print(mm1)

