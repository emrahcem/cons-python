'''
Created on Aug 28, 2013

@author: Emrah Cem{emrah.cem@utdallas.edu}
'''

import networkx as nx
from weighted_vertex_sampler import *

__author__ = """Emrah Cem (emrah.cem@utdallas.edu)"""
__all__=['induced_random_vertex_sampler']

def induced_weighted_random_vertex_sampler(G, sample_node_size, weights=None, with_replacement=True):
    
    res=weighted_vertex_sampler(G, sample_node_size, weights=weights, with_replacement=with_replacement)
    induced_subgraph=nx.Graph(G.subgraph(res.nodes()))
    for n in res.nodes():
        induced_subgraph.node[n]['times_selected']=res.node[n].get('times_selected',0)
    
    return induced_subgraph
