'''
Created on May 17, 2013

@author: Emrah Cem{emrah.cem@utdallas.edu}
'''

class InvalidGraphFeatureException(Exception):    
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class InvalidSamplingMethodException(Exception):    
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class InvalidQueryException(Exception):    
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class InvalidGraphGeneratorException(Exception):    
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class InvalidProbabilityDistributionException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class InvalidProbabilityDensityException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)