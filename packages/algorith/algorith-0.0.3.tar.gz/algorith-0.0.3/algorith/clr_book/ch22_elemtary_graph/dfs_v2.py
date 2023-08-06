import collections
from algorith.clr_book.ch22_elemtary_graph.graph import Graph

#####Alternate implementation based on 
# https://stackoverflow.com/a/53995651/1826912
# uses dictionaries instead of color propert for each node.
def dfs_v2(G):
    greys = set()
    blacks = set()

    for u in G.adj:
        ## If not grey or black, then the vertex must be white.
        if u not in greys and u not in blacks:
            greys, blacks = dfs_visit(G, u, greys, blacks)

## This doesn't currently work.. need to fix it.
# Currently designed for detecting cycles, but can be used to traverse graph.
def dfs_visit(G, u, greys, blacks):
    greys.add(u)
    for v in G.adj[u]:
        # Detect cycles
        if v in greys:
            print(f"Cycle detected: found a back edge from {u} to {v}.")
        # Recurse into DFS tree
        if v not in blacks:
            dfs_visit(G, v, greys, blacks)
    greys.remove(u)
    blacks.add(u)
    return greys, blacks

