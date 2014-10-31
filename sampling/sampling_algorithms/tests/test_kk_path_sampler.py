'''
Created on May 13, 2013

@author: Emrah Cem{emrah.cem@utdallas.edu}
'''
import unittest
import sampling.sampling_algorithms as smp_algo
from sampling.sampling_algorithms.tests import test_samplers

class Test_kk_path_sampler(test_samplers.UnitTestForSamplers):

    def test_connected_graph_stop_at_sample_node_size_fuzzy_select(self):
        sample=smp_algo.kk_path_sampler(self.G,100, 30, True)
        
        self.assertTrue(sample.number_of_nodes()==100)
        
        #sample is a subgraph of population graph
        for edge in sample.edges():
            self.assertTrue(self.G.has_edge(*edge)) 
        for node in sample.nodes():
            self.assertTrue(self.G.has_node(node))
            
        #no parallel edges
        self.assertTrue(len(sample.edges())==len(set(sample.edges())))
        
        #desired sample node size is larger than population size 
        with self.assertRaises(ValueError):
            smp_algo.kk_path_sampler(self.G,100000, 100, True)
            
        #desired sample node size is less than 1
        with self.assertRaises(ValueError):
            smp_algo.kk_path_sampler(self.G,-1, 100, True)
        
        #K is larger than the population size
        with self.assertRaises(ValueError):
            smp_algo.kk_path_sampler(self.G,100, 100000, True)
        
        #K is smaller than 2
        with self.assertRaises(ValueError):
            smp_algo.kk_path_sampler(self.G,100, 1, True)
               
    def test_connected_graph_stop_at_sample_node_size_not_fuzzy_select(self):
        sample=smp_algo.kk_path_sampler(self.G,100, 30, True, False)
        
        self.assertTrue(sample.number_of_nodes()==100)
        
        #sample is a subgraph of population graph
        for edge in sample.edges():
            self.assertTrue(self.G.has_edge(*edge)) 
        for node in sample.nodes():
            self.assertTrue(self.G.has_node(node))
            
        #no parallel edges
        self.assertTrue(len(sample.edges())==len(set(sample.edges())))
        
        #desired sample node size is larger than population size 
        with self.assertRaises(ValueError):
            smp_algo.kk_path_sampler(self.G,100000, 100, True, False)
            
        #desired sample node size is less than 1
        with self.assertRaises(ValueError):
            smp_algo.kk_path_sampler(self.G,-1, 100, True, False)
        
        #K is larger than the population size
        with self.assertRaises(ValueError):
            smp_algo.kk_path_sampler(self.G,100, 100000, True, False)
        
        #K is smaller than 2
        with self.assertRaises(ValueError):
            smp_algo.kk_path_sampler(self.G,100, 1, True, False)
    
    
    def test_connected_graph_dont_stop_at_sample_node_size_fuzzy_select(self):
        sample=smp_algo.kk_path_sampler(self.G,100, 30, False)
        
        #sample is a subgraph of population graph
        for edge in sample.edges():
            self.assertTrue(self.G.has_edge(*edge)) 
        for node in sample.nodes():
            self.assertTrue(self.G.has_node(node))
        
        sample=smp_algo.kk_path_sampler(self.G, 1000, 1000, False)
        self.assertTrue(self.G.nodes()==sample.nodes())
           
        #no parallel edges
        self.assertTrue(len(sample.edges())==len(set(sample.edges())))
        
        #desired sample node size is larger than population size 
        with self.assertRaises(ValueError):
            smp_algo.kk_path_sampler(self.G,100000, 100, False)
            
        #desired sample node size is less than 1
        with self.assertRaises(ValueError):
            smp_algo.kk_path_sampler(self.G,-1, 100, False)
            
        #K is larger than the population size
        with self.assertRaises(ValueError):
            smp_algo.kk_path_sampler(self.G,100, 100000, False)
        
        #K is smaller than 2
        with self.assertRaises(ValueError):
            smp_algo.kk_path_sampler(self.G,100, 1, False)
            
    def test_connected_graph_dont_stop_at_sample_node_size_not_fuzzy_select(self):
        sample=smp_algo.kk_path_sampler(self.G,100, 30, False, False)
        
        #sample is a subgraph of population graph
        for edge in sample.edges():
            self.assertTrue(self.G.has_edge(*edge)) 
        for node in sample.nodes():
            self.assertTrue(self.G.has_node(node))
        
        sample=smp_algo.kk_path_sampler(self.G, 1000, 1000, False, False)
        self.assertTrue(self.G.nodes()==sample.nodes())
           
        #no parallel edges
        self.assertTrue(len(sample.edges())==len(set(sample.edges())))
        
        #desired sample node size is larger than population size 
        with self.assertRaises(ValueError):
            smp_algo.kk_path_sampler(self.G,100000, 100, False, False)
            
        #desired sample node size is less than 1
        with self.assertRaises(ValueError):
            smp_algo.kk_path_sampler(self.G,-1, 100, False, False)
            
        #K is larger than the population size
        with self.assertRaises(ValueError):
            smp_algo.kk_path_sampler(self.G,100, 100000, False, False)
        
        #K is smaller than 2
        with self.assertRaises(ValueError):
            smp_algo.kk_path_sampler(self.G,100, 1, False, False)

suite = unittest.TestLoader().loadTestsFromTestCase(Test_kk_path_sampler)
unittest.TextTestRunner(verbosity=2).run(suite)