from random_walk_sampler import *

__author__ = """Emrah Cem (emrah.cem@utdallas.edu)"""
__all__=['metropolized_random_walk_sampler']

def metropolized_random_walk_sampler(G, sample_size, stopping_condition='UNIQUE_NODES', excluded_initial_steps=0):
    return random_walk_sampler(G, sample_size=sample_size, stopping_condition=stopping_condition, metropolized=True, excluded_initial_steps=excluded_initial_steps)