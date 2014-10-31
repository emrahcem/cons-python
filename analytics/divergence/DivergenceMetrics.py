'''
Created on May 29, 2013

@author: ecem
'''

__all__=['Divergence','KLDivergence','LambdaDivergence','JensenShannonDivergence','KolmogorovSmirnovDistance', 'JeffreyDivergence']

import abc
import logging
import math

import sampling as smp
import analytics

class Divergence(object):
    '''
    classdocs
    '''
    __metaclass__ = abc.ABCMeta
    
    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    @abc.abstractproperty
    def name(self):
        pass
    
    @abc.abstractproperty
    def abbreviation(self):
        pass
        
    @staticmethod
    @abc.abstractmethod
    def compute(H,K):
        if len(K)==0:
            K={0:1}
        return H,K
        #pass
 
class KLDivergence(Divergence):
    
    @property
    def name(self):
        return "Kullback-Leibler Divergence"
    @property
    def abbreviation(self):
        return "KL-Divergence"
    
    @staticmethod
    def compute(H, K):
        Divergence.compute(H, K)
        try:
            if analytics.isValidPDF(H) and analytics.isValidPDF(K):
                all_keys= dict(H.items()+K.items()).keys()
                analytics.fill_gaps(H,all_keys)
                analytics.fill_gaps(K,all_keys)
                total=0
                for key in sorted(all_keys): 
                    if H[key] != 0:
                        if K[key] == 0:
                            raise ValueError('KL Divergence is  not defined for the input. Please see the definition of KL-Divergence')
                        else:
                            total+=H[key]*math.log(H[key]/K[key],2)          
                return total
            else:
                raise smp.InvalidProbabilityDensityException('Invalid probability density')
        except ValueError:
            logging.error('KL Divergence is  not defined for the input. Please see the definition of KL-Divergence')
        except smp.InvalidProbabilityDensityException:
            logging.exception('Invalid probability density')

class LambdaDivergence(Divergence):
    
    @property
    def name(self):
        return "Lambda Divergence"
    
    @property
    def abbreviation(self):
        return "L-Divergence"
    @staticmethod
    def compute(H,K,lamda):
        try:
            H,K=Divergence.compute(H, K)
            if lamda <=0 or lamda >=1 :
                raise ValueError('Invalid lambda value for LambdaDivergence. It should be in (0,1).')
            if analytics.isValidPDF(H) and analytics.isValidPDF(K):
                smoothH,_=analytics.smooth(H, K, lamda)
                return lamda* KLDivergence.compute(H, smoothH)+ (1-lamda)* KLDivergence.compute(K, smoothH)
            else:
                print K
                raise smp.InvalidProbabilityDensityException('Invalid probability density')
        except smp.InvalidProbabilityDensityException:
            logging.exception('Invalid probability density')
        except ValueError:
            logging.exception('Invalid lambda value for LambdaDivergence. It should be positive.')
            
class JensenShannonDivergence(LambdaDivergence):
    
    @property
    def name(self):
        return "Jensen-Shannon Divergence"
    
    @property
    def abbreviation(self):
        return "JS-Divergence"
    
    @staticmethod
    def compute(H,K):
        return LambdaDivergence.compute(H,K,0.5)


class JeffreyDivergence(LambdaDivergence):
    
    @property
    def name(self):
        return "Jeffrey Divergence"
    
    @property
    def abbreviation(self):
        return "JF-Divergence"
    
    @staticmethod
    def compute(H,K):
        return 2*JensenShannonDivergence.compute(H,K)


class KolmogorovSmirnovDistance(Divergence):
    
    @property
    def name(self):
        return "Kolmogorov-Smirnov Distance"
    
    @property
    def abbreviation(self):
        return "KS-Distance"
    
    @staticmethod
    def compute(H,K, cdf=False):
        H,K=Divergence.compute(H, K)
        try:
            if cdf:
                if not (analytics.isValidCDF(H) and analytics.isValidCDF(K)):
                    raise smp.InvalidProbabilityDistributionException('Invalid cumulative distribution')
            if not cdf:
                if not (analytics.isValidPDF(H) and analytics.isValidPDF(K)):
                    raise smp.InvalidProbabilityDensityException('Invalid probability density')
                #convert to cdf
                H=analytics.pdfTocdf(H)
                K=analytics.pdfTocdf(K)
            
            all_keys= dict(H.items()+K.items()).keys()
            analytics.fill_gaps(H, all_keys,cdf=True)
            analytics.fill_gaps(K, all_keys,cdf=True)
                       
            max_diff=0
            #max_key=-1

            for key in sorted(all_keys):
                
                if math.fabs(H[key]-K[key])>max_diff:
            #        max_key=key
                    max_diff=math.fabs(H[key]-K[key])
            return max_diff#, max_key, H[max_key],K[max_key]
        
        except smp.InvalidProbabilityDistributionException:
            logging.exception('Invalid probability distribution')
        except smp.InvalidProbabilityDensityException:
            logging.exception('Invalid probability density')
#===============================================================================
# if __name__ =="__main__":
#     H={3:0.1, 1:0.4, 7:0.5}
#     K={1:0.5, 2:0.4, 5:0.1}
#     H={2:0.4,3:.6}
#     H={0:0.9999,1:0.0001}
#     K={2:0.3,3:.7}
#     print JensenShannonDivergence.compute(H, K)
#===============================================================================
    