'''
Created on May 19, 2013

@author: Emrah Cem(emrah.cem@utdallas.edu)
'''

from functools import wraps
from time import time
from inspect import getcallargs
from sys import stdout

import datetime
import logging
import os

log = logging.getLogger(__name__)

__all__=['create_logger','log_graph_generation','log_sampler','log_sample_no','timed']

def create_logger():
    logger=logging.getLogger()
    
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(module)-20s - %(levelname)-6s - %(message)s')
    if len(logger.handlers):
        logger.handlers.remove(logger.handlers[1])
    else:
        #create streamhandler just once
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        #ch.setLevel(logging.WARNING)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    
    ##comment out if you dont want log file
    fh = logging.FileHandler(os.path.join(os.getcwd(),'log.txt'))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

def log_graph_generation(f):
    from functools import wraps
    @wraps(f)
    def wrapper(self, *args, **kwds):
        try:
            log.info('-'*30+self.name+'-'*30)
            log.info('Generating graph')
            result = f(self, *args, **kwds)
            return result
        except Exception as exc:
            log.info('Ignoring this graph.')
            log.info('See log file for details')
            log.debug(exc)
    return wrapper

def log_sampler(f):
    @wraps(f)
    def wrapper(self, *args, **kwds):
        arg=getcallargs(f,self , *args, **kwds)
        log.info(arg['sampler'].name)
        result = f(self, *args, **kwds)
        return result
    return wrapper

def log_sample_no(f):
    @wraps(f)
    def wrapper(self, *args, **kwds):
        arg=getcallargs(f,self , *args, **kwds)
        log.info(''.join(['sample ', str(arg['exp_no'])])) 
        stdout.flush()
        result = f(self, *args, **kwds)
        return result
    return wrapper

def timed(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        start = time()
        result = f(*args, **kwds)
        elapsed = time() - start
        log.debug("(completed in {0:s} sec)".format(str(datetime.timedelta(seconds=elapsed))))
        return result
    return wrapper