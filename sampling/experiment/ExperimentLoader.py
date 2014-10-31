'''
Created on Jun 22, 2013

@author: ecem
'''

from abc import ABCMeta, abstractmethod#, abstractproperty
import logging

from sampling.experiment.SamplingJob import SamplingJob
from sampling.experiment import ReadDefaults

_all__=['XMLLoader']

class ExperimentLoader(object):
    '''
    classdocs
    '''
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def load_experiment(self, exp):
        pass

class XMLLoader(ExperimentLoader):
    
    def __init__(self, xml_file_handler):
        self.xml_file_handler=xml_file_handler
        
    def load_experiment(self, exp):
        ExperimentLoader.load_experiment(self, exp)
        exp.set_input_file(self.xml_file_handler)
        try:
            seed, list_of_job_inputs=ReadDefaults.read_xml(self.xml_file_handler)
            exp.set_seed(seed)
            for inputs, job_params in list_of_job_inputs:
                job_inst=SamplingJob(**job_params)
                for g in inputs['Graph']:
                    gen=getattr(__import__("sampling"), g[0])(**g[1])
                    #gen.name=g[2]
                    job_inst.add_graph_gen(gen)
                for s in inputs['Sampler']:
                    job_inst.add_sampler(getattr(__import__("sampling"), s[0])(**s[1]))
                for f in inputs['Feature']:
                    job_inst.add_feature(getattr(__import__("sampling"), f)())
                for q in inputs['Query']:
                    job_inst.add_query(getattr(__import__("sampling"), q)())
                exp.add_sampling_job(job_inst)
        except AttributeError as e:
            print e
            logging.exception('Exception')
        except TypeError:
            logging.exception('Exception')
        
        