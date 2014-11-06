from abc import ABCMeta, abstractmethod
import networkx as nx 
import logging 

__all__=['GraphGenerator','BarabasiAlbertGraphGenerator','WattsStrogatzGraphGenerator','ErdosRenyiGraphGenerator','FromFileGraphGenerator']

logger = logging.getLogger(__name__)

class GraphGenerator:
    __metaclass__ = ABCMeta
    
    def __init__(self, name, abbreviation, seed, folder_name, distribution_file_name):
        self.G=None
        self._name=name#(n='+str(n)+',m='+str(m)+')'
        self._abbreviation=abbreviation 
        self._folder_name=folder_name
        self.seed=seed
        self.distribution_file_name=distribution_file_name
     
    @property
    def name(self):
        return self._name
    
    @property
    def abbreviation(self):
        return self._abbreviation
    
    @property
    def folder_name(self):
        return self._folder_name
    
    @abstractmethod
    def generate(self):
        self.G.graph['name']=self.name
        self.G.graph['folder_name']=self.folder_name
        self.G.graph['distribution_file_name']=self.distribution_file_name
        self.G.graph['abbreviation']=self.abbreviation
        #logger.info('-'*30+self.name+'-'*30)
        logger.info("Generating %s" % self.name)
     
    def largest_connected_component(self,G):
        return sorted(nx.connected_component_subgraphs(G), key = len, reverse=True)[0] #nx.connected_component_subgraphs(G)[0]

class BarabasiAlbertGraphGenerator(GraphGenerator):
     
    __metaclass__= ABCMeta
     
    def __init__(self,n,m,seed=None, name='Barabasi-Albert Graph', abbreviation='BA', folder_name='Barabasi-Albert-Graph', distribution_file_name=None):
        super(BarabasiAlbertGraphGenerator, self).__init__(name, abbreviation, seed, folder_name, distribution_file_name)
        self.n=n
        self.m=m 
    
    def generate(self):
        self.G=nx.convert_node_labels_to_integers(self.largest_connected_component(nx.barabasi_albert_graph(self.n, self.m, self.seed)), first_label=0)
        GraphGenerator.generate(self)
        return self.G
       
class WattsStrogatzGraphGenerator(GraphGenerator):
    __metaclass__= ABCMeta
     
    def __init__(self,n,k,p,seed=None, name='Watts-Strogatz Graph', abbreviation='WS', folder_name='Watts-Strogatz-Graph',distribution_file_name=None):
        super(WattsStrogatzGraphGenerator, self).__init__(name, abbreviation, seed, folder_name, distribution_file_name)
        self.n=n
        self.k=k
        self.p=p
     
    def generate(self):
        self.G=nx.convert_node_labels_to_integers(self.largest_connected_component(nx.watts_strogatz_graph(self.n, self.k, self.p, self.seed)), first_label=0)
        GraphGenerator.generate(self)
        return self.G

class ErdosRenyiGraphGenerator(GraphGenerator):
 
    __metaclass__= ABCMeta
     
    def __init__(self,n,p,seed=None,directed=False, name='Erdos-Renyi Graph', abbreviation='ER', folder_name='Erdos-Renyi-Graph', distribution_file_name=None):
        super(ErdosRenyiGraphGenerator, self).__init__(name, abbreviation, seed, folder_name, distribution_file_name)
        self.n=n
        self.p=p
        self.directed=directed

    def generate(self):
        self.G=nx.convert_node_labels_to_integers(self.largest_connected_component(nx.erdos_renyi_graph(self.n, self.p, self.seed)), first_label=0)
        GraphGenerator.generate(self)
        return self.G      

class FromFileGraphGenerator(GraphGenerator):
    __metaclass__= ABCMeta
     
    def __init__(self, path_to_file, name, abbreviation, seed=None, folder_name='Real-World-Graph', distribution_file_name=None):
        super(FromFileGraphGenerator, self).__init__(name, abbreviation, seed, folder_name, distribution_file_name)
        self.path=path_to_file
        
    def generate(self, **kwargs):
        self.G=nx.convert_node_labels_to_integers(self.largest_connected_component(nx.read_edgelist(path=self.path, nodetype=int, **kwargs)), first_label=0)
        GraphGenerator.generate(self)
        return self.G 


