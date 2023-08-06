## Leetcode problem 207: Course schedule.
import numpy as np
import algorith.clr_book.ch22_elemtary_graph.graph as gr

## numCourses=2; prerequisites=[[1,0]]; return: True
## numCourses=2; prerequisites=[[1,0],[0,1]]; return: False
## numCourses=4; prerequisites=[[0,1],[0,2],[1,3],[2,3]]; return: False


## See here: https://walkccc.github.io/CLRS/Chap22/22.3/
def find_cycle_w_dfs_it(g):
    for u in g.vertices:
        if u.color=="white":
            if find_cycle_w_dfs(g,u):
                return True
    return False


def find_cycle_w_dfs(g,u):
    u.color="grey"
    st=[u]
    while len(st)>0:
        u=st[len(st)-1]
        remains=False
        for v in g.adj[u]:
            if v.color=="grey":
                return True
            elif v.color=="white":
                remains=True
                v.color="grey"
                st.append(v)
                break#Exit the for loop
        if not remains:
            st.pop()
            u.color="black"
    return False


def find_cycle_w_dfs_rec(g):
    for ver in g.vertices:
        if ver.color=="white":
            try:
                find_cycles_dfs_visit(g,ver)
            except:
                return True
    return False


def find_cycles_dfs_visit(g,u):
    u.color="grey"
    if u in g.adj.keys():
        for v in g.adj[u]:
            if v.color=="white":
                find_cycles_dfs_visit(g,v)
            elif v.color=="grey":
                raise Exception("cycle detected!")
    u.color="black"

#########################################
## Tests

def tst():
    prerequisites=[[1,0],[2,0],[3,1],[3,2]]
    numCourses=4
    g=gr.Graph().init_from_edge_list(numCourses,prerequisites)
    print(find_cycle_w_dfs_rec(g)==False)
    prerequisites=[[0,1],[1,0]]
    numCourses=2
    g=gr.Graph().init_from_edge_list(numCourses,prerequisites)
    print(find_cycle_w_dfs_rec(g)==True)
    prerequisites=[[1,0],[0,3],[0,2],[3,2],[2,5],[4,5],[5,6],[2,4]]
    numCourses=7
    g=gr.Graph().init_from_edge_list(numCourses,prerequisites)
    print(find_cycle_w_dfs_it(g))
    #find_cycle_w_dfs_rec(g)

