from typing import List


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        self.paths = []
        self.uniq_paths = set()
        self.arr = candidates
        candidates.sort()
        self.comb_sum(target,[])
        return self.paths

    def comb_sum(self,t,path):
        for a in self.arr:
            if (t-a)==0:
                path.append(a)
                path1 = path.copy()
                path1.sort()
                if str(path1) not in self.uniq_paths:
                    self.uniq_paths.add(str(path1))                
                    self.paths.append(path1)
            elif t-a>0:
                path.append(a)
                self.comb_sum(t-a,path)
            else:
                break
            path.pop()


if __name__=="__main__":
    a = [2,3,6,7]
    t = 7
    sol = Solution()
    paths = sol.combinationSum(a,t)
    print(paths)
    a = [2,3,5]
    t = 8
    paths = sol.combinationSum(a,t)
    print(paths)

