'''
Created on Aug 30, 2013

@author: Emrah Cem{emrah.cem@utdallas.edu}
'''
import random
from sampling.sampling_algorithms import *

__all__=['add_path_to_graph','add_node_to_graph','add_edge_to_graph','generate_edge']



def generate_edge(G, with_replacement):
    if with_replacement:
        while True:
            yield random.choice(G.edges())
    else:
        edge_list=random.sample(G.edges(),G.number_of_edges())#this will shuffle edges
        for e in edge_list:
            yield e
         
def add_path_to_graph(G,path):
    if len(path)==1:
        add_node_to_graph(G,path[0])
    else:
        G.add_path(path)
        for n in path:
            G.node[n]['times_selected']=G.node[n].get('times_selected',0)+1
        u=path[0]
        for v in path[1:]:
            G.edge[u][v]['times_selected']=G.edge[u][v].get('times_selected',0)+1
            u=v
        G.graph['number_of_nodes_repeated']=G.graph.get('number_of_nodes_repeated',0)+len(path)
        G.graph['number_of_edges_repeated']=G.graph.get('number_of_edges_repeated',0)+len(path)-1
        
def add_node_to_graph(G,n):
    G.add_node(n)
    G.node[n]['times_selected']=G.node[n].get('times_selected',0)+1
    G.graph['number_of_nodes_repeated']=G.graph.get('number_of_nodes_repeated',0)+1

def add_edge_to_graph(G,e, add_nodes=True):
    G.add_edge(*e)
    G.edge[e[0]][e[1]]['times_selected']=G.edge[e[0]][e[1]].get('times_selected',0)+1
    if add_nodes:
        add_node_to_graph(G, e[0])
        add_node_to_graph(G, e[1])
    G.graph['number_of_edges_repeated']=G.graph.get('number_of_edges_repeated',0)+1


if __name__ =="__main__":

    import matplotlib.pyplot as plt
    from matplotlib.ticker import MultipleLocator
    import numpy as np
    import matplotlib.cm as cm
    pop_size=200
    
    sample_size=50
    #print 'generating graph'
    #===========================================================================
    G=nx.fast_gnp_random_graph(pop_size, 0.02)
    
    # print 'collecting sample'
    import time
    t=time.time()
    sample=kk_path_sampler(G, sample_size, K=10, stopping_condition='UNIQUE_NODES')
    #sample=induced_random_vertex_sampler(G, sample_size, with_replacement=False)
    print time.time()-t
    # #sample=random_edge_sampler(G, sample_size, stopping_condition='EDGES', with_replacement=True)
    # 
    # print 'number of unique nodes:',sample.number_of_nodes()
    # print 'number of unique edges:',sample.number_of_edges()
    # print 'number of nodes:',sample.graph.get('number_of_nodes_repeated',0)
    # print 'number of edges:',sample.graph.get('number_of_edges_repeated',0)
    #===========================================================================

    from scipy.stats import norm
#===============================================================================
# 
# 
#     G=nx.erdos_renyi_graph(1000,10)
#     sample_sizes=range(50,1000,50)
#     
#     result={}
#     l2=[]
#     for size in sample_sizes:
#         print size
#         l=[]
#         sampler=smp.InducedRandomVertexSampler(size, with_replacement=False)
#         for i in xrange(0,100):
#             #print i
#             t=time.time()
#             res=sampler.sample(G)
#             print time.time()-t
#             #print (size - len([r for r in res.degree().values() if r >0]))/float(size)
#             #l.append((size - len([r for r in res.degree().values() if r >0]))/float(size))
#         #(mu, sigma) = norm.fit(l)
#         #l2.append((mu,sigma))
#===============================================================================

    n_color=[G.degree(n) for n in sample.nodes()]
    e_color=[float(data.get('times_selected',0)) for e0,e1,data in sample.edges_iter(data=True)]
      
    pos_vals=nx.spring_layout(G)
    node_color_map=cm.get_cmap('gist_yarg')
    edge_color_map=cm.get_cmap('jet')
    nx.draw(G,pos=pos_vals, alpha=0.07, with_labels=False)
      
    if sample.graph.has_key('source_nodes'):
        nx.draw_networkx_nodes(sample, pos_vals, nodelist=sample.graph['source_nodes'], alpha=0.7, node_shape='s', node_size=600, node_color='chocolate')
    if sample.graph.has_key('destination_nodes'):
        nx.draw_networkx_nodes(sample, pos_vals, nodelist=sample.graph['destination_nodes'],alpha=0.7,  node_shape='s', node_size=600, node_color='#87CEFA')
    if sample.graph.has_key('vantage_points'):
        nx.draw_networkx_nodes(sample, pos_vals, nodelist=sample.graph['vantage_points'], alpha=0.7,  node_shape='s', node_size=600, node_color='chocolate')
    if sample.graph.has_key('induced_edges'):
        induced_edges=nx.draw_networkx_edges(G, pos_vals, edgelist=sample.graph['induced_edges'], width=4, edge_color='chocolate', alpha=0.7,)
      
    if len(n_color)>0:
        nodes=nx.draw_networkx_nodes(sample, pos_vals, nodelist=sample.nodes(),  node_color=n_color, cmap=node_color_map, vmin=min(n_color), vmax=max(n_color), with_labels=False)
        if min(n_color) != max(n_color):
            plt.sci(nodes)
            res=np.linspace(min(n_color), max(n_color), 10)
            cb=plt.colorbar(shrink=.7)
            if max(n_color)-min(n_color)< 10 or res[1]-res[0]< 1:
                cb.locator=MultipleLocator(1)
                cb.update_ticks()
            cb.set_label("Node degree")
  
    if len(e_color)>0:
        edges=nx.draw_networkx_edges(G, pos_vals, edgelist=sample.edges(),width=2, edge_color=e_color, edge_cmap=edge_color_map, edge_vmin=min(e_color),edge_vmax=max(e_color))
        if min(e_color) != max(e_color):
            plt.sci(edges)
            res=np.linspace(min(e_color), max(e_color), 10)
            cb=plt.colorbar(orientation='horizontal' , shrink=.7)
            if max(e_color)-min(e_color)< 10 or res[1]-res[0]< 1:
                cb.locator=MultipleLocator(1)
                cb.update_ticks()
            cb.set_label("# of times edge was selected")
      
    for n in sample.nodes():
        x,y=pos_vals[n]
        plt.text(x,y-0.01,s=str(n)+'-'+str(sample.node[n]['times_selected']),horizontalalignment='center', fontdict={'color'  : 'darkred','weight' : 'bold', 'size'   : 12})     
    plt.gcf().savefig('test.pdf') 
    plt.show()
