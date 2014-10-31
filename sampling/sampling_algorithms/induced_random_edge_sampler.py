from random_edge_sampler import *
import graph_wrapper as g_wrapper
#from numpy.random import sample

__author__ = """Emrah Cem (emrah.cem@utdallas.edu)"""
__all__=['induced_random_edge_sampler']

def induced_random_edge_sampler(G, sample_size, stopping_condition='UNIQUE_NODES', with_replacement=True):
    sample_graph=random_edge_sampler(G, sample_size=sample_size, stopping_condition=stopping_condition, with_replacement=with_replacement)    

    induced_edges=set(G.subgraph(sample_graph.nodes()).edges())-set(sample_graph.edges())

    for e in induced_edges:
        g_wrapper.add_edge_to_graph(sample_graph,e)
        
    sample_graph.graph['induced_edges']=induced_edges
    return sample_graph