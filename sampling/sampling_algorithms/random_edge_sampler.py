import networkx as nx
import random
import math
import graph_wrapper as g_wrapper

__author__ = """Emrah Cem (emrah.cem@utdallas.edu)"""
__all__=['random_edge_sampler']

#def random_edge_sampler(G, sample_edge_or_node_size, stop_at_vertex_size=True, count_each_once=False, with_replacement=True, include_last_edge_if_number_of_nodes_exceeds=True):
    

def random_edge_sampler(G, sample_size, stopping_condition='UNIQUE_NODES', with_replacement=True, include_last_edge_when_exceeds=True):
    
    stopping_condition=str.upper(str(stopping_condition))
    if type(G) != nx.Graph:
        raise nx.NetworkXException("Graph must be a simple undirected graph!") 
    if not stopping_condition in ['UNIQUE_NODES','UNIQUE_EDGES','NODES','EDGES']:
        raise ValueError('Invalid stopping criteria, please choose one from ['+'"UNIQUE_NODES", "UNIQUE_EDGES", "NODES", "EDGES"'+']')
    if sample_size==None or sample_size<1 or (sample_size > G.number_of_edges() and stopping_condition=='UNIQUE_EDGES') or (sample_size > G.number_of_nodes() and stopping_condition=='UNIQUE_NODES'):
        raise ValueError('Invalid sample size')
    if with_replacement==False and ( (stopping_condition=='NODES'  and sample_size>2*G.number_of_edges()) or (stopping_condition=='EDGES'  and sample_size>G.number_of_edges()) ):
        raise ValueError('Invalid sample size')
    
    sample_graph=nx.Graph()
    

    if with_replacement:
        edges=G.edges()
        if stopping_condition=='UNIQUE_NODES':
            for _ in range(0,sample_size/2):
                    g_wrapper.add_edge_to_graph(sample_graph, random.choice(edges))
                 
            if include_last_edge_when_exceeds:
                while sample_graph.number_of_nodes()< sample_size:
                    g_wrapper.add_edge_to_graph(sample_graph,random.choice(edges))
            else:
                while True:
                    e=random.choice(edges)
                    if sample_graph.number_of_nodes()< sample_size-1:
                        g_wrapper.add_edge_to_graph(sample_graph, e)
                    else:
                        if sample_graph.number_of_nodes()== sample_size:
                            break
                        else:
                            if len(set(e).intersection(sample_graph.nodes()))==0:
                                g_wrapper.add_node_to_graph(sample_graph, e[0])
                                break
                            elif len(set(e).intersection(sample_graph.nodes()))==1:
                                g_wrapper.add_edge_to_graph(sample_graph, e)
                                break
                            else:
                                g_wrapper.add_edge_to_graph(sample_graph, e)
        elif stopping_condition=='UNIQUE_EDGES':
            while sample_graph.number_of_edges()< sample_size:
                    g_wrapper.add_edge_to_graph(sample_graph,random.choice(edges))
         
        elif stopping_condition=='NODES':
            number_of_edges=int(math.ceil(sample_size/2.0)) if include_last_edge_when_exceeds else int(math.floor(sample_size/2.0)) 
             
            for _ in range(0,number_of_edges):
                g_wrapper.add_edge_to_graph(sample_graph,random.choice(edges))
             
            if not include_last_edge_when_exceeds and sample_size %2 ==1:
                g_wrapper.add_node_to_graph(sample_graph,random.choice(edges)[0])
         
        elif stopping_condition=='EDGES':
            for _ in xrange(0,sample_size):
                g_wrapper.add_edge_to_graph(sample_graph,random.choice(edges))
 
    else:# not with replacement
        edge_list=random.sample(G.edges(),G.number_of_edges()) #creates a shuffled edge list
         
        if stopping_condition=='UNIQUE_NODES':
            for e in edge_list[0:sample_size/2]:
                    g_wrapper.add_edge_to_graph(sample_graph, e)
                 
            if include_last_edge_when_exceeds:
                for e in edge_list[sample_size/2:]:
                    if sample_graph.number_of_nodes()< sample_size:
                        g_wrapper.add_edge_to_graph(sample_graph,e)
                    else:
                        break
            else:
                for e in edge_list[sample_size/2:]:
                    if sample_graph.number_of_nodes()< sample_size-1:
                        g_wrapper.add_edge_to_graph(sample_graph, e)
                    else:
                        if sample_graph.number_of_nodes()== sample_size:
                            break
                        else:
                            if len(set(e).intersection(sample_graph.nodes()))==0:
                                g_wrapper.add_node_to_graph(sample_graph, e[0])
                                break
                            elif len(set(e).intersection(sample_graph.nodes()))==1:
                                g_wrapper.add_edge_to_graph(sample_graph, e)
                                break
                            else:
                                g_wrapper.add_edge_to_graph(sample_graph, e)
             
        elif stopping_condition=='UNIQUE_EDGES':
            for e in edge_list:
                if sample_graph.number_of_edges()< sample_size:
                    g_wrapper.add_edge_to_graph(sample_graph, e)
                else:
                    break
                 
        elif stopping_condition=='NODES':
             
            number_of_edges=int(math.ceil(sample_size/2.0)) if include_last_edge_when_exceeds else int(math.floor(sample_size/2.0)) 
             
            for e in edge_list[0:number_of_edges]:
                g_wrapper.add_edge_to_graph(sample_graph,e)
             
            if not include_last_edge_when_exceeds and sample_size %2 ==1:
                g_wrapper.add_node_to_graph(sample_graph,edge_list[number_of_edges][0])
                 
        elif stopping_condition=='EDGES':
            for e in edge_list[0:sample_size]:
                g_wrapper.add_edge_to_graph(sample_graph, e)
                
    return sample_graph

