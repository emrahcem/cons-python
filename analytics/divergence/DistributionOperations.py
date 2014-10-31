'''
Created on Aug 21, 2013

@author: Emrah Cem{emrah.cem@utdallas.edu}
'''

from operator import itemgetter
from numpy import cumsum
from itertools import izip, tee
from sampling.classes.exceptions import InvalidProbabilityDensityException as invalid_probability_exception
import logging

__all__=['isValidPDF', 'isValidCDF', 'pdfTocdf', 'fill_gaps', 'smooth', 'trim_pdf', 'trim_cdf']

def __pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

#Given a distribution in a dictionary form {x1:y1, x2:y2, x3:y3, ...} and a list of keys {x_i1, x_i2, x_i3, ...}
#finds the appropriate value for key in the list if it does not exist in the distribution based in whether it is a CDF or PDF.
def fill_gaps(dist, all_keys, cdf=False):
    if cdf:
        last=0
        for key in sorted(all_keys):
            if not dist.has_key(key):
                #print key,'!!new=',last
                dist[key]=last
            else:
                #print 'last=',last
                last=dist[key]
    else:
        for key in all_keys:
            if not dist.has_key(key):
                dist[key]=0
            
def smooth(d1,d2,alpha):
    all_keys= dict(d1.items()+d2.items()).keys()
    fill_gaps(d1, all_keys)
    fill_gaps(d2, all_keys)
    smoothed_d1={}
    smoothed_d2={}
    for key in all_keys:
        smoothed_d1[key]=alpha*d1[key]+(1-alpha)*d2[key]
        smoothed_d2[key]=alpha*d2[key]+(1-alpha)*d1[key]
    
    return smoothed_d1,smoothed_d2

#Given a probability density function in a dictionary form {x1:y1,x2:y2,x3:y3,...}, decides whether it is a valid PDF
def isValidPDF(dist):
    return (dist is not None) and approx_equal( sum(dist.values()), 1, 1e-9) and all(value>=0 for value in dist.values())

#Given a cumulative distribution function in a dictionary form {x1:y1,x2:y2,x3:y3,...}, decides whether it is a valid CDF
def isValidCDF(H):
    return H is not None and approx_equal(H[max(sorted(H))],1, 1e-9) and all(value>=0 and value<=1+1e-9 for value in H.values()) and all(y-x>=0 for x,y in __pairwise([value for (_, value) in sorted(H.items())]))

#Converts a dictionary representing a PDF into a dictionary representing a CDF
def pdfTocdf(H):
    try:
        if isValidPDF(H):
            keys,values=zip(*sorted(H.items(), key=itemgetter(0)))
            return dict(zip(keys,cumsum(values)))
        else:
            raise invalid_probability_exception('Invalid probability density')
    
    except invalid_probability_exception:
        logging.exception('Invalid probability density')

def approx_equal(a, b, tol):
    return abs(a - b) < tol

#Given a cumulative distribution function in a dictionary form {x1:y1,x2:y2,x3:y3,...}, trims the dictionary from above.
#From both the left and right most side, trims all the entries x1:y1 until a y value which is not approximately 0  is observed.
def trim_pdf(pdf):
    
    if isValidPDF(pdf):
        for k in sorted(pdf):
            if approx_equal(pdf[k], 0, 1e-9):
                del pdf[k]
            else:
                break
            
        for k in sorted(pdf ,reverse=True):
            if approx_equal(pdf[k], 0, 1e-9):
                del pdf[k]
            else:
                break
        return True;
    else:
        return False;

#Given a cumulative distribution function in a dictionary form {x1:y1,x2:y2,x3:y3,...}, trims the dictionary from above.
#From the right most side, trims all the entries x1:y1 until a y value which is not approximately 1 is observed. 
def trim_cdf(cdf):
     
    if isValidCDF(cdf):
        #reverse_sorted_cdf=sorted(cdf ,reverse=True);
        #shifted=reverse_sorted_cdf[1:]
        #tuples=izip(reverse_sorted_cdf, shifted)
        
        for k,prev_k in __pairwise(sorted(cdf ,reverse=True)):
            #print k,k2
            if approx_equal(cdf[prev_k], 1, 1e-9):
                del cdf[k]
            else:
                break
        return True
    else:
        return False
      
if __name__ == '__main__':
    cdf={0.01:0, 0.05:0.2, 0.1:0.4, 0.4:0.42, 0.5:0.45, 5:0.8, 10:1, 6:0.9, 20:1.0, 30:1.0, 60:1.0000000009}
    print pdfTocdf(cdf)
    if(trim_cdf(cdf)):
        print cdf
    else:
        print 'Not a valid cdf.'
    