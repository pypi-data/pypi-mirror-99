## Leetcode problem 210: Course schedule II.
#https://leetcode.com/problems/course-schedule-ii/
#based on topological sorting.

import numpy as np
import algorith.clr_book.ch22_elemtary_graph.graph as gr
from typing import List


class Solution():
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        self.lst = []
        g=gr.Graph().init_from_edge_list(numCourses,prerequisites)
        self.dfs_topolo_sort(g)
        return self.lst
        
    def dfs_topolo_sort(self,g):
        for v in g.vertices:
            if v.color=="white":
                try:
                    self.dfs_visit(g,v)
                except:
                    self.lst=[]
                    break
    
    def dfs_visit(self,g,u):
        u.color="grey"
        for v in g.adj[u]:
            if v.color=="grey":
                raise Exception("cycle detected!")
            elif v.color=="white":
                self.dfs_visit(g,v)
        u.color="black"
        self.lst.append(u.key)


if __name__ == "__main__":
    numCourses = 4; prerequisites = [[1,0],[2,0],[3,1],[3,2]]; output_1= [0,2,1,3]; output_2= [0,1,2,3]
    lst = Solution().findOrder(numCourses,prerequisites)
    print(lst)
    numCourses = 2; prerequisites = [[1,0]]; output= [0,1]
    lst = Solution().findOrder(numCourses,prerequisites)
    print(lst)
    numCourses = 2; prerequisites = [[0,1]]; output= [1,0]
    lst = Solution().findOrder(numCourses,prerequisites)
    print(lst)
    numCourses = 2; prerequisites = [[0,1],[1,0]]; output= []
    lst = Solution().findOrder(numCourses,prerequisites)
    print(lst)

