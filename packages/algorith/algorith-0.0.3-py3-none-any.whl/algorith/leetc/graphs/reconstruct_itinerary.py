## Leetcode problem 332: Reconstruct itinerary.
#https://leetcode.com/problems/reconstruct-itinerary/
import numpy as np
from collections import defaultdict
from typing import List
## This solution is a fail.. this is a Euler tour problem.

class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        g=Graph(tickets)
        self.itinerary=[]
        self.dfs(g)
        self.itinerary = [self.itinerary[i] for i in np.arange(len(self.itinerary)-1,-1,-1)]
        return self.itinerary

    def dfs(self,g):
        for v in g.vertices:
            if v.key=="JFK":
                self.dfs_visit(g,v)

    def dfs_visit(self,g,u):
        u.color="grey"
        for v in g.adj[u]:
            if v.color=="white":
                self.dfs_visit(g,v)
            elif v.color=="grey":
                print("cycle detected!")
        u.color="black"


class Node():
    def __init__(self,key,color="white"):
        self.key=key
        self.color=color

    def __hash__(self):
        return hash(self.key)

    def __le__(self,other):
        return self.key <= other.key


class Graph():
    def __init__(self,adj_lst):
        adj_lst.sort(key=lambda x:x[1])
        self.vertice_set = set()
        self.vertice_ix = {}
        self.vertices=[]
        ix=0
        for ed in adj_lst:
            if ed[0] not in self.vertice_set:
                self.vertice_set.add(ed[0])
                self.vertices.append(Node(ed[0]))
                self.vertice_ix[ed[0]]=ix
                ix+=1
            if ed[1] not in self.vertice_set:
                self.vertice_set.add(ed[1])
                self.vertices.append(Node(ed[1]))
                self.vertice_ix[ed[1]]=ix
                ix+=1
        self.adj = defaultdict(list)
        for ed in adj_lst:
            ver1 = self.vertices[self.vertice_ix[ed[0]]]
            ver2 = self.vertices[self.vertice_ix[ed[1]]]
            self.adj[ver1].append(ver2)


if __name__=="__main__":
    ## Test case-1:
    input1= [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]
    output1= ["JFK", "MUC", "LHR", "SFO", "SJC"]
    #itin = Solution().findItinerary(input1)
    #print(str(itin))
    ## test case-2:
    input1 = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]
    output1 = ["JFK","ATL","JFK","SFO","ATL","SFO"]
    itin = Solution().findItinerary(input1)
    print(str(itin))

