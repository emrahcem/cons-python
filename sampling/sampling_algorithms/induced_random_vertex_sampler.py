import networkx as nx 
from random_vertex_sampler import *
import graph_wrapper as g_wrapper

__author__ = """Emrah Cem (emrah.cem@utdallas.edu)"""
__all__=['induced_random_vertex_sampler']

#DO I NEED TO INCREMENT NODE COUNTS WHEN ADDING INDUCED EDGES? IF I DO, SAMPLE SIZE WILL EXCEED (2*num_of_induced_edges+ INPUT SAMPLE SIZE) THE INPUT SAMPLE SIZE?

def induced_random_vertex_sampler(G, sample_size, with_replacement=True):
    
    sample_graph=random_vertex_sampler(G, sample_size=sample_size, with_replacement=with_replacement) 
    induced_edges=set(G.subgraph(sample_graph.nodes()).edges())
    
    for e in induced_edges:
        g_wrapper.add_edge_to_graph(sample_graph,e)
    
    sample_graph.graph['induced_edges']=induced_edges    
    return sample_graph
