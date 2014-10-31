'''
Created on May 13, 2013

@author: Emrah Cem{emrah.cem@utdallas.edu}
'''
import unittest
import networkx as nx
from sampling.sampling_algorithms.induced_random_vertex_sampler import induced_random_vertex_sampler  
from sampling.sampling_algorithms.tests import test_samplers

class Test_induced_random_vertex_sampler(test_samplers.UnitTestForSamplers):

    def test_connected_graph_without_replacement(self):
        self.assertTrue(nx.is_connected(self.G))
        
        #stops at the desired number of unique nodes        
        sample=induced_random_vertex_sampler(self.G, 100, False)
        self.assertEqual(len(set(sample.nodes())), 100)
    
        #sample is a subgraph of population graph
        for edge in sample.edges():
            self.assertTrue(self.G.has_edge(*edge)) 
        for node in sample.nodes():
            self.assertTrue(self.G.has_node(node))
        
        #no parallel edges
        self.assertTrue(len(sample.edges())==len(set(sample.edges())))
        
        #negative sample size
        with self.assertRaises(ValueError):
            induced_random_vertex_sampler(self.G, -1, True)

      
        #desired number of edges is larger than that of population
        with self.assertRaises(ValueError):
            induced_random_vertex_sampler(self.G, 100000, False)
         
        #raises exception when the input graph is not nx.Graph
        with self.assertRaises(nx.NetworkXException):
            induced_random_vertex_sampler([1,2,3], 100, True)
            

    def test_disconnected_graph_without_replacement(self):
        self.assertFalse(nx.is_connected(self.dG))
        self.assertFalse(nx.is_connected(self.dG2))
        
        #stops at the desired number of unique nodes
        sample=induced_random_vertex_sampler(self.dG, 100, False)
        self.assertEqual(len(set(sample.nodes())), 100)
        
        for edge in sample.edges():
            self.assertTrue(self.dG.has_edge(*edge)) 
        for node in sample.nodes():
            self.assertTrue(self.dG.has_node(node))
        
        sample=induced_random_vertex_sampler(self.dG2, 100, False)
        self.assertEqual(len(set(sample.nodes())), 100)
        
        self.assertTrue(nx.subgraph(sample, self.G))
                
        #negative sample size
        with self.assertRaises(ValueError):
            induced_random_vertex_sampler(self.dG, -1, True)
        
        with self.assertRaises(ValueError):
            induced_random_vertex_sampler(self.dG2, -1, True)

        #desired number of edges is larger than that of population
        with self.assertRaises(ValueError):
            induced_random_vertex_sampler(self.dG, 100000, False)

        with self.assertRaises(ValueError):
            induced_random_vertex_sampler(self.dG2, 100000, False)

        #raises exception when the input graph is not nx.Graph
        with self.assertRaises(nx.NetworkXException):
            induced_random_vertex_sampler([1,2,3], 100, True)
            
suite = unittest.TestLoader().loadTestsFromTestCase(Test_induced_random_vertex_sampler)
unittest.TextTestRunner(verbosity=2).run(suite)
