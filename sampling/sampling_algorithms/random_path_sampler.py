import networkx as nx
import random
import graph_wrapper as g_wrapper

__author__ = """Emrah Cem (emrah.cem@utdallas.edu)"""

__all__=['random_path_sampler']

def random_path_sampler(G, sample_size, stopping_condition='UNIQUE_NODES', include_last_path_when_exceeds=True):
    
    stopping_condition=str.upper(str(stopping_condition))
    if type(G) != nx.Graph:
        raise nx.NetworkXException("Graph must be a simple undirected graph!")
    
    if not stopping_condition in ['UNIQUE_NODES','UNIQUE_EDGES','NODES','EDGES']:
        raise ValueError('Invalid stopping criteria, please choose one from ['+'"UNIQUE_NODES", "UNIQUE_EDGES", "NODES", "EDGES"'+']')
     
    if sample_size==None or sample_size<1 or (stopping_condition=='UNIQUE_NODES' and sample_size > len(G)) or (stopping_condition=='UNIQUE_EDGES' and sample_size > G.number_of_edges()):
        raise ValueError('Invalid sample size')
    
    sample_graph=nx.Graph(name=str(G.name+'_SPS_size'+str(sample_size))+'_stopping_condition'+stopping_condition)


    while True:
        s=random.choice(G.nodes())
        d=random.choice(G.nodes())
        if s!=d:
            try:
                path=nx.shortest_path(G,s,d)
                if stopping_condition=='UNIQUE_NODES':
                    if len(set(sample_graph.nodes()).union(set(path)))<=sample_size:
                        g_wrapper.add_path_to_graph(sample_graph, path)  
                        if sample_graph.number_of_nodes()==sample_size:
                            break
                    else:
                        if include_last_path_when_exceeds:
                            g_wrapper.add_path_to_graph(sample_graph, path)
                        else:
                            for i in range(0,len(path)):
                                if len(set(sample_graph.nodes()).union(set(path[0:i])))==sample_size:
                                    g_wrapper.add_path_to_graph(sample_graph, path[0:i])
                        break
                                    
                if stopping_condition=='UNIQUE_EDGES':
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
                if stopping_condition=='NODES':
                    if sample_graph.graph.get('number_of_nodes_repeated',0)+len(path)< sample_size:
                        g_wrapper.add_path_to_graph(sample_graph, path)
                    else:
                        if include_last_path_when_exceeds:
                            g_wrapper.add_path_to_graph(sample_graph, path)
                        else:
                            index_of_last_node=sample_size-sample_graph.graph['number_of_nodes_repeated']
                            g_wrapper.add_path_to_graph(sample_graph, path[0:index_of_last_node])
                        break
                    
                if stopping_condition=='EDGES':
                    if sample_graph.graph.get('number_of_edges_repeated',0)+len(path)-1<sample_size:
                        g_wrapper.add_path_to_graph(sample_graph,path)
                    else:
                        if include_last_path_when_exceeds:
                            g_wrapper.add_path_to_graph(sample_graph,path)
                        else:   
                            g_wrapper.add_path_to_graph(sample_graph,path[0: sample_size - sample_graph.graph['number_of_edges_repeated']+1  ]) 
                        break 
                    
            except nx.NetworkXNoPath:
                pass
            except nx.NetworkXError:
                pass
            
    if (stopping_condition=='UNIQUE_NODES' and sample_graph.number_of_nodes()<sample_size) or (stopping_condition=='UNIQUE_EDGES' and sample_graph.number_of_edges()<sample_size):
        raise ValueError('Desired sample size could not be reached.')
    
    if (stopping_condition=='NODES' and sample_graph.graph['number_of_nodes_repeated'] < sample_size) or (stopping_condition=='EDGES' and sample_graph.graph['number_of_edges_repeated'] < sample_size):
        raise ValueError('Desired sample size could not be reached.')
                
    return sample_graph   
        