if __name__ == '__main__':
    
    g=FromFileGraphGenerator(path_to_file='../../networks_real/yeast_protein_interaction.txt', name='yeast pro', abbreviation='y-ppi', seed=1)
    #g.generate(smp.NetworkXContext())
    #print g.generate(smp.IGraphContext())
    #===========================================================================
    # nxgen=FromFileNetworkXGraphGenerator('../../networks_real/yeast_protein_interaction.txt', "Yeast Protein", 'y-protein', 1)
    # igen=FromFileIGraphGraphGenerator('../../networks_real/yeast_protein_interaction.txt', "Yeast Protein", 'y-protein', 1)
    # nxgen.generate()
    # igen.generate()
    #===========================================================================
    
    #===========================================================================
    # context=GraphGenerationContext(NetworkXBarabasiAlbertGraphGenerator(100, 10, seed=1))
    # g=context.generate()
    #===========================================================================
    
#===============================================================================
# 
# class GraphGenerationStrategy:
#     __metaclass__ = ABCMeta
#     
#     @property
#     def name(self):
#         return self._name
# 
#     @property
#     def abbreviation(self):
#         return self._abbreviation
#     
#     def __init__(self, name, abbreviation, seed):
#         self._name=name
#         self._abbreviation=abbreviation
#         self.seed=seed
#     
#     def largest_connected_component(self,G):
#         return nx.connected_component_subgraphs(G)[0]
#         
#     @abstractmethod
#     def generate(self):
#         pass
#     
# 
# class IGraphGraphGenerationStrategy(GraphGenerationStrategy):
#     __metaclass__ = ABCMeta
#     
#     def __init_(self, name, abbreviation, seed):
#         super(IGraphGraphGenerationStrategy, self).__init__(name, abbreviation, seed)
#     
#     @abstractmethod
#     def generate(self):
#         pass
# 
# class NetworkXGraphGenerationStrategy(GraphGenerationStrategy):
#     __metaclass__ = ABCMeta
#     
#     @abstractmethod
#     def generate(self):
#         pass
# 
# 
# class GraphGenerationContext:
#     
#     def __init__(self, graph_generation_strategy):
#         self.graph_generation_strategy=graph_generation_strategy
#         
#     def generate(self):
#         return self.graph_generation_strategy.generate()
# 
# 
#         
# class NetworkXBarabasiAlbertGraphGenerator(NetworkXGraphGenerationStrategy):
#     
#     def __init__(self, n, m, name='Barabasi-Albert Graph', abbreviation='BA', seed=None):
#         super(NetworkXBarabasiAlbertGraphGenerator, self).__init__(name, abbreviation, seed)
#         self.n=n
#         self.m=m
# 
#     def generate(self):
#         return self.largest_connected_component(nx.barabasi_albert_graph(self.n, self.m, self.seed))
#         
# 
# class NetworkXWattsStrogatzGraphGenerator(NetworkXGraphGenerationStrategy):
#     def __init__(self, n, k, p, name='Watts-Strogatz Graph', abbreviation='WS', seed=None):
#         super(NetworkXWattsStrogatzGraphGenerator, self).__init(name, abbreviation, seed)
#         self.n=n
#         self.k=k
#         self.p=p    
#     
#     def generate(self):
#         return self.largest_connected_component(nx.watts_strogatz_graph(self.n, self.k, self.p, self.seed))
# 
# class NetworkXErdosRenyiGraphGenerator(NetworkXGraphGenerationStrategy):
#     
#     def __init__(self, n, p, directed=False, name='Erdos-Renyi Graph', abbreviation='ER', seed=None):
#         super(NetworkXErdosRenyiGraphGenerator, self).__init__(name, abbreviation, seed)
#         self.n=n
#         self.p=p
#         self.directed=directed
#     def generate(self):
#         return self.largest_connected_component(nx.erdos_renyi_graph(self.n, self.p, self.seed, self.directed))
# 
# class NetworkXFromFileGraphGenerator(NetworkXGraphGenerationStrategy):
#     def __init__(self, path_to_file, name, abbreviation, **kwargs):
#         super(NetworkXFromFileGraphGenerator, self).__init__(name, abbreviation, None)
#         self.path_to_file=path_to_file
#         self.kwargs=kwargs
#     def generate(self):
#         return self.largest_connected_component(nx.read_edgelist(self.path_to_file, self.kwargs))
# 
# 
# 
# class IGraphBarabasiAlbertGraphGenerator(IGraphGraphGenerationStrategy):
#     def __init__(self, n, m, name='Barabasi-Albert Graph', abbreviation='BA', seed=None):
#         super(IGraphBarabasiAlbertGraphGenerator, self).__init__(name, abbreviation, seed)
#         self.n=n
#         self.m=m
#     def generate(self):
#         return igraph.Graph(NetworkXBarabasiAlbertGraphGenerator(n=self.n, m=self.m, name=self.name, abbreviation=self.abbreviation, seed=self.seed).generate().edges())
# 
# class IGraphWattsStrogatzGraphGenerator(IGraphGraphGenerationStrategy):
#     def __init__(self, n, k, p, name='Watts-Strogatz Graph', abbreviation='WS', seed=None):
#         super(IGraphWattsStrogatzGraphGenerator, self).__init(name, abbreviation, seed)
#         self.n=n
#         self.k=k
#         self.p=p
#     def generate(self):
#         return igraph.Graph(NetworkXWattsStrogatzGraphGenerator(n=self.n, k=self.k, p=self.p, name=self.name, abbreviation=self.abbreviation, seed=self.seed).generate().edges())
# 
# class IGraphErdosRenyiGraphGenerator(IGraphGraphGenerationStrategy):
#     def __init__(self, n, p, directed=False, name='Erdos-Renyi Graph', abbreviation='ER', seed=None):
#         super(IGraphErdosRenyiGraphGenerator, self).__init__(name, abbreviation, seed)
#         self.n=n
#         self.p=p
#         self.directed=directed
#     def generate(self):
#         return igraph.Graph(NetworkXErdosRenyiGraphGenerator(n=self.n, p=self.p, name=self.name, abbreviation=self.abbreviation, seed=self.seed).generate().edges())
# 
# class IGraphFromFileGraphGenerator(IGraphGraphGenerationStrategy):
#     def __init__(self, path_to_file, name, abbreviation, **kwargs):
#         super(IGraphFromFileGraphGenerator, self).__init__(name, abbreviation, None)
#         self.path_to_file=path_to_file
#         self.kwargs=kwargs
# 
#     def generate(self):
#         return igraph.Graph(NetworkXFromFileGraphGenerator(self.path_to_file, self.name, self.abbreviation).generate().edges())

