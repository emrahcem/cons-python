import networkx as nx
import random 
from itertools import product
import warnings 
import graph_wrapper as g_wrapper

__author__ = """Emrah Cem (emrah.cem@utdallas.edu)"""
__all__=['km_path_sampler']


def km_path_sampler(G, sample_size, K=None, M=None, source_nodes=None, destination_nodes=None, source_destination_nodes_can_overlap=False, stopping_condition='UNIQUE_NODES', fuzzy_select=True, include_last_path_when_exceeds=True):
#def km_path_sampler(G, sample_size, K, M, stop_at_sample_size=True, fuzzy_select=True):
    stopping_condition=str.upper(str(stopping_condition))
    if type(G) != nx.Graph:
        raise nx.NetworkXException("Graph must be a simple undirected graph!") 
    if not stopping_condition in ['UNIQUE_NODES','UNIQUE_EDGES','NODES','EDGES']:
        raise ValueError('Invalid stopping criteria, please choose one from ['+'"UNIQUE_NODES", "UNIQUE_EDGES", "NODES", "EDGES"'+']')
    if sample_size==None or sample_size<1 or (stopping_condition=='UNIQUE_NODES' and sample_size > len(G)) or (stopping_condition=='UNIQUE_EDGES' and sample_size > G.number_of_edges()):
        raise ValueError('Invalid sample size')
    
    if source_nodes is not None:
        if not set(source_nodes).issubset(G.nodes()):
            raise ValueError("Source nodes must be a subset of node set of population graph")
        else:
            if K is not None: 
                warnings.warn('parameter K was ignored, since source nodes were given explicitly', UserWarning)
    else:
        if K is None:
            source_nodes=random.sample([x for x in xrange(0,len(G))],int(len(G)*3/100))
        else:
            if K<2 or K>len(G):
                raise ValueError("Number of source points should be in [2,"+str(len(G))+']')
            source_nodes=random.sample([x for x in xrange(0,len(G))],K)
            
    if destination_nodes is not None:
        if not set(destination_nodes).issubset(G.nodes()):
            raise ValueError("Destination nodes must be a subset of node set of population graph")
        if not source_destination_nodes_can_overlap and len(set(source_nodes).intersection(set(destination_nodes)))>0:
            raise ValueError("Destination nodes can not overlap with source nodes")
        if M is not None: 
            warnings.warn('parameter M was ignored, since destination points were given explicitly', UserWarning)
    else:
        if M is None:
            if source_destination_nodes_can_overlap:
                destination_nodes=random.sample([x for x in xrange(0,len(G))],int(len(G)*7/100))
            else:
                destination_nodes=random.sample([x for x in set(G.nodes())-source_nodes],int(len(G)*7/100))
        else:
            if M<2 or M>len(G):
                raise ValueError("Number of source points should be in [2,"+str(len(G))+']')
            if source_destination_nodes_can_overlap:
                destination_nodes=random.sample([x for x in xrange(0,len(G))],M)
            else:
                if len(set(G.nodes())-set(source_nodes)) < int(len(source_nodes)):
                    raise ValueError("There is not enough destination points to select (they should non-overlap with source nodes)")
                else:
                    destination_nodes=random.sample([x for x in set(G.nodes())-set(source_nodes)],M)
    
        
    #nodes= random.sample([x for x in xrange(0,len(G))],K+M)
    #source_nodes=nodes[:K]
    #print 'source:',source_nodes
    #destination_nodes=nodes[K:]
    #print 'dest:',destination_nodes
    sample_graph=nx.Graph(name=str(G.name+'_KM_size'+str(sample_size)+'_stopping_condition'+stopping_condition+'_k'+str(len(source_nodes))+ '_m'+str(len(destination_nodes)) ))  
    stopLooping=False
    
    
    
    s_d_tuples=[s_d_tuple for s_d_tuple in product(*(source_nodes,destination_nodes)) if s_d_tuple[0]!=s_d_tuple[1]]
    if fuzzy_select:
        random.shuffle(s_d_tuples)
    
    for s_d_tuple in s_d_tuples:
        if stopLooping:
            break   
        try:
            path=nx.shortest_path(G,*s_d_tuple)
            if stopping_condition=='UNIQUE_NODES':
                if len(set(sample_graph.nodes()).union(set(path)))>sample_size:#check if the whole path is added, desired sample size is exceeded, if so add the path partially
                    if include_last_path_when_exceeds:
                        g_wrapper.add_path_to_graph(sample_graph, path)
                    else:
                        for i in range(0,len(path)):
                            if len(set(sample_graph.nodes()).union(set(path[0:i])))==sample_size:
                                g_wrapper.add_path_to_graph(sample_graph, path[0:i])
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
                        #print sample_size - sample_graph.graph['number_of_edges_repeated']+1
                        g_wrapper.add_path_to_graph(sample_graph,path[0: sample_size - sample_graph.graph['number_of_edges_repeated']+1  ]) 
                    
                    stopLooping=True
                       
        except nx.NetworkXNoPath:
            pass
        except nx.NetworkXError:
            pass
        
    if (stopping_condition=='UNIQUE_NODES' and sample_graph.number_of_nodes()<sample_size) or (stopping_condition=='UNIQUE_EDGES' and sample_graph.number_of_edges()<sample_size):
        #print 'desired size not reached'
        raise ValueError('Desired sample size could not be reached.')
    
    if (stopping_condition=='NODES' and sample_graph.graph['number_of_nodes_repeated'] < sample_size) or (stopping_condition=='EDGES' and sample_graph.graph['number_of_edges_repeated'] < sample_size):
        raise ValueError('Desired sample size could not be reached.')
     
    sample_graph.graph['source_nodes']=source_nodes
    sample_graph.graph['destination_nodes']=destination_nodes 
    return sample_graph


