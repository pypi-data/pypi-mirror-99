import numpy as np

#a=np.random.choice(2,size=(10,10))
def count_clouds(a):
    visited = set(); clouds = 0
    for i in range(len(a)):
        for j in range(len(a[0])):
            if a[i,j]==0 and (i,j) not in visited:
                clouds+=1
                ##Now do depth first search.
                stack = [(i,j)]
                while stack:
                    curr = stack.pop()
                    if curr not in visited:
                        visited.add(curr)
                        (ix,jx) = curr
                        if ix < len(a)-1 and a[ix+1,jx]==0:
                            stack.append((ix+1,jx))
                        if jx < len(a[0])-1 and a[ix,jx+1]==0:
                            stack.append((ix,jx+1))
    return clouds


def tst_count_clouds():
    a = np.ones((10,10))
    a[:2,:2]=0; a[2,2]=0
    
    a = np.ones((10,10))
    a[1:5,3:4]=0; a[8,8]=0
    a[9,9]=0
    
    a=np.random.choice(2,size=(10,10))
    clouds = count_clouds(a)
