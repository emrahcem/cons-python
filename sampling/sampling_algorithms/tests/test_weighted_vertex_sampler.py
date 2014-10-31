'''
Created on May 14, 2013

@author: Emrah Cem{emrah.cem@utdallas.edu}
'''
import unittest
import sampling.sampling_algorithms as smp_algo
from sampling.sampling_algorithms.tests import test_samplers

class Test_weighted_vertex_sampler(test_samplers.UnitTestForSamplers):

    
    def test_inputs(self):
        
        with self.assertRaises(ValueError):
            smp_algo.weighted_vertex_sampler(self.G, 10000, None, False)
        
        with self.assertRaises(ValueError):
            smp_algo.weighted_vertex_sampler(self.G, -1, None, False)
    
    def test_no_weight_with_replacement(self):
        
        #test the number of nodes (including the frequency of visits)
        sample=smp_algo.weighted_vertex_sampler(self.G, 10, None, True)
        l=[data['times_visited'] for _, data in sample.nodes(data=True)]
        self.assertEqual(sum(l), 10)
    
    def test_no_weight_without_replacement(self):
        
        #test the number of unique nodes in the sample 
        sample=smp_algo.weighted_vertex_sampler(self.G, 10, None, False)
        self.assertEqual(len(sample), 10)

suite = unittest.TestLoader().loadTestsFromTestCase(Test_weighted_vertex_sampler)
unittest.TextTestRunner(verbosity=2).run(suite)