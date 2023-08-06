from typing import List

def combin(ar,n,k):
    if len(ar)==k:
        print(ar)
        return
    for i in range(1,n+1):
        if len(ar)==0 or i>ar[len(ar)-1]:
            ar.append(i)
            combin(ar,n,k)
            ar.pop()


if __name__=="__main__":
    combin([],4,2)

class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        self.arr=[]
        self.combin([],n,k)
        return self.arr

    def combin(self,ar,n,k):
        if len(ar)==k:
            self.arr.append(ar.copy())
            return
        for i in range(1,n+1):
            if len(ar)==0 or i>ar[len(ar)-1]:
                ar.append(i)
                self.combin(ar,n,k)
                ar.pop()
