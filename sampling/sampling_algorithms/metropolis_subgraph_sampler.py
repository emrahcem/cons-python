'''
Created on Jul 2, 2013

@author: Emrah Cem{emrah.cem@utdallas.edu}
'''

import networkx as nx
import random
from math import pow,log10

import sampling as smp
from pandas.core.series import Series
from matplotlib.pyplot import gca
import sys

def __divergence(G, S, divergence, feature):
    
    return divergence.compute(smp.FrontendQuery(G).run_query(feature) ,smp.FrontendQuery(S).run_query(feature))
    
def metropolis_subgraph_sampler(G, sample_node_size, divergence, feature, num_of_iter, p, T, gamma):
    current_subgraph=nx.subgraph(G, random.sample(G.nodes(),sample_node_size))
    best_subgraph= current_subgraph
    div_scores={}
    s=set(G.nodes()).difference(set(current_subgraph.nodes()))
    for i in range(0, num_of_iter):
        sys.stdout.write("\r%{0} completed".format(100.0* float(i)/num_of_iter))
        sys.stdout.flush()
        v= random.choice(current_subgraph.nodes())
        #s=set(G.nodes()).difference(set(current_subgraph.nodes()))
        s.add(v) 
        w= random.choice(list(s))
        
    
        #new_subgraph= nx.Graph.copy(current_subgraph)
        #new_subgraph.add_edges_from(G.edges(w))
        #new_subgraph.remove_node(v)
        
        
        
        new_nodes=current_subgraph.nodes()
        new_nodes.remove(v)
        new_nodes.append(w)   
        
        new_subgraph=nx.subgraph(G, new_nodes)
        alpha=random.random()
         
        accept_prob=pow(__divergence(G,current_subgraph,divergence,feature)/__divergence(G,new_subgraph,divergence,feature), float(p))
        if alpha < accept_prob:
            current_subgraph=new_subgraph
            s.remove(w)
        else:
            s.remove(v)

        if __divergence(G,current_subgraph,divergence,feature) < __divergence(G,best_subgraph,divergence,feature):
            best_subgraph=current_subgraph
        div_scores[i]=__divergence(G,best_subgraph,divergence,feature)
        T=gamma*T
    nx.write_gml(best_subgraph, "best_subgraph.gml")
    return best_subgraph, div_scores
    
if __name__ == '__main__':
    import analytics
    import pylab
    G=nx.barabasi_albert_graph(1000, 10, 1)
    p=10*G.number_of_edges()*log10(G.number_of_nodes())/G.number_of_nodes() 
    best, div=metropolis_subgraph_sampler(G, 100, analytics.DivergenceMetrics.JensenShannonDivergence, smp.SimpleGraphDegree(), 1000, p, 10, 2)
    #print 'div:',div
    Series(div).plot()
    gca().set_ylabel('JS-Divergence')
    gca().set_xlabel('# of iterations')
    pylab.show()
    #pylab.plot(div)
    