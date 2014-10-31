'''
Created on May 17, 2013

@author: ecem
'''

import logging
import sampling as smp

log = logging.getLogger(__name__)

__all__=['execute_single_query','execute_all_frontend_queries','execute_all_backend_queries','compute_queries','execute_all_queries_for_a_feature']
from sampling.classes.query_types import *

def compute_single_query(feature, query):
    try: 
        log.debug('Running '+query.name+' for '+feature.name)
        return query.run_query(feature)
    except TypeError:
        log.debug('Error in query execution:'+query.name)
        log.debug("Ignoring query.")

def compute_queries(query, feature_list):
    feature_dic={}
    log.info('Computing characteristics of population graph')
    for feature in feature_list:
        result=compute_single_query(feature, query)
        if result!=None:
            feature_dic[feature.name]=result
    return feature_dic

def compute_all_frontend_queries(G, feature_list):
    feature_dic={}
    for feature in feature_list:
        result=compute_single_query(feature, FrontendQuery(G))
        if result!=None:
            feature_dic[feature.name]=result
    return feature_dic

def compute_all_backend_queries(G, sample_graph, feature_list):
    feature_dic={}
    for feature in feature_list:
        result=compute_single_query(feature, BackendQuery(G, sample_graph))
        if result!=None:
            feature_dic[feature.name]=result
    return feature_dic
           
def compute_all_queries_for_a_feature(G, sample_graph, feature, query_list): 
    query_dic={}
    for query in query_list:
        if type(query) == BackendQuery: 
            query.set_population_graph(G)
            query.set_sample_graph(sample_graph)
        elif type(query) == FrontendQuery:
            query.set_graph(sample_graph)
        result=compute_single_query(feature,query)
        if result !=None:
            query_dic[query.name]=result
            #DataFramePlotter().plot_data(DataFrame.from_dict({'sample':result,'population':Globals.curr_graph_distributions[0][feature.name]['Backend Query']}),saveTo=Globals.curr_dir, cumulative=True, title=feature.name+'('+query.name+')',ylim=(0,1.01))           
    #log.debug(feature.name+':'+str(query_dic))
    return query_dic
         
def compute_all_features(G, sample_graph, feature_list, query_list):
    feature_dic={}
    for feature in feature_list:
        result=compute_all_queries_for_a_feature(G, sample_graph, feature, query_list)
        if result !=None:
            feature_dic[feature.name]=result
        
    return feature_dic

# if __name__ == "__main__":
#     import networkx as nx
#     import sampling as smp
#     
#     G=nx.barabasi_albert_graph(10, 4, 3)
#     nx.write_gml(G, 'G.gml')
#     sample_graph=smp.induced_random_edge_sampler(G, 5, True, False)
#     print sample_graph.nodes()
#     print sample_graph.edges()
#     nx.write_gml(sample_graph, 'sample.gml')
#     q_list=[BackendQuery(), FrontendQuery()]
#     f_list=[smp.SimpleGraphDegree()]
#     ex=QueryExecuter()
#     print ex.compute_all_queries(G, sample_graph, f_list, q_list)
    