'''
Created on Jul 4, 2013

@author: ecem
'''
import unittest
import networkx as nx
import sampling.sampling_algorithms as smp_algo
from sampling.sampling_algorithms.tests import test_samplers

class Test_induced_random_edge_sampler(test_samplers.UnitTestForSamplers):


    def test_connected_graph_without_replacement(self):
        self.assertTrue(nx.is_connected(self.G))
        
        #desired number of nodes is in the sample
        sample=smp_algo.random_edge_sampler(self.G, 100, stopping_condition='UNIQUE_NODES', with_replacement=True,  include_last_edge_when_exceeds=False)
        self.assertEqual(len(set(sample.nodes())), 100)
        
        #sample is a subgraph of population graph
        for edge in sample.edges():
            self.assertTrue(self.G.has_edge(*edge)) 
        for node in sample.nodes():
            self.assertTrue(self.G.has_node(node))
        
        #no parallel edges
        self.assertTrue(len(sample.edges())==len(set(sample.edges())))
                
        #when the input graph is not an nx.Graph
        with self.assertRaises(nx.NetworkXException):
            smp_algo.random_edge_sampler([1,2,3], 100, True, True)
            
        #when the sample size is not positive
        with self.assertRaises(ValueError):
            smp_algo.random_edge_sampler(self.G, -1, True, False)




        sample=smp_algo.random_edge_sampler(self.G, 100, stopping_condition='UNIQUE_EDGES', with_replacement=True,  include_last_edge_when_exceeds=False)
        self.assertEqual(len(set(sample.edges())), 100)

        #sample is a subgraph of population graph
        for edge in sample.edges():
            self.assertTrue(self.G.has_edge(*edge)) 
        for node in sample.nodes():
            self.assertTrue(self.G.has_node(node))
        
        #no parallel edges
        self.assertTrue(len(sample.edges())==len(set(sample.edges())))
                
        #when the input graph is not an nx.Graph
        with self.assertRaises(nx.NetworkXException):
            smp_algo.random_edge_sampler([1,2,3], 100, True, True)
            
        #when the sample size is not positive
        with self.assertRaises(ValueError):
            smp_algo.random_edge_sampler(self.G, -1, True, False)
            
suite = unittest.TestLoader().loadTestsFromTestCase(Test_induced_random_edge_sampler)
unittest.TextTestRunner(verbosity=2).run(suite)