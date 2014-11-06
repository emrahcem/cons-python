'''
Created on Aug 4, 2013

@author: Emrah Cem{emrah.cem@utdallas.edu}
'''

import random
import pickle    
import networkx as nx
import os 
import analytics

from sampling.helpers import Folder_creator, Logger 
from sampling.experiment import FeatureComputer
from sampling.classes.query_types import FrontendQuery

import logging
#from analytics.analyzers.Analyzer import GraphDistributionPlotAnalysis

logger = logging.getLogger(__name__)

__all__=['computePopulationDistributions','execute_all_graphs','execute_single_graph','execute_single_sample','execute_single_sampler_for_a_graph']

def __fill_graph_dic_for_population(H, feature_list, query_list, times_to_sample):
    graph_dic = {}
    for exp in range(0, int(times_to_sample)):
        feature_dic = {}
        for feature in feature_list:
            query_dic = {}
            for query in query_list:
                query_dic[query.name] = H[feature.name]
             
            feature_dic[feature.name] = query_dic        
        graph_dic[exp] = feature_dic
    return graph_dic

def computePopulationDistributions(G, feature_list):
    H = FeatureComputer.compute_queries(FrontendQuery(G), feature_list)
    if len(H) !=0:
        return H

def __sample(G, sampler):
    return sampler.sample(G)

def __execute_single_sample(G, sampler, feature_list, query_list, exp_no):
    try:
        sample_graph = __sample(G, sampler)
        sample_dic= FeatureComputer.compute_all_features(G, sample_graph, feature_list, query_list)
    except Exception as e:
        logger.exception(e)
    else:
        return sample_dic

def __execute_all_samples_for_a_sampler(G, sampler, feature_list, query_list, times_to_sample=1):
    try:
        sampler_dic={}
        for exp_no in range(0, int(times_to_sample)):
            logger.info('sample %s, (size= %s)' % (exp_no,sampler.sample_size) )
            result_for_single_sample = __execute_single_sample(G, sampler, feature_list, query_list, exp_no)
            if result_for_single_sample is not None:
                sampler_dic[exp_no] = result_for_single_sample
    except Exception as e:
        logger.exception(e)
    else:
        if len(sampler_dic) > 0:
            return sampler_dic
        
def execute_single_sampler_for_a_graph(G, sampler, feature_list, query_list, times_to_sample=1, seed_val=1, create_logger=False):
    go_back=False
    sampler_dic=None
    try:
        if Folder_creator.create_folder(sampler.name):
            go_back=True
            if create_logger:
                Logger.create_logger()
        
            #compute results for a single sampler
            #===================================================================
            random.seed(seed_val)
            sampler_dic = __execute_all_samples_for_a_sampler(G, sampler, feature_list, query_list, times_to_sample)
            pickle.dump(sampler_dic, open('dist.pickle','w'))
            
            analyzer = analytics.AnalysisGroup()
            
            analyzer.add_analysis(analytics.SamplerPdfCdfPlotAnalysis(sampler_dic, title= 'Characteristic Distribution and Descriptive Statistics in the sample graph \n( sampled by '+sampler.name+' )', file_name=os.path.join(os.getcwd(),'CDF_PDF_plot.pdf')))
            analyzer.add_analysis(analytics.SamplerDistributionPlotAnalysis(sampler_dic, pop_dic=G.graph.get('distribution'), title=  'Characteristic Distributions in the sample graph \n( sampled by '+sampler.name+' )' , file_name=os.path.join(os.getcwd(),'CDF_plot.pdf')))
            
            if G.graph.has_key('distribution'):
                analyzer.add_analysis(analytics.SamplerBoxplotAnalysis(sampler_dic, pop_dic=G.graph['distribution'], divergence=analytics.DivergenceMetrics.JensenShannonDivergence, title=sampler.name + '\n'+analytics.DivergenceMetrics.JensenShannonDivergence().abbreviation,  file_name=os.path.join(os.getcwd(),'boxplot_'+analytics.DivergenceMetrics.JensenShannonDivergence().abbreviation+'.pdf')))
                analyzer.add_analysis(analytics.SamplerBoxplotAnalysis(sampler_dic, pop_dic=G.graph['distribution'], divergence=analytics.DivergenceMetrics.KolmogorovSmirnovDistance, title=sampler.name + '\n'+analytics.DivergenceMetrics.KolmogorovSmirnovDistance().abbreviation, file_name=os.path.join(os.getcwd(),'boxplot_'+analytics.DivergenceMetrics.KolmogorovSmirnovDistance().abbreviation+'.pdf'), show=True))
                analyzer.add_analysis(analytics.SamplerDescriptiveAnalysis(sampler_dic, pop_dic=G.graph['distribution'], divergence=analytics.DivergenceMetrics.JensenShannonDivergence, file_name=os.path.join(os.getcwd(),'summary_'+analytics.DivergenceMetrics.JensenShannonDivergence().abbreviation+'.txt')))
                analyzer.add_analysis(analytics.SamplerDescriptiveAnalysis(sampler_dic, pop_dic=G.graph['distribution'], divergence=analytics.DivergenceMetrics.KolmogorovSmirnovDistance, file_name=os.path.join(os.getcwd(),'summary_'+analytics.DivergenceMetrics.KolmogorovSmirnovDistance().abbreviation+'.txt')))
            
            analyzer.analyze()
            
    except Exception as e:
        logger.exception(e)
    else:
        if sampler_dic is not None:
            return sampler_dic
    finally:
        if go_back:
            os.chdir('..')
    
