def t_recur(s,p,i,j):
    if i==-1 and j==-1:
        return True
    elif j==-1:
        return False
    elif i==-1:
        if (j+1)%2!=0:
            return False
        else:
            for k in range(int((j+1)//2)):
                if p[2*k+1]!="*":
                    return False
            return True        
    if p[j]==s[i] or p[j]==".":
        return t_recur(s,p,i-1,j-1)
    elif p[j]=="*":
        res1 = t_recur(s,p,i,j-2)
        res2 = False
        if p[j-1]==s[i] or p[j-1]==".":
            res2 = t_recur(s,p,i-1,j)
        return res1 or res2
    else:
        return False


if __name__ == "__main__":
    s="aa"; p="a"
    res = t_recur(s,p,len(s)-1,len(p)-1)
    print(res==False)
    s="aa"; p="a*"
    res = t_recur(s,p,len(s)-1,len(p)-1)
    print(res==True)
    s="ab"; p=".*"
    res = t_recur(s,p,len(s)-1,len(p)-1)
    print(res==True)
    s="aab"; p="c*a*b"
    res = t_recur(s,p,len(s)-1,len(p)-1)
    print(res==True)
    s="ab"; p=".*.."
    res = t_recur(s,p,len(s)-1,len(p)-1)
    print(res==True)
    s="aaa";p="aaaa"
    res = t_recur(s,p,len(s)-1,len(p)-1)
    print(res==False)

