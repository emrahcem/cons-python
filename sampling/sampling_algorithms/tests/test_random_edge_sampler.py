'''
Created on May 13, 2013

@author: Emrah Cem{emrah.cem@utdallas.edu}
'''
import unittest
import networkx as nx
import sampling.sampling_algorithms as smp_algo
from sampling.sampling_algorithms.tests import test_samplers

class Test_random_edge_sampler(test_samplers.UnitTestForSamplers):

    def test_connected_graph_without_replacement(self):
        self.assertTrue(nx.is_connected(self.G))
        
        #desired number of nodes is in the sample
        sample=smp_algo.random_edge_sampler(self.G, 100, True, False)
        self.assertAlmostEqual(len(set(sample.nodes())), 100, delta=1)
        
        #sample is a subgraph of population graph
        for edge in sample.edges():
            self.assertTrue(self.G.has_edge(*edge)) 
        for node in sample.nodes():
            self.assertTrue(self.G.has_node(node))
        
        #no parallel edges
        self.assertTrue(len(sample.edges())==len(set(sample.edges())))
        
        #desired number of edges are in the sample
        self.assertEqual(smp_algo.random_edge_sampler(self.G, 100, False, False).number_of_edges(),100)
        
        #desired number of vertices in the sample is larger than population size
        with self.assertRaises(ValueError):
            smp_algo.random_edge_sampler(self.G, 1001, True, False)
        
        #when the input graph is not an nx.Graph
        with self.assertRaises(nx.NetworkXException):
            smp_algo.random_edge_sampler([1,2,3], 100, True, True)
            
        #when the sample size is not positive
        with self.assertRaises(ValueError):
            smp_algo.random_edge_sampler(self.G, -1, True, False)
    
    
    def test_disconnected_graph_without_replacement(self):
        self.assertFalse(nx.is_connected(self.dG))
        
        #all nodes incident to sampled edges are included in the sample
        sample=smp_algo.random_edge_sampler(self.dG, 100, True, False)
       
        #sample is a subgraph of population graph    
        for edge in sample.edges():
            self.assertTrue(self.dG.has_edge(*edge)) 
        for node in sample.nodes():
            self.assertTrue(self.dG.has_node(node))
            
        #test number of unique nodes , adding one edge may add two new nodes, so +(-) number of nodes will be in the sample
        self.assertAlmostEqual(len(set(smp_algo.random_edge_sampler(self.dG, 100, True, False).nodes())), 100, delta=1)
        
        #when the sample size is not positive
        with self.assertRaises(ValueError):
            smp_algo.random_edge_sampler(self.dG, -1, True, False)
            
        #when the desired sample size is larger than population size (without replacement)
        with self.assertRaises(ValueError):
            smp_algo.random_edge_sampler(self.dG, 1001, True, False)
        
        #when the desired number of edges in the sample is larger than the number of edges in population (without replacement)
        with self.assertRaises(ValueError):
            smp_algo.random_edge_sampler(self.dG, 1000, False, False)
            
        #when the input graph is not an nx.Graph
        with self.assertRaises(nx.NetworkXException):
            smp_algo.random_edge_sampler([1,2,3], 100, True, False)
        
suite = unittest.TestLoader().loadTestsFromTestCase(Test_random_edge_sampler)
unittest.TextTestRunner(verbosity=2).run(suite)
