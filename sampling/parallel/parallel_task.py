import math
import parallel_computer as pc
from abc import ABCMeta
import igraph
import networkx as nx

__all__=['ParallelDegreeTask',
         'ParallelClusteringCoefficientTask',
         'ParallelShortestPathTask']

class ParallelTask:
    __metaclass__ = ABCMeta

    def chunks(self, l, n):
        for i in xrange(0, len(l), n):
            yield l[i:i+n]
            
    def __init__(self,G,S=None,chunk_size=None):

        #=======================================================================
        # if S==None:
        #     if chunk_size==None:   
        #         self.chunk_gen=self.chunks(G.nodes(),int(math.sqrt(len(G))))
        #     else:
        #         self.chunk_gen=self.chunks(G.nodes(),chunk_size)
        # else:
        #     if chunk_size==None: 
        #         self.chunk_gen=self.chunks(S.nodes(),int(math.sqrt(len(S))))
        #     else:
        #         self.chunk_gen=self.chunks(S.nodes(),chunk_size)
        #=======================================================================
        if S==None:
            if chunk_size==None:   
                self.chunk_gen=self.chunks(list(xrange(len(G.vs))),int(math.sqrt(len(G.vs))))
            else:
                self.chunk_gen=self.chunks(list(xrange(len(G.vs))),chunk_size)
        else:
            if chunk_size==None: 
                self.chunk_gen=self.chunks(S.nodes(),int(math.sqrt(len(S))))
            else:
                self.chunk_gen=self.chunks(S.nodes(),chunk_size)

class ParallelDegreeTask(ParallelTask):

    def __init__(self,G,S=None,chunk_size=None):
        ParallelTask.__init__(self,G,S,chunk_size)
        self.TASKS=[(pc.degree_task,(G,chunk)) for chunk in self.chunk_gen]    

class ParallelClusteringCoefficientTask(ParallelTask):
    
    def __init__(self,G,S=None,chunk_size=None):
        ParallelTask.__init__(self,G,S,chunk_size)
        self.TASKS=[(pc.clustering_coefficient_task,(G,chunk)) for chunk in self.chunk_gen]    

class ParallelShortestPathTask(ParallelTask):
    
    def __init__(self,G,S=None,chunk_size=None):
        
        #=======================================================================
        # ParallelTask.__init__(self,G,S,chunk_size)
        # if S==None:
        #     self.TASKS=[(pc.shortest_path_task,(G,sources, None)) for sources in self.chunk_gen]
        # else:
        #     self.TASKS=[(pc.shortest_path_task,(G,sources, S.nodes())) for sources in self.chunk_gen]
        #=======================================================================
        
        
        
        igr=igraph.Graph(n=G.number_of_nodes(), edges=nx.convert_node_labels_to_integers(G, first_label=0).edges())
        ParallelTask.__init__(self,igr,S,chunk_size)
        if S==None:
            self.TASKS=[(pc.shortest_path_task,(igr,sources, None)) for sources in self.chunk_gen]
        else:
            self.TASKS=[(pc.shortest_path_task,(igr,sources, S.nodes())) for sources in self.chunk_gen]
