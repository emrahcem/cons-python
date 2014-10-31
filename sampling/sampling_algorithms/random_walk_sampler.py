import networkx as nx
import random
import warnings
import graph_wrapper as g_wrapper

__author__ = """Emrah Cem (emrah.cem@utdallas.edu)"""
__all__=['random_walk_sampler']

def random_walk_sampler(G, sample_size, initial_node=None, stopping_condition='UNIQUE_NODES', metropolized=False, excluded_initial_steps=0):
    
    stopping_condition=str.upper(str(stopping_condition))
    if type(G) != nx.Graph:
        raise nx.NetworkXException("Graph must be a simple undirected graph!") 
    if sample_size==None or sample_size<1 or (sample_size > G.number_of_nodes() and stopping_condition=='UNIQUE_NODES') or (sample_size > G.number_of_edges() and stopping_condition=='UNIQUE_EDGES'):
        raise ValueError('Invalid sample size')
    if not stopping_condition in ['UNIQUE_NODES','UNIQUE_EDGES','NODES','EDGES']:
        raise ValueError('Invalid stopping criteria, please choose one from ['+'"UNIQUE_NODES", "UNIQUE_EDGES", "NODES", "EDGES"'+']')     
    if initial_node is not None and G.has_node(initial_node):
        current_node=initial_node
    else:
        current_node=random.choice(G.nodes())
        if initial_node is not None:
            warnings.warn('Initial node could not be found in population graph. It was chosen randomly.')
    
    sample_graph=nx.Graph()
    current_node= ignore_initial_steps(G, metropolized, excluded_initial_steps, current_node)
    
    if stopping_condition=='UNIQUE_NODES':
        while True:  
            update_sample_graph_before_the_step(current_node, sample_graph)
            if sample_graph.number_of_nodes() < sample_size:
                node_before_step=current_node
                current_node=next_node(G, current_node, metropolized)
                take_a_step(node_before_step, current_node, sample_graph)
            else:
                break
            
            
    elif stopping_condition=='UNIQUE_EDGES':
        while True:  
            update_sample_graph_before_the_step(current_node, sample_graph)
            if sample_graph.number_of_edges() < sample_size:
                node_before_step=current_node
                current_node=next_node(G, current_node, metropolized)
                take_a_step(node_before_step, current_node, sample_graph)
            else:
                break

    elif stopping_condition=='NODES':
        while True:
            update_sample_graph_before_the_step(current_node, sample_graph)
            if sample_graph.graph.get('number_of_nodes_repeated',0)<sample_size:
                node_before_step=current_node
                current_node=next_node(G, current_node, metropolized)
                take_a_step(node_before_step, current_node, sample_graph)
            else:
                break

    elif stopping_condition=='EDGES':
        while True:
            update_sample_graph_before_the_step(current_node, sample_graph)
            if sample_graph.graph.get('number_of_edges_repeated',0)<sample_size:
                node_before_step=current_node
                current_node=next_node(G, current_node, metropolized)
                take_a_step(node_before_step, current_node, sample_graph)
            else:
                break
    return sample_graph 

def next_node(G, current_node, metropolized):
    if metropolized:
        candidate = random.choice(G.neighbors(current_node))
        current_node = candidate if (random.random() < float(G.degree(current_node))/G.degree(candidate)) else current_node
    else:
        current_node = random.choice(G.neighbors(current_node))
    return current_node


def ignore_initial_steps(G, metropolized, excluded_initial_steps, current_node):
    
    for _ in xrange(0,excluded_initial_steps):
        current_node = next_node(G, current_node, metropolized)
        
    return current_node


def update_sample_graph_before_the_step(current_node, sample_graph):
    g_wrapper.add_node_to_graph(sample_graph, current_node)
    #print 'add node:', current_node

def take_a_step(node_before_step, current_node, sample_graph):
    
    #if node_before_step == current_node:
    #    g_wrapper.add_node_to_graph(sample_graph, current_node)
    #else:
    if node_before_step != current_node:
        g_wrapper.add_edge_to_graph(sample_graph, (node_before_step,current_node), add_nodes=False)   