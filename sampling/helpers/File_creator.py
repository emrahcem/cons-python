'''
Created on May 28, 2013

@author: Emrah Cem{emrah.cem@utdallas.edu}
'''

from functools import wraps
import os
import networkx as nx

__all__=['create_sample_graph_files']

def create_sample_graph_files(f):
    @wraps(f)
    def wrapper(self,*args, **kwds):
        sample=f(self,*args,**kwds)
        nx.write_gml(sample, os.path.join(os.getcwd(),'sample.gml'))
        nx.write_edgelist(sample,os.path.join(os.getcwd(),'sample.edgelist'))
        nx.write_adjlist(sample, os.path.join(os.getcwd(),'sample.adjlist'))
        return sample
    return wrapper
    