if __name__ == '__main__':
    from matplotlib.ticker import MultipleLocator
    import numpy as np
    import matplotlib.cm as cm
    import matplotlib.pyplot as plt
    sample_size=5
    pop_size=10
    k=5
    m=5
    G=nx.barabasi_albert_graph(pop_size, 2)
    
    #source_nodes=random.sample([x for x in xrange(0,len(G))],k)
    #destination_nodes=random.sample([x for x in xrange(0,len(G))],m)
    sample=km_path_sampler(G, sample_size, K=k,M=m, stopping_condition='NODES', fuzzy_select=True, include_last_path_when_exceeds=False, source_destination_nodes_can_overlap=False)
    print 'sources:',sample.graph['source_nodes']
    print 'destinations:',sample.graph['destination_nodes']
    print sample.graph['number_of_edges_repeated']

    plt.figure(2)
    n_color=list([G.degree(n) for n in sample.nodes()])
    e_color=list([float(data.get('times_selected',0)) for e0,e1,data in sample.edges_iter(data=True)])
      
    pos_vals=nx.spring_layout(G)
    node_color_map=cm.get_cmap('gist_yarg')
    edge_color_map=cm.get_cmap('jet')
    nx.draw(G,pos=pos_vals, alpha=0.07, with_labels=False)
     
    nx.draw_networkx_nodes(sample, pos_vals, nodelist=sample.graph['source_nodes'], alpha=0.7, node_shape='s', node_size=600, node_color='chocolate')
    nx.draw_networkx_nodes(sample, pos_vals, nodelist=sample.graph['destination_nodes'],alpha=0.7,  node_shape='s', node_size=600, node_color='#87CEFA')
      
    nodes=nx.draw_networkx_nodes(sample, pos_vals, nodelist=sample.nodes(),  node_color=n_color, cmap=node_color_map, vmin=min(n_color), vmax=max(n_color))
    edges=nx.draw_networkx_edges(G, pos_vals, edgelist=sample.edges(),width=2, edge_color=e_color, edge_cmap=edge_color_map, edge_vmin=min(e_color),edge_vmax=max(e_color))
 
    for n in sample.nodes():
        x,y=pos_vals[n]
        plt.text(x,y-0.005,s=str(n)+'-'+str(sample.node[n]['times_selected']),horizontalalignment='center', fontdict={'color'  : 'darkred','weight' : 'bold', 'size'   : 12})

    if min(n_color) != max(n_color):
        plt.sci(nodes)
        res=np.linspace(min(n_color), max(n_color), 10)
        cb=plt.colorbar(shrink=.7)
        print len(res) , res[1], res[0]
        if max(n_color)-min(n_color)< 10 or res[1]-res[0]< 1:
            cb.locator=MultipleLocator(1)
            cb.update_ticks()
    cb.set_label("Node degree")

    if min(e_color) != max(e_color):
        plt.sci(edges)
        res=np.linspace(min(e_color), max(e_color), 10)
        cb=plt.colorbar(orientation='horizontal' , shrink=.7)
        if max(e_color)-min(e_color)< 10 or res[1]-res[0]< 1:
            cb.locator=MultipleLocator(1)
            cb.update_ticks()
        
        cb.set_label("# of times edge was selected")

    plt.show()
    
        