# class BarabasiAlbertNetworkXGraphGenerator(BarabasiAlbertGraphGenerator):
#     
#     def __init__(self,n,m,seed=None, name='Barabasi-Albert Graph', abbreviation='BA'):
#         super(BarabasiAlbertNetworkXGraphGenerator,self).__init__(n,m,seed=seed, name=name, abbreviation=abbreviation)
#     
#     @smp.timed
#     @smp.log_graph_generation
#     def generate(self):
#         self.G=self.largest_connected_component(nx.barabasi_albert_graph(self.n, self.m, self.seed))
#         self.G.graph['name']=self.name
#         self.G.graph['params']= {'n':self.n, 'm':self.m}
#         self.G.graph['abbreviation']=self.abbreviation
#         return self.G
#     
# class BarabasiAlbertIGraphGraphGenerator(BarabasiAlbertGraphGenerator):
#     def __init__(self,n,m,seed=None, name='Barabasi-Albert Graph', abbreviation='BA'):
#         super(BarabasiAlbertIGraphGraphGenerator,self).__init__(n,m,seed=seed, name=name, abbreviation=abbreviation)
#     
#     @smp.timed
#     @smp.log_graph_generation
#     def generate(self):
#         return igraph.Graph(BarabasiAlbertNetworkXGraphGenerator(self.n,self.m,seed=self.seed, name=self.name, abbreviation=self.abbreviation).largest_connected_component(nx.barabasi_albert_graph(self.n, self.m, self.seed)).edges())
# 
#  
# class WattsStrogatzNetworkXGraphGenerator(WattsStrogatzGraphGenerator):
#     def __init__(self,n,k,p,seed=None, name='Watts-Strogatz Graph', abbreviation='WS'):
#         super(WattsStrogatzNetworkXGraphGenerator,self).__init__(n,k,p,seed=seed, name=name, abbreviation=abbreviation)
#     
#     @smp.timed
#     @smp.log_graph_generation
#     def generate(self):
#         self.G=self.largest_connected_component(nx.watts_strogatz_graph(self.n,self.k,self.p,self.seed))
#         self.G.graph['name']=self._name
#         self.G.graph['params']= {'n':self.n, 'k':self.k, 'p':self.p}
#         self.G.graph['abbreviation']="WS"
#         
#         return self.G
# 
# class WattsStrogatzIGraphGraphGenerator(WattsStrogatzGraphGenerator):
#     def __init__(self,n,k,p,seed=None, name='Watts-Strogatz Graph', abbreviation='WS'):
#         super(WattsStrogatzIGraphGraphGenerator,self).__init__(n,k,p,seed=seed, name=name, abbreviation=abbreviation)
#     
#     @smp.timed
#     @smp.log_graph_generation
#     def generate(self):
#         return igraph.Graph(WattsStrogatzNetworkXGraphGenerator(self.n,self.k,self.p,seed=self.seed,name=self.name).largest_connected_component(nx.watts_strogatz_graph(self.n, self.k, self.p, self.seed)).edges())
#         
# 

