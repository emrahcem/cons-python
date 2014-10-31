import time
import datetime
from sys import stdout
from multiprocessing import Pool
import networkx as nx
from collections import Counter
import numpy as np
__all__=['run']

def degree_task(G,chunk):
    return dict(Counter(nx.degree(G,chunk).values()))
    

def clustering_coefficient_task(G,chunk):
    clust=nx.clustering(G,nodes=chunk)
    bins=np.linspace(0,1,1001)
    digitized=np.digitize(clust.values(),bins)/1000.0
    f_dic=dict(Counter(digitized.tolist()))
    return f_dic
    
def shortest_path_task(G,sources=None, targets=None):
    dic={}
    #===========================================================================
    # if targets is None:
    #     targets=list(xrange(len(G.vs)))
    # #print 'input',sources,targets
    # for s in sources:
    #     l=[t for t in targets if t>s]
    #     #print 'find from ',sources,' to', l
    #     if len(l)>0:
    #         res=G.shortest_paths(s,l, mode='ALL')
    #         feature_dic=dict(Counter(res[0]))
    #         #print s, feature_dic
    #         un=set(dic.keys()).union(set(feature_dic.keys()))
    #         dic.update(dic.fromkeys(un.difference(dic.keys()),0))
    #         feature_dic.update(feature_dic.fromkeys(un.difference(feature_dic.keys()),0))
    #         dic.update(dict((s,dic[s]+feature_dic[s]) for s in feature_dic))
    #===========================================================================
    res=G.shortest_paths(sources,targets, mode="ALL")
    for i,_ in enumerate(sources):
        res[i].remove(0)
        #print ch,res[i]
        feature_dic=dict(Counter(res[i]))
        un=set(dic.keys()).union(set(feature_dic.keys()))
        dic.update(dic.fromkeys(un.difference(dic.keys()),0))
        feature_dic.update(feature_dic.fromkeys(un.difference(feature_dic.keys()),0))
        dic.update(dict((s,dic[s]+feature_dic[s]) for s in feature_dic))
      
    
    #===========================================================================
    # if targets is None:
    #     targets=G.nodes()
    #       
    # for node in sources:
    #     spls=nx.single_source_shortest_path_length(G,node)
    #      
    #     spls={k:v for k,v in spls.items() if k in targets}
    #     spls.pop(node)
    #     feature_dic=dict(Counter(spls.values()))
    #     un=set(dic.keys()).union(set(feature_dic.keys()))
    #     dic.update(dic.fromkeys(un.difference(dic.keys()),0))
    #     feature_dic.update(feature_dic.fromkeys(un.difference(feature_dic.keys()),0))
    #     dic.update(dict((s,dic[s]+feature_dic[s]) for s in feature_dic))
    #===========================================================================
    #print 'dic:',dic
    
    #if len(dic)==0:
    #    return {0:1.0}
    #else:
    return dic


def parallel_star(args):
    def function_call(func,args):
        return func(*args)
    return function_call(*args)

def run(parallelTask, normalize=True):
    pool=Pool()
    imap_unordered_it = pool.imap_unordered(parallel_star, parallelTask.TASKS)
    result=[]
    counter=0
    num_of_chunks=len(parallelTask.TASKS)
    begin=time.time()
    
    for x in imap_unordered_it:
        stdout.write("\r%{0} completed in {1:s} sec".format(int(counter*100/num_of_chunks),str(datetime.timedelta(seconds=time.time()-begin))))
        stdout.flush()
        counter+=1
        result.append(x)
    stdout.write("\r%{0} completed in {1:s}".format(int(counter*100/num_of_chunks),str(datetime.timedelta(seconds=time.time()-begin))))    
    stdout.write("\r")
    stdout.flush()
    
    sum_dic=_sum_list_of_dictionaries(result)
    #print 'sum_dic',sum_dic
    sum_dic.pop(float('Inf'),0)
    
    if len(sum_dic)==0:
        sum_dic={0:1}
    
    if normalize:
        total=sum(sum_dic.values())
        sum_dic={k:v/total for k,v in sum_dic.items()}
    pool.close()
    pool.join()
    return sum_dic


def _sum_list_of_dictionaries(list_of_dic):
    combine=[]
    for dic in list_of_dic:
        combine+=dic.items()
    all_keys=dict(combine).keys()
    result={}
    for key in all_keys:
        total_val_of_key=0.0
        for dic in list_of_dic:
            if dic.has_key(key):
                total_val_of_key+=dic[key]
        result[key]=total_val_of_key
    return result
