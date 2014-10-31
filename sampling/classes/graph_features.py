from abc import ABCMeta, abstractmethod, abstractproperty
from collections import Counter
import networkx as nx
import numpy as np
import sampling.parallel as parallel_comp
import igraph

__all__=['SimpleGraphFeature','SimpleGraphDegree','SimpleGraphClusteringCoefficient','SimpleGraphPathLength']

class SimpleGraphFeature:
    __metaclass__ = ABCMeta

    @abstractmethod
    def compute_backend_distribution(self,G,S):
        pass
    
    @abstractmethod
    def compute_frontend_distribution(self,G):
        pass
    
    @abstractproperty
    def name(self):
        pass


class SimpleGraphDegree(SimpleGraphFeature):
    @property
    def name(self):
        return 'degree'

    def compute_frontend_distribution(self,G, normalize=True):
        #return context().compute_frontend_distribution_of_degree(G, normalize)
        dic = dict(Counter(nx.degree(G).values()))
        #iG=igraph.Graph(len(G), edges=G.edges())
        #dic = dict(Counter(iG.degree()))
        #if dic!=dic2:
        #    print 'dic:',dic
        #    print 'dic2:',dic2
        total = sum(dic.values())
        return {k:float(v)/total for k,v in dic.items()} if normalize else dic
        
    def compute_backend_distribution(self,G,S, normalize=True):
        #return context().compute_backend_distribution_of_degree(G,S, normalize)
        dic = dict(Counter(nx.degree(G,S.nodes()).values()))
        #iG=igraph.Graph(G.edges())
        #dic = dict(Counter(iG.degree(S.nodes())))
        
        #if dic!=dic2:
        #    print 'dic:',dic
        #    print 'dic2:',dic2
        total = sum(dic.values())
        return {k:float(v)/total for k,v in dic.items()} if normalize else dic


#     def compute_statistics(self,G,S=None):
# ##        return pc.run(ParallelDegreeTask(G,S))
#         dic={}
#         if S==None:
#             dic = dict(Counter(nx.degree(G).values()))
#         else:
#             dic = dict(Counter(nx.degree(G,S.nodes()).values()))
# 
#         total=sum(dic.values())
#         dic={k:float(v)/total for k,v in dic.items()}
# 
#         return dic
        
class SimpleGraphClusteringCoefficient(SimpleGraphFeature):
    @property
    def name(self):
        return 'clustering coefficient'
    
    def compute_frontend_distribution(self, G, normalize=True, num_of_bins=1000):
        #clust2=nx.clustering(G)
        #bins=np.linspace(0,1,num_of_bins+1)
        #digitized2=np.digitize(clust2.values(),bins)/float(num_of_bins)
        #digitized2=digitized2-1.0/num_of_bins
        #dic2=dict(Counter(digitized2.tolist()))
        #print G.number_of_nodes(),G.number_of_edges()
        igr=igraph.Graph(n=G.number_of_nodes(), edges=nx.convert_node_labels_to_integers(G, first_label=0).edges())
        clust=igr.transitivity_local_undirected(mode="zero")
        bins=np.linspace(0,1,num_of_bins+1)
        #digitized=np.digitize(clust.values(),bins)/float(num_of_bins)
        digitized=np.digitize(clust,bins)/float(num_of_bins)
        digitized=digitized-1.0/num_of_bins
        dic=dict(Counter(digitized.tolist()))
        
        total=sum(dic.values())
        return {k:float(v)/total for k,v in dic.items()} if normalize else dic
        
    def compute_backend_distribution(self, G, S, normalize=True, num_of_bins=1000):
        
        #clust=nx.clustering(G,nodes=S)
        igr=igraph.Graph(nx.convert_node_labels_to_integers(G, first_label=0).edges())
        clust=igr.transitivity_local_undirected(vertices=S.nodes(), mode="zero")
        bins=np.linspace(0,1,num_of_bins+1)
        digitized=np.digitize(clust,bins)/float(num_of_bins)
        #digitized=np.digitize(clust.values(),bins)/float(num_of_bins)
        digitized=digitized-1.0/num_of_bins
        dic=dict(Counter(digitized.tolist()))
        total=sum(dic.values())
        return {k:float(v)/total for k,v in dic.items()} if normalize else dic
    
#     def compute_statistics(self,G,S=None):
# ##        return pc.run(ParallelClusteringCoefficientTask(G,S))
#         if S==None:
#             clust=nx.clustering(G)
#             bins=np.linspace(0,1,1001)
#             digitized=np.digitize(clust.values(),bins)/1000.0
#             dic=dict(Counter(digitized.tolist()))
#             total=sum(dic.values())
#             dic={k:float(v)/total for k,v in dic.items()}
#         else:
#             clust=nx.clustering(G,nodes=S)
#             bins=np.linspace(0,1,1001)
#             digitized=np.digitize(clust.values(),bins)/1000.0
#             dic=dict(Counter(digitized.tolist()))
#             total=sum(dic.values())
#             dic={k:float(v)/total for k,v in dic.items()}
#         return dic
    
class SimpleGraphPathLength(SimpleGraphFeature):
    @property
    def name(self):
        return 'path length'

    def compute_frontend_distribution(self,G, normalize=True):
        #=======================================================================
        # igr=igraph.Graph(nx.convert_node_labels_to_integers(G, first_label=0).edges())
        # h=igr.path_length_hist(igr)
        #  
        # pld= {b[0]:b[2] for b in h.bins()}
        # if normalize:
        #     total=sum(pld.values())
        #     #sum_dic={k:v/total for k,v in sum_dic.items()}
        #     pld= {k:v/float(total) for k,v in pld.items()}
        #
        #return {0:1} if len(pld)==0 else pld
        #=======================================================================
        return parallel_comp.parallel_computer.run(parallel_comp.ParallelShortestPathTask(G) , normalize)
    def compute_backend_distribution(self,G,S, normalize=True):
        #res=smp.parallel_computer.run(smp.ParallelShortestPathTask(G,S,chunk_size=len(S)/multiprocessing.cpu_count()), normalize)
        res=parallel_comp.parallel_computer.run(parallel_comp.ParallelShortestPathTask(G,S), normalize)
        return res
    