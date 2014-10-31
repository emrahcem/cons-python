'''
Created on May 14, 2013

@author: Emrah Cem{emrah.cem@utdallas.edu}
'''
import unittest
import networkx as nx
import random

class UnitTestForSamplers(unittest.TestCase):


    def setUp(self):
        self.G=nx.barabasi_albert_graph(1000, 10, 8)
        pth_graph=nx.path_graph(1000)
        edge=random.choice(pth_graph.edges())
        pth_graph.remove_edge(edge[0], edge[1])
        self.dG=pth_graph
        self.dG2=nx.barabasi_albert_graph(900, 10, 0)
        for i in xrange(900,1000):
            self.dG2.add_node(i)

    def tearDown(self):
        pass
    

