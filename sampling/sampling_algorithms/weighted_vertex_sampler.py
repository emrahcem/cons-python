import networkx as nx
import random
import itertools, bisect
import graph_wrapper as g_wrapper

__author__ = """Emrah Cem (emrah.cem@utdallas.edu)"""

__all__=['weighted_vertex_sampler']

def weighted_vertex_sampler(G, sample_size, weights, with_replacement=True):
    
    if type(G) != nx.Graph:
        raise nx.NetworkXException("Graph must be a simple undirected graph!") 
    if sample_size==None or sample_size<1 or (not with_replacement and sample_size>len(G)):
        raise ValueError('Invalid sample size')
        
    sample_graph=nx.Graph()
    if with_replacement:   
        if weights==None:  # uniform
            for _ in xrange(0,sample_size):
                g_wrapper.add_node_to_graph(sample_graph, random.choice(G.nodes()))
        else:    # weighted
            cum_weights = [0]*len(G)
            tot_weight = 0
 
            for i,v in enumerate(G.nodes()):
                tot_weight += weights(v)
                cum_weights[i] = tot_weight
                        
            for c in itertools.count():
                if c==sample_size: break
                selected_node = bisect.bisect_right(cum_weights, random.random() * tot_weight)
                g_wrapper.add_node_to_graph(sample_graph, random.choice(G.nodes()))
                #sys.stdout.write("\r%{0} completed".format(100*len(sample_graph)/sample_size ))
                #sys.stdout.flush()
    else:
        if weights==None:
            sampled_vertices=random.sample(G.nodes(),sample_size)
            for n in sampled_vertices:
                g_wrapper.add_node_to_graph(sample_graph,n)
        else:
            cum_weights = [0]*len(G)
            tot_weight = 0
 
            for i,v in enumerate(G.nodes()):
                tot_weight += weights(v)
                cum_weights[i] = tot_weight
                        
            while sample_graph.number_of_nodes()< sample_size:
                selected_node = bisect.bisect_right(cum_weights, random.random() * tot_weight)
                if not sample_graph.has_node(selected_node):
                    g_wrapper.add_node_to_graph(sample_graph,selected_node)
    
    return sample_graph      