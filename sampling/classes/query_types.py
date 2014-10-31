from abc import ABCMeta, abstractmethod, abstractproperty

__all__=['Query','BackendQuery','FrontendQuery']

class Query:
    __metaclass__ = ABCMeta

    @abstractmethod
    def run_query(self,feature):
        return

    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def abbreviation(self):
        pass
    
#     def compute_statistics(self, feature, graph, sample_graph=None):
#         if type(self) == BackendQuery:
#             return feature.compute_backend_statistics(graph, sample_graph)
#         elif  type(self) == FrontendQuery:
#             return feature.compute_frontend_statistics(graph)
#             
#         #return feature.compute_statistics(graph,sample_graph)
#     
class BackendQuery(Query):
    @property
    def name(self):
        return 'Backend Query'
    
    @property
    def abbreviation(self):
        return 'BE'
    
    def __init__(self, population_graph=None, sample_graph=None):
        self.population_graph=population_graph
        self.sample_graph=sample_graph
    
    def set_population_graph(self, population_graph):
        self.population_graph= population_graph
    
    def set_sample_graph(self, sample_graph):
        self.sample_graph= sample_graph
        
    def run_query(self, feature):
        if self.population_graph == None or self.sample_graph == None:
            raise TypeError('Both population graph and sample graph must be set')
        return feature.compute_backend_distribution(self.population_graph, self.sample_graph)
        #return self.compute_statistics(feature, self.population_graph, self.sample_graph)
        
class FrontendQuery(Query):
    @property
    def name(self):
        return 'Frontend Query'

    @property
    def abbreviation(self):
        return 'FE'
    
    def __init__(self, graph=None):
        self.graph=graph
    
    def set_graph(self, graph):
        self.graph = graph
        
    def run_query(self, feature):
        if self.graph == None:
            raise TypeError('Graph must be set')
        return feature.compute_frontend_distribution(self.graph)
        #return self.compute_statistics(feature, self.graph)