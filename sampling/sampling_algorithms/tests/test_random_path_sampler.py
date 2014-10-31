'''
Created on May 14, 2013

@author: Emrah Cem{emrah.cem@utdallas.edu}
'''
import unittest
import networkx as nx
import sampling.sampling_algorithms as smp_algo
from sampling.sampling_algorithms.tests import test_samplers

class Test_random_path_sampler(test_samplers.UnitTestForSamplers):

    def test_connected_graph(self):
        sample=smp_algo.random_path_sampler(self.G, 100)
        
        self.assertEqual(len(sample), 100)
        
        for edge in sample.edges():
            self.assertTrue(self.G.has_edge(*edge)) 
        for node in sample.nodes():
            self.assertTrue(self.G.has_node(node))
        
        #when desired sample size is larger that population size
        with self.assertRaises(ValueError):
            smp_algo.random_path_sampler(self.G, 1001)
        
        #when desired sample size is less than 1
        with self.assertRaises(ValueError):
            smp_algo.random_path_sampler(self.G, 0)
        
        #when the input graph is not nx.Graph
        with self.assertRaises(nx.NetworkXException):
            smp_algo.random_path_sampler([1,2,3,4,5], 100)
        

    def test_disconnected_graph(self):
        sample=smp_algo.random_path_sampler(self.dG2, 100)
        self.assertEqual(len(sample), 100)
        
        for edge in sample.edges():
            self.assertTrue(self.dG2.has_edge(*edge)) 
        for node in sample.nodes():
            self.assertTrue(self.dG2.has_node(node))
        
        #when desired sample size is larger that population size
        with self.assertRaises(ValueError):
            smp_algo.random_path_sampler(self.dG2, 1001)
        
        #when desired sample size is less than 1
        with self.assertRaises(ValueError):
            smp_algo.random_path_sampler(self.dG2, 0)
        
        #when the input graph is not nx.Graph
        with self.assertRaises(nx.NetworkXException):
            smp_algo.random_path_sampler([1,2,3,4,5], 100)

suite = unittest.TestLoader().loadTestsFromTestCase(Test_random_path_sampler)
unittest.TextTestRunner(verbosity=2).run(suite)