def execute_all_samplers_for_a_graph(G, sampler_list, feature_list, query_list, times_to_sample=1, seed_val=1, create_logger=False):
    go_back=False
    samplers_dic={}
    try:
        if Folder_creator.create_folder('samplers'):
            go_back=True
            if create_logger:
                Logger.create_logger()
            
            samplers_dic={}
            for sampler in sampler_list:
                logger.info(sampler.name)
                dic_for_single_sampler= execute_single_sampler_for_a_graph(G, sampler, feature_list, query_list, times_to_sample, seed_val)
                if dic_for_single_sampler is not None:# and original_dic != None:
                    samplers_dic[sampler.name] = dic_for_single_sampler
            
    except Exception as e:
        logger.exception(e)
    else:
        if len(samplers_dic)>0:        
            return samplers_dic
    finally:
        if go_back:
            os.chdir('..')

def execute_population_features(G, feature_list, create_logger=False, folder_name='population'):
    go_back=False
    try:
        if Folder_creator.create_folder(folder_name):
            go_back=True
            if create_logger:
                Logger.create_logger()
                
            #writes the graph into the file in .gml format
            nx.write_gml(G, os.path.join(os.getcwd(),'nx_graph.gml'))
            
            #loads the population distribution from the file if graph has 'distribution_file_name' attribute
            #this attribute can be provided in the input xml file as the path to the distribution file
            #this is for better performance, dont compute population distibutions if it had already been computed and saved(dumped) in a file 
            if G.graph['distribution_file_name'] is not None:
                try:
                    pop_dist=pickle.load(open(G.graph['distribution_file_name'],'r'))
                    logger.info('Succesfully loaded population characteristics from '+G.graph['distribution_file_name'] )
                except Exception as e:
                    logger.exception('Could not load population characteristics from the file. Computing...')
                    pop_dist=computePopulationDistributions(G, feature_list)
            else:
                pop_dist=computePopulationDistributions(G, feature_list)
            
            pickle.dump(pop_dist, open('dist.pickle','w'))
                    
            analysis=analytics.PopulationFeaturesPlotAnalysis(data=pop_dist, title='Characteristic Distribution and Descriptive Statistics in \n '+G.graph['name'], file_name=os.path.join(os.getcwd(), G.graph['abbreviation']+'_descriptive_statistics.pdf'))
            analysis.analyze()
            
    except Exception as e:
        logger.exception(e)
    else:
        if pop_dist is not None:
            G.graph['distribution']=pop_dist
            return pop_dist
    finally:
        if go_back:
            os.chdir('..')
            
def execute_single_graph(G, sampler_list, feature_list, query_list, times_to_sample=1, seed_val=1, create_logger=False, compute_population_distributions=True):
    go_back=False
    try:
        if Folder_creator.create_folder(G.graph['folder_name']):
            go_back=True
            if create_logger:
                Logger.create_logger()
            
            if compute_population_distributions:
                pop_dist=execute_population_features(G, feature_list)
            
            graph_dic = execute_all_samplers_for_a_graph(G, sampler_list, feature_list, query_list, times_to_sample, seed_val)
            if compute_population_distributions:
                graph_dic['Original']=__fill_graph_dic_for_population(pop_dist, feature_list, query_list, times_to_sample)
                    
            analysis=analytics.GraphDistributionPlotAnalysis(data=graph_dic, divergence=analytics.DivergenceMetrics.JensenShannonDivergence, \
                                          title=G.graph['name'], file_name= os.path.join(os.getcwd(),G.graph['abbreviation']+'_distribution.pdf'))
            analysis.analyze()
            
    except Exception as e:
        logger.exception(e)
    else:
        if graph_dic is not None:
            pickle.dump(graph_dic,open(os.path.join(os.getcwd(),'graph_dic.pickle'),'w'))
            return graph_dic
    finally:
        if go_back:
            os.chdir('..')

def execute_all_graphs(job, seed_val=1, compute_population_distributions=True):    
    try:
        #compute results for job
        job_dic={}
        graph_attr={}
        for graph_gen in job.graph_gen_list:
            G = graph_gen.generate()
            if not G == None:
                result=execute_single_graph(G, job.sampler_list, job.feature_list, job.query_list, job.times_to_sample, seed_val, compute_population_distributions=compute_population_distributions)
                if result != None:
                    job_dic[graph_gen.name]=result
                    graph_attr[graph_gen.name]=G.graph
    except Exception as e:
        logger.exception(e)
    else:
        if len(job_dic) >0:    
            return job_dic,graph_attr 

#if __name__ == '__main__':    
    #G=nx.barabasi_albert_graph(1000,10,1)
    #result=smp.SamplingJobExecuter.execute_population_features(G, [smp.SimpleGraphDegree(),smp.SimpleGraphPathLength()] , create_logger=True)
    #result=smp.SamplingJobExecuter.execute_all_samplers_for_a_graph(G,[smp.KKPathSampler(100,30,seed=1), smp.KMPathSampler(100,30,70,seed=1)], [smp.SimpleGraphDegree(),smp.SimpleGraphPathLength()], [smp.BackendQuery(), smp.FrontendQuery()], create_logger=True)
    #print result