# class ErdosRenyiNetworkXGraphGenerator(ErdosRenyiGraphGenerator):
#     
#     def __init__(self,n,p,seed=None, directed=False, name='Erdos-Renyi Graph', abbreviation='ER'):
#         super(ErdosRenyiNetworkXGraphGenerator,self).__init__(n,p,seed=seed, directed=directed, name=name, abbreviation=abbreviation)
#         
#     @smp.timed
#     @smp.log_graph_generation
#     def generate(self):
#         self.G=self.largest_connected_component(nx.erdos_renyi_graph(self.n,self.p,self.seed,self.directed))
#         self.G.graph['name']=self._name
#         self.G.graph['params']= {'n':self.n, 'p':self.p}
#         self.G.graph['abbreviation']="ER"
#         return self.G
#     
# class ErdosRenyiIGraphGraphGenerator(ErdosRenyiGraphGenerator):
#     def __init__(self,n,p,seed=False, directed=None, name='Erdos-Renyi Graph', abbreviation='ER'):
#         super(ErdosRenyiIGraphGraphGenerator,self).__init__(n,p,seed=seed, name=name, abbreviation=abbreviation)
#     
#     @smp.timed
#     @smp.log_graph_generation
#     def generate(self):
#         return igraph.Graph(ErdosRenyiNetworkXGraphGenerator(self.n,self.p,seed=self.seed,name=self.name, abbreviation=self.abbreviation).largest_connected_component(nx.erdos_renyi_graph(self.n,self.p, self.seed,self.directed)).edges())

# class FromFileNetworkXGraphGenerator(FromFileGraphGenerator):
#     
#     def __init__(self,path_to_file, name, abbreviation, seed=None):
#         super(FromFileNetworkXGraphGenerator,self).__init__(path_to_file, name, abbreviation, seed)
#     
#     @smp.timed
#     @smp.log_graph_generation
#     def generate(self):
#         self.G=self.largest_connected_component(nx.read_edgelist(self.path_to_file,nodetype=int)) 
#         self.G.graph['name']=self._name
#         self.G.graph['abbreviation']=self._abbreviation
#         for n in self.G.nodes_iter():
#             print n, self.G.neighbors(n)
#         return self.G    
# 
# class FromFileIGraphGraphGenerator(FromFileGraphGenerator):
# 
#     def __init__(self,path_to_file, name, abbreviation, seed=None):
#         super(FromFileIGraphGraphGenerator,self).__init__(path_to_file, name, abbreviation, seed)
#         
#     @smp.timed
#     @smp.log_graph_generation
#     def generate(self):
#         print igraph.Graph(FromFileNetworkXGraphGenerator(self.path_to_file,self.name, self.abbreviation, seed=self.seed).largest_connected_component(nx.read_edgelist(self.path_to_file,nodetype=int)).edges())
#===============================================================================

