'''
Created on May 14, 2013

@author: Emrah Cem{emrah.cem@utdallas.edu}
'''
import unittest
import networkx as nx
import sampling.sampling_algorithms as smp_algo
from sampling.sampling_algorithms.tests import test_samplers

class Test_random_walk_sampler(test_samplers.UnitTestForSamplers):

    def test_connected_graph(self):
        sample= smp_algo.random_walk_sampler(self.G, 100, False, False, 0)
        
        self.assertTrue(len(sample)==100)
        
        self.assertTrue(nx.is_connected(sample))
        
        with self.assertRaises(ValueError):
            smp_algo.random_walk_sampler(self.G, 0, False, False, 0)
    
    def test_excluded_initial_steps_dont_count_by_step_size_not_metropolized(self):
        
        #samples desired number of nodes
        sample=smp_algo.random_walk_sampler(self.G, 100, False, False, 10)
        self.assertTrue(len(sample) == 100)
        
    def test_excluded_initial_steps_dont_count_by_step_size_metropolized(self):
        sample=smp_algo.random_walk_sampler(self.G, 100, False, True, 10)
        self.assertTrue(len(sample) == 100)
              
    def test_excluded_initial_steps_count_by_step_size_not_metropolized(self):
        
        #samples desired number of nodes
        sample=smp_algo.random_walk_sampler(self.G, 100, True, False, 10)
        self.assertTrue(len(sample) <= 100) 
        
        sample=smp_algo.random_walk_sampler(self.G, 100, True, False, 20)

        l=[data['times_visited'] for _ , data in sample.nodes(data=True)]
        self.assertEqual(sum(l)-1,100)
        
        l=[data['times_visited'] for _,_, data in sample.edges(data=True)]
        l2=[data['times_self_loop'] for _, data in sample.nodes(data=True) if 'times_self_loop' in data]
        self.assertEqual(sum(l2)+sum(l),100)    
        
    def test_excluded_initial_steps_count_by_step_size_metropolized(self):
        
        #samples desired number of nodes
        sample=smp_algo.random_walk_sampler(self.G, 100, True, True, 10)
        self.assertTrue(len(sample) <= 100) 
        
        sample=smp_algo.random_walk_sampler(self.G, 100, True, True, 20)

        l=[data['times_visited'] for _, data in sample.nodes(data=True)]
        self.assertEqual(sum(l)-1,100)
        
        l=[data['times_visited'] for _,_, data in sample.edges(data=True)]
        l2=[data['times_self_loop'] for _, data in sample.nodes(data=True) if 'times_self_loop' in data]
        self.assertEqual(sum(l2)+sum(l),100)    
               
    def test_disconnected_graph(self):
        pass
    
suite = unittest.TestLoader().loadTestsFromTestCase(Test_random_walk_sampler)
unittest.TextTestRunner(verbosity=2).run(suite)