from abc import ABCMeta, abstractmethod, abstractproperty
import random
from sampling.helpers import timed
from sampling import sampling_algorithms  as smp_algo
import logging

__all__=['Sampler','NoSampler','KKPathSampler','KMPathSampler','MetropolisSubgraphSampler','MetropolizedRandomWalkSampler','RandomPathSampler','RandomVertexSampler','RandomWalkSampler','InducedRandomVertexSampler','InducedRandomEdgeSampler','RandomEdgeSampler']

logger = logging.getLogger(__name__)

class Sampler:
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def sample(self,G):
        logger.debug(self.name+' is collecting sample of size %s' %self.sample_size)
    
    @abstractproperty
    def name(self):
        pass

class NoSampler(Sampler):
    @property
    def name(self):
        return 'Original'

    @property
    def abbreviation(self):
        return 'Orig'
        
    def sample(self,G):
        return G
    
class KKPathSampler(Sampler):
    '''Wrapper class for kk_path_sampler(G, sample_size, K, stopping_condition='UNIQUE_NODES', fuzzy_select=True, seed=None)'''

    @property
    def name(self):
        return 'KK Path Sampling'

    @property
    def abbreviation(self):
        return 'KK'

    def __init__(self, sample_size, K,
                 stopping_condition='UNIQUE_NODES', fuzzy_select=True, seed=None):
        self.sample_size=sample_size
        self.K=K
        self.stopping_condition=stopping_condition
        self.fuzzy_select=fuzzy_select
        
    @timed    
    def sample(self,G):
        super(KKPathSampler, self).sample(G)
        return smp_algo.kk_path_sampler(G,sample_size=self.sample_size, K=self.K, stopping_condition=self.stopping_condition, fuzzy_select=self.fuzzy_select)
        
class KMPathSampler(Sampler):
    '''Wrapper class for km_path_sampler(G, sample_size, K, M, stopping_condition='UNIQUE_NODES', source_destination_nodes_can_overlap=False, fuzzy_select=True, seed=None)'''

    @property
    def name(self):
        return 'KM Path Sampling'

    @property
    def abbreviation(self):
        return 'KM'

    def __init__(self, sample_size, K,
                 M, stopping_condition='UNIQUE_NODES', source_destination_nodes_can_overlap=False, fuzzy_select=True, seed=None):
        self.sample_size=sample_size
        self.stopping_condition=stopping_condition
        self.K=K
        self.M=M
        self.source_destination_nodes_can_overlap=source_destination_nodes_can_overlap
        self.fuzzy_select=fuzzy_select

    @timed    
    def sample(self, G):
        super(KMPathSampler, self).sample(G)
        return smp_algo.km_path_sampler(G, sample_size=self.sample_size, K=self.K, M=self.M, stopping_condition=self.stopping_condition, source_destination_nodes_can_overlap=self.source_destination_nodes_can_overlap, fuzzy_select=self.fuzzy_select)
        
class RandomPathSampler(Sampler):
    '''Wrapper class for random_path_sampler(G, sample_size, seed=None)'''

    @property
    def name(self):
        return 'Random Path Sampling'

    @property
    def abbreviation(self):
        return 'RP'

    def __init__(self, sample_size, stopping_condition='UNIQUE_NODES', seed=None):
        self.sample_size=sample_size
        self.stopping_condition=stopping_condition
        random.seed(seed)
        
    @timed
    def sample(self, G):
        super(RandomPathSampler, self).sample(G)
        return smp_algo.random_path_sampler(G, sample_size=self.sample_size, stopping_condition=self.stopping_condition)
            
class MetropolizedRandomWalkSampler(Sampler):
    '''Wrapper class for metropolized_random_walk_sampler(G, sample_size, stopping_condition='UNIQUE_NODES', excluded_initial_steps=0, seed=None)'''

    @property
    def name(self):
        return 'Metropolized Random Walk Sampling'

    @property
    def abbreviation(self):
        return 'MRW'

    def __init__(self, sample_size, stopping_condition='UNIQUE_NODES', excluded_initial_steps=0, seed=None):
        self.sample_size=sample_size
        self.stopping_condition=stopping_condition
        self.excluded_initial_steps=excluded_initial_steps
        random.seed(seed)
    
    @timed    
    def sample(self, G):
        super(MetropolizedRandomWalkSampler, self).sample(G)
        return smp_algo.metropolized_random_walk_sampler(G, sample_size=self.sample_size, stopping_condition=self.stopping_condition, excluded_initial_steps=self.excluded_initial_steps)
        
class RandomWalkSampler(Sampler):
    '''Wrapper class for random_walk_sampler(G, sample_size, stopping_condition='UNIQUE_NODES', metropolized=False, excluded_initial_steps=0, seed=None)'''

    @property
    def name(self):
        return 'Random Walk Sampling'

    @property
    def abbreviation(self):
        return 'RW'

    def __init__(self, sample_size, stopping_condition='UNIQUE_NODES', metropolized=False, excluded_initial_steps=0, seed=None):
        self.sample_size=sample_size
        self.stopping_condition=stopping_condition
        self.metropolized=metropolized
        self.excluded_initial_steps=excluded_initial_steps
        random.seed(seed)
    
    @timed    
    def sample(self, G):
        super(RandomWalkSampler, self).sample(G)
        return smp_algo.random_walk_sampler(G, sample_size=self.sample_size, stopping_condition=self.stopping_condition, metropolized=self.metropolized, excluded_initial_steps=self.excluded_initial_steps)
    

class RandomVertexSampler(Sampler):
    '''Wrapper class for random_vertex_sampler(G, sample_size, with_replacement=True, seed=None)'''

    @property
    def name(self):
        return 'Random Vertex Sampling'

    @property
    def abbreviation(self):
        return 'RV'

    def __init__(self, sample_size, with_replacement=True, seed=None):
        self.sample_size=sample_size
        self.with_replacement=with_replacement
        random.seed(seed)

    @timed    
    def sample(self, G):
        super(RandomVertexSampler, self).sample(G)
        return smp_algo.random_vertex_sampler(G, sample_size=self.sample_size, with_replacement=self.with_replacement)

class InducedRandomVertexSampler(Sampler):
    '''Wrapper class for induced_random_vertex_sampler(G, sample_size, with_replacement=True, seed=None)'''

    @property
    def name(self):
        return 'Induced Random Vertex Sampling'

    @property
    def abbreviation(self):
        return 'IRV'

    def __init__(self, sample_size, with_replacement=True, seed=None):
        self.sample_size=sample_size
        self.with_replacement=with_replacement
        random.seed(seed)
    
    @timed    
    def sample(self, G):
        super(InducedRandomVertexSampler, self).sample(G)
        return smp_algo.induced_random_vertex_sampler(G, sample_size=self.sample_size, with_replacement=self.with_replacement)


class RandomEdgeSampler(Sampler):
    '''Wrapper class for random_edge_sampler(G, sample_size, stopping_condition='UNIQUE_NODES', with_replacement=False, seed=None)'''

    @property
    def name(self):
        return 'Random Edge Sampling'

    @property
    def abbreviation(self):
        return 'RE'

    def __init__(self, sample_size, stopping_condition='UNIQUE_NODES', with_replacement=False, seed=None):
        self.sample_size=sample_size
        self.with_replacement=with_replacement
        self.stopping_condition=stopping_condition
        random.seed(seed)
    
    @timed    
    def sample(self, G):
        super(RandomEdgeSampler, self).sample(G)
        return smp_algo.random_edge_sampler(G, sample_size=self.sample_size, stopping_condition=self.stopping_condition, with_replacement=self.with_replacement)


class InducedRandomEdgeSampler(Sampler):
    '''Wrapper class for induced_random_edge_sampler(G, sample_size, stopping_condition='UNIQUE_NODES', with_replacement=False, seed=None)'''

    @property
    def name(self):
        return 'Induced Random Edge Sampling'

    @property
    def abbreviation(self):
        return 'IRE'

    def __init__(self, sample_size, stopping_condition='UNIQUE_NODES', with_replacement=False, seed=None):
        self.sample_size=sample_size
        self.with_replacement=with_replacement
        self.stopping_condition=stopping_condition
        random.seed(seed)
    
    @timed    
    def sample(self, G):
        super(InducedRandomEdgeSampler, self).sample(G)
        return smp_algo.induced_random_edge_sampler(G, sample_size=self.sample_size, stopping_condition=self.stopping_condition, with_replacement=self.with_replacement)


class MetropolisSubgraphSampler(Sampler):
    '''Wrapper class for metropolis_subgraph_sampler(G, sample_size, divergence, feature, num_of_iter, p, T, gamma)'''

    @property
    def name(self):
        return 'Metropolis Subgraph Sampling'

    @property
    def abbreviation(self):
        return 'IRE'

    def __init__(self, sample_size, divergence, feature, num_of_iter, p, T, gamma, seed=None):
        self.divergence = divergence
        self.feature = feature
        self.num_of_iter = num_of_iter
        self.sample_size=sample_size
        self.p = p
        self.T = T
        self.gamma = gamma
        random.seed(seed)
    
    @timed    
    def sample(self, G):
        super(MetropolisSubgraphSampler, self).sample(G)
        return smp_algo.metropolis_subgraph_sampler(G, sample_node_size=self.sample_size, divergence=self.divergence, feature=self.feature, num_of_iter=self.num_of_iter, p=self.p, T=self.T, gamma=self.gamma)
