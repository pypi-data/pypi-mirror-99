import numpy as np
import networkx as nx

def sample_shortest_path():
    g = nx.Graph()
    g.add_edge('A', 'B', weight=4)
    g.add_edge('B', 'D', weight=2)
    g.add_edge('A', 'C', weight=3)
    g.add_edge('C', 'D', weight=4)
    nx.shortest_path(g, 'A', 'D', weight='weight')

def sample_max_flow():
    g = nx.DiGraph()
    g.add_edge('x','a', capacity=3.0)
    g.add_edge('x','b', capacity=1.0)
    g.add_edge('a','c', capacity=3.0)
    g.add_edge('b','c', capacity=5.0)
    g.add_edge('b','d', capacity=4.0)
    g.add_edge('d','e', capacity=2.0)
    g.add_edge('c','y', capacity=2.0)
    g.add_edge('e','y', capacity=3.0)
    flow_value, flow_dict = nx.maximum_flow(g, 'x', 'y')


