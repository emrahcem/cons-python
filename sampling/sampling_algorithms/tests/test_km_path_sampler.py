'''
Created on May 14, 2013

@author: Emrah Cem{emrah.cem@utdallas.edu}
'''
import unittest
import networkx as nx
import sampling.sampling_algorithms as smp_algo
from sampling.sampling_algorithms.tests import test_samplers

class Test_km_path_sampler(test_samplers.UnitTestForSamplers):
    
    def test_inputs(self):
        
        #input graph is nx.Graph
        with self.assertRaises(nx.NetworkXException):
            smp_algo.km_path_sampler([1,2,3],100, 30, 70, True)
     
        #K is larger than the population size
        with self.assertRaises(ValueError):
            smp_algo.km_path_sampler(self.G,100, 100000, 70, True)
        
        #K is smaller than 1
        with self.assertRaises(ValueError):
            smp_algo.km_path_sampler(self.G,100, 0, 70, True)
        
        #M is larger than the population size
        with self.assertRaises(ValueError):
            smp_algo.km_path_sampler(self.G,100, 30, 10000, True)
        
        #M is smaller than 1
        with self.assertRaises(ValueError):
            smp_algo.km_path_sampler(self.G,100, 30, 0, True)
                   
        #desired sample node size is larger than population size 
        with self.assertRaises(ValueError):
            smp_algo.km_path_sampler(self.G,100000, 30, 70, False, False)
            
        #desired sample node size is less than 1
        with self.assertRaises(ValueError):
            smp_algo.km_path_sampler(self.G, 0, 30, 70, False, False)
    
    def test_connected_graph_stop_at_sample_node_size_fuzzy_select(self):
        
        sample=smp_algo.km_path_sampler(self.G,100, 30,70, True)
        
        self.assertTrue(sample.number_of_nodes()==100)
        
        #sample is a subgraph of population graph
        for edge in sample.edges():
            self.assertTrue(self.G.has_edge(*edge)) 
        for node in sample.nodes():
            self.assertTrue(self.G.has_node(node))
        
        #no parallel edges
        self.assertTrue(len(sample.edges())==len(set(sample.edges())))
        
            
    def test_connected_graph_stop_at_sample_node_size_not_fuzzy_select(self):
        
        sample=smp_algo.km_path_sampler(self.G,100, 30, 50, True, False)
        
        self.assertTrue(sample.number_of_nodes()==100)
        
        #sample is a subgraph of population graph
        for edge in sample.edges():
            self.assertTrue(self.G.has_edge(*edge)) 
        for node in sample.nodes():
            self.assertTrue(self.G.has_node(node))
        
        #no parallel edges
        self.assertTrue(len(sample.edges())==len(set(sample.edges())))
    
    
    def test_connected_graph_dont_stop_at_sample_node_size_fuzzy_select(self):
        sample=smp_algo.km_path_sampler(self.G,100, 30, 70, False)
        
        #sample is a subgraph of population graph
        for edge in sample.edges():
            self.assertTrue(self.G.has_edge(*edge)) 
        for node in sample.nodes():
            self.assertTrue(self.G.has_node(node))
        
        sample=smp_algo.km_path_sampler(self.G, 1000, 500, 500, False)
        
        self.assertTrue(self.G.nodes()==sample.nodes())
           
        #no parallel edges
        self.assertTrue(len(sample.edges())==len(set(sample.edges())))
        
            
    def test_connected_graph_dont_stop_at_sample_node_size_not_fuzzy_select(self):
        sample=smp_algo.km_path_sampler(self.G,100, 30, 70, False, False)
        
        #sample is a subgraph of population graph
        for edge in sample.edges():
            self.assertTrue(self.G.has_edge(*edge)) 
        for node in sample.nodes():
            self.assertTrue(self.G.has_node(node))
        
        sample=smp_algo.km_path_sampler(self.G, 1000, 500, 500, False, False)
        
        self.assertTrue(self.G.nodes()==sample.nodes())
           
        #no parallel edges
        self.assertTrue(len(sample.edges())==len(set(sample.edges())))
    
    
    def test_disconnected_graph_stop_at_sample_node_size_fuzzy_select(self):
        
        sample=smp_algo.km_path_sampler(self.dG2,100, 30,70, True)
        
        self.assertTrue(sample.number_of_nodes()==100)
        
        #sample is a subgraph of population graph
        for edge in sample.edges():
            self.assertTrue(self.G.has_edge(*edge)) 
        for node in sample.nodes():
            self.assertTrue(self.G.has_node(node))
        
        #no parallel edges
        self.assertTrue(len(sample.edges())==len(set(sample.edges())))
        
            
    def test_disconnected_graph_stop_at_sample_node_size_not_fuzzy_select(self):
        
        sample=smp_algo.km_path_sampler(self.dG2,100, 30, 50, True, False)
        
        self.assertTrue(sample.number_of_nodes()==100)
        
        #sample is a subgraph of population graph
        for edge in sample.edges():
            self.assertTrue(self.G.has_edge(*edge)) 
        for node in sample.nodes():
            self.assertTrue(self.G.has_node(node))
        
        #no parallel edges
        self.assertTrue(len(sample.edges())==len(set(sample.edges())))
    
    
    def test_disconnected_graph_dont_stop_at_sample_node_size_fuzzy_select(self):
        sample=smp_algo.km_path_sampler(self.dG2,100, 30, 70, False)
        
        #sample is a subgraph of population graph
        for edge in sample.edges():
            self.assertTrue(self.G.has_edge(*edge)) 
        for node in sample.nodes():
            self.assertTrue(self.G.has_node(node))
           
        #no parallel edges
        self.assertTrue(len(sample.edges())==len(set(sample.edges())))
        
            
    def test_disconnected_graph_dont_stop_at_sample_node_size_not_fuzzy_select(self):
        sample=smp_algo.km_path_sampler(self.dG2,100, 30, 70, False, False)
        
        #sample is a subgraph of population graph
        for edge in sample.edges():
            self.assertTrue(self.G.has_edge(*edge)) 
        for node in sample.nodes():
            self.assertTrue(self.G.has_node(node))
           
        #no parallel edges
        self.assertTrue(len(sample.edges())==len(set(sample.edges())))

suite = unittest.TestLoader().loadTestsFromTestCase(Test_km_path_sampler)
unittest.TextTestRunner(verbosity=2).run(suite)

# if __name__ == "__main__":
#     #import sys;sys.argv = ['', 'Test.testName']
#     unittest.main()