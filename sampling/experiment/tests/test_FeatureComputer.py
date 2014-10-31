'''
Created on May 28, 2013

@author: exc103320
'''
import unittest
import networkx as nx
import random

import sampling as smp
#from sampling.classes.query_types import FrontendQuery, BackendQuery
#from sampling.classes.graph_features import SimpleGraphDegree
#from sampling.experiment.FeatureComputer import *
class Test_FeatureComputer(unittest.TestCase):


    def setUp(self):
        self.G=nx.barabasi_albert_graph(100, 10)
        self.S=nx.subgraph(self.G, random.sample(self.G.nodes(),30) )
    def tearDown(self):
        pass
    
    def test_compute_single_query(self):
        fq=smp.FrontendQuery(self.G)
        self.assertTrue(len(smp.FeatureComputer.compute_single_query(fq, smp.SimpleGraphDegree()))>0)
        
        fq_none=smp.FrontendQuery(None)
        self.assertEqual(smp.FeatureComputer.compute_single_query(fq_none, smp.SimpleGraphDegree()),None)
        
        bq=smp.BackendQuery(self.G,self.S)
        self.assertTrue(len(smp.FeatureComputer.compute_single_query(bq, smp.SimpleGraphDegree()))>0)
        
        bq_none=smp.BackendQuery(None, self.S)
        self.assertEqual(smp.FeatureComputer.compute_single_query(bq_none, smp.SimpleGraphDegree()),None)
        
        bq_none=smp.BackendQuery(self.G, None)
        self.assertEqual(smp.FeatureComputer.compute_single_query(bq_none, smp.SimpleGraphDegree()),None)
        
    def test_compute_all_queries(self):
        self.assertEqual(1,2)

    def test_compute_all_backend_queries(self):
        self.assertEqual(1,2)
    
    def test_compute_all_frontend_queries(self):
        self.assertEqual(1,2)
    
suite = unittest.TestLoader().loadTestsFromTestCase(Test_FeatureComputer)
unittest.TextTestRunner(verbosity=2).run(suite)