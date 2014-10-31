from weighted_vertex_sampler import *

__author__ = """Emrah Cem (emrah.cem@utdallas.edu)"""
__all__=['random_vertex_sampler']

def random_vertex_sampler(G, sample_size, with_replacement=True):
    return weighted_vertex_sampler(G, sample_size=sample_size, weights=None, with_replacement=with_replacement)