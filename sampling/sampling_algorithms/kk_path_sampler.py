import networkx as nx
import random
import itertools
import warnings
import graph_wrapper as g_wrapper

__author__ = """Emrah Cem (emrah.cem@utdallas.edu)"""
__all__=['kk_path_sampler']

def kk_path_sampler(G, sample_size, K=None, vantage_points=None,
                    stopping_condition='UNIQUE_NODES', fuzzy_select=True, include_last_path_when_exceeds=True):
    """Return a subgraph sampled by KK_path_sampler """
    
    stopping_condition=str.upper(str(stopping_condition))
    if type(G) != nx.Graph:
        raise nx.NetworkXException("Graph must be a simple undirected graph!") 
    if not stopping_condition in ['UNIQUE_NODES','UNIQUE_EDGES','NODES','EDGES']:
        raise ValueError('Invalid stopping criteria, please choose one from ['+'"UNIQUE_NODES", "UNIQUE_EDGES", "NODES", "EDGES"'+']')
    if sample_size==None or sample_size<1 or (stopping_condition=='UNIQUE_NODES' and sample_size > len(G)) or (stopping_condition=='UNIQUE_EDGES' and sample_size > G.number_of_edges()):
        raise ValueError('Invalid sample size')
    if vantage_points is not None: 
        if not set(vantage_points).issubset(G.nodes()):
            raise ValueError("Vantage points must be a subset of node set of population graph")
        else:
            if K is not None: 
                warnings.warn('parameter K was ignored, since vantage points were given explicitly', UserWarning)   
    else:
        if K is None:
            vantage_points= random.sample([x for x in G.nodes()],int(len(G)*5/100))
        if K is not None:
            if K<2 or K>len(G):
                raise ValueError("Number of vantage points should be in [2,"+str(len(G))+']')
            vantage_points= random.sample([x for x in G.nodes()],K)  
        
    sample_graph=nx.Graph(name=str(G.name+'_KK_size'+str(sample_size)+'_stopping_condition'+stopping_condition+'_k'+str(len(vantage_points))))  
    stopLooping=False
    
    s_d_tuples=list(itertools.combinations(vantage_points,2))
    
    if fuzzy_select:
        random.shuffle(s_d_tuples)
    
    
    for s_d_tuple in s_d_tuples:
        
        if stopLooping:
            break           
        try:
            path=nx.shortest_path(G,*s_d_tuple)
            
            if stopping_condition=='UNIQUE_NODES':
                if sample_graph.number_of_nodes() +len(path) >sample_size:#check if the whole path is added, desired sample size is exceeded, if so add the path partially
                #if len(set(sample_graph.nodes()).union(set(path)))>sample_size:#check if the whole path is added, desired sample size is exceeded, if so add the path partially
                    if include_last_path_when_exceeds:
                        g_wrapper.add_path_to_graph(sample_graph, path)
                    else:
                        for i in range(0,len(path)):
                            if len(set(sample_graph.nodes()).union(set(path[0:i])))==sample_size:
                                g_wrapper.add_path_to_graph(sample_graph, path[0:i])
                    if sample_graph.number_of_nodes() > sample_size:
                        stopLooping=True
                        break
                else:
                    g_wrapper.add_path_to_graph(sample_graph, path)
                    if sample_graph.number_of_nodes()==sample_size:
                        stopLooping=True
                        break

            elif stopping_condition=='UNIQUE_EDGES':
                if sample_graph.number_of_edges()+len(path)-1<sample_size:
                    g_wrapper.add_path_to_graph(sample_graph,path)
                else:
                    if include_last_path_when_exceeds:
                        g_wrapper.add_path_to_graph(sample_graph, path)
                        if  sample_graph.number_of_edges()>sample_size:
                            break
                    else:
                        new_edge=0
                        last_index_of_path=-1
                        for i,e in enumerate(zip(path,path[1:])):
                            if not sample_graph.has_edge(*e):
                                new_edge+=1
                                if new_edge==sample_size-sample_graph.number_of_edges():
                                    last_index_of_path=i
                                    break
               
                        if last_index_of_path== -1:
                            g_wrapper.add_path_to_graph(sample_graph,path)
                        else:
                            g_wrapper.add_path_to_graph(sample_graph,path[0:last_index_of_path+2])
                            break
                    
            elif stopping_condition=='NODES':
                if sample_graph.graph.get('number_of_nodes_repeated',0)+len(path)< sample_size:
                    g_wrapper.add_path_to_graph(sample_graph, path)
                else:
                    if include_last_path_when_exceeds:
                        g_wrapper.add_path_to_graph(sample_graph, path)
                    else:
                        index_of_last_node=sample_size-sample_graph.graph['number_of_nodes_repeated']
                        g_wrapper.add_path_to_graph(sample_graph, path[0:index_of_last_node])
                    stopLooping=True
                    
            elif stopping_condition=='EDGES':
                if sample_graph.graph.get('number_of_edges_repeated',0)+len(path)-1<sample_size:
                    g_wrapper.add_path_to_graph(sample_graph,path)
                else:
                    if include_last_path_when_exceeds:
                        g_wrapper.add_path_to_graph(sample_graph,path)
                    else:   
                        g_wrapper.add_path_to_graph(sample_graph,path[0: sample_size - sample_graph.graph['number_of_edges_repeated']+1  ]) 
                    stopLooping=True 
                       
        except nx.NetworkXNoPath:
            print 'no path'
            pass
        except nx.NetworkXError as e:
            print e
            pass
    
    if (stopping_condition=='UNIQUE_NODES' and sample_graph.number_of_nodes()<sample_size) or (stopping_condition=='UNIQUE_EDGES' and sample_graph.number_of_edges()<sample_size):
        raise ValueError('Desired sample size could not be reached.')
    
    if (stopping_condition=='NODES' and sample_graph.graph['number_of_nodes_repeated'] < sample_size) or (stopping_condition=='EDGES' and sample_graph.graph['number_of_edges_repeated'] < sample_size):
        raise ValueError('Desired sample size could not be reached.')
    
    sample_graph.graph['vantage_points']=vantage_points
    return sample_graph