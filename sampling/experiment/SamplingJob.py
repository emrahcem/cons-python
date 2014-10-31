'''
Created on May 17, 2013

@author: ecem
'''

import sampling as smp

class SamplingJob:
    '''
    classdocs
    '''

    def __init__(self,name, times_to_sample=1):
        '''
        Constructor
        '''
        self.graph_gen_list=[]
        self.feature_list=[]
        self.sampler_list=[]
        self.query_list=[]
        self.times_to_sample=times_to_sample
        self.name=name
        
    def add_graph_gen(self, graph_gen):
        if not issubclass(type(graph_gen),smp.GraphGenerator):
            raise smp.InvalidGraphGeneratorException('Invalid Graph generator. Generator should extend "GraphGenerator" class')  
        self.graph_gen_list.append(graph_gen)
    
    def remove_graph_gen(self, graph_gen):
        self.graph_gen_list.remove(graph_gen)
    
    def add_feature(self, feature):
        if not issubclass(type(feature),smp.SimpleGraphFeature):
            raise smp.InvalidGraphFeatureException('Invalid graph feature. Feature should extend "SimpleGraphFeature" class')
        self.feature_list.append(feature)
    
    def remove_feature(self, feature):
        self.feature_list.remove(feature)
        
    def add_sampler(self, sampler):
        if not issubclass(type(sampler), smp.Sampler):
            raise smp.InvalidSamplingMethodException('Invalid sampling method. Sampling method should extend "Sampler" class')
        self.sampler_list.append(sampler)
    
    def remove_sampler(self, sampler):
        self.sampling_method_list.remove(sampler)
        
    def add_query(self, query):
        if not issubclass(type(query), smp.Query):
            raise smp.InvalidQueryException('Invalid query. Query should extend "Query" class')
        self.query_list.append(query)
    
    def remove_query(self, query):
        self.query_list.remove(query)
    
    def set_times_to_sample(self, times_to_sample):
        self.times_to_sample=times_to_sample
        