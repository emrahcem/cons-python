

'''
Created on May 19, 2013

@author: Emrah Cem(emrah.cem@utdallas.edu)
'''
from xml.dom.minidom import parse 


__all__=['read_xml']

def __getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def __convert_to_type(str_val,str_type):
    result=None
    if str_type=="int":
        result=int(str_val)
    elif str_type=="float":
        result=float(str_val)
    elif str_type=="bool":
        if str_val.upper() == 'TRUE':
            result=True
        else:
            result=False
    elif str_type=="str":
        result=str_val
    return result
   
def __handle_graphs(graphs,seed):    
    def handle_graph(graph):
        def handle_graph_folder_name(name):
            return __getText(name.childNodes)
        def handle_graph_distribution_file_name(name):
            return __getText(name.childNodes)
        def handle_graph_params(params):
            def handle_graph_param(param):
                def handle_graph_param_name(name):
                    return __getText(name.childNodes)
                def handle_graph_param_value(value):
                    return __convert_to_type(__getText(value.childNodes), value.getAttribute('type'))
                    
                name=handle_graph_param_name(param.getElementsByTagName('param_name')[0])
                value=handle_graph_param_value(param.getElementsByTagName('param_value')[0])
                return (name,value)
           
            param_dict={}
            for param in params:
                param_dict[handle_graph_param(param)[0]]=handle_graph_param(param)[1]
            param_dict['seed']=seed 
            return param_dict
        
        class_name=graph.getAttribute('class')
        
        folder_name=handle_graph_folder_name(graph.getElementsByTagName('folder_name')[0])
        print graph.getElementsByTagName('distribution_file_name')
        if len(graph.getElementsByTagName('distribution_file_name'))>0:
            distribution_file_name=handle_graph_distribution_file_name(graph.getElementsByTagName('distribution_file_name')[0])
        params=graph.getElementsByTagName('param')
        par_dict=handle_graph_params(params)
        par_dict['folder_name']=folder_name
        if len(graph.getElementsByTagName('distribution_file_name'))>0:
            par_dict['distribution_file_name']=distribution_file_name
        return (class_name, par_dict)
    
    g_list=[]
    for graph in graphs:
        g_list.append(handle_graph(graph))

    return g_list

def __handle_features(features):
    def handle_feature(feature):
        def handle_feature_name(name):
            return __getText(name.childNodes)
    
        handle_feature_name(feature.getElementsByTagName('name')[0])
        return feature.getAttribute('class')

    f_list=[]
    for feature in features:
        f_list.append(handle_feature(feature))

    return f_list

def __handle_queries(queries):    
    def handle_query(query):
        def handle_query_name(name):
            return __getText(name.childNodes)

        
        handle_query_name(query.getElementsByTagName('name')[0])
        return query.getAttribute('class')
        
    q_list=[]
    for query in queries:
        q_list.append(handle_query(query))
        
    return q_list
    

def __handle_samplers(samplers,seed):
    def handle_sampler(sampler):
        def handle_sampler_name(name):
            return __getText(name.childNodes)
        
        def handle_sampler_params(params):
            def handle_sampler_param(param):
                def handle_sampler_param_name(name):
                    return __getText(name.childNodes)
    
                def handle_sampler_param_value(value):
                    return __convert_to_type(__getText(value.childNodes), value.getAttribute('type'))
                    
                name=handle_sampler_param_name(param.getElementsByTagName('param_name')[0])
                value=handle_sampler_param_value(param.getElementsByTagName('param_value')[0])
                return(name,value)
            
            param_dict={}
            for param in params:
                param_dict[handle_sampler_param(param)[0]]=handle_sampler_param(param)[1]
            if not sampler_name=="Original":
                param_dict['seed']=seed 
            return param_dict
             
        class_name=sampler.getAttribute('class')
        sampler_name=handle_sampler_name(sampler.getElementsByTagName('name')[0])
        params_node=sampler.getElementsByTagName('params')[0]
        params=params_node.getElementsByTagName('param')
        par_dict=handle_sampler_params(params)
        return (class_name, par_dict)
    
    s_list=[]    
    for sampler in samplers:
        s_list.append(handle_sampler(sampler))
    
    return s_list

def __handle_jobs(jobs,seed):
    def handle_job(job):
        times_to_sample=int(job.getAttribute('times_to_sample'))
        sample_size=int(job.getAttribute('sample_size')) if job.getAttribute('sample_size')!="" else None 
        job_name = job.getAttribute('name')
        graphs=job.getElementsByTagName('Graph')
        g_list=__handle_graphs(graphs,seed)
        features=job.getElementsByTagName('Feature')
        f_list=__handle_features(features)
        queries=job.getElementsByTagName('Query')
        q_list=__handle_queries(queries)
        samplers=job.getElementsByTagName('Sampler')
        s_list=__handle_samplers(samplers,seed)
        if sample_size is not None:
            for s in s_list:
                s[1]['sample_size']=sample_size
        return {'Graph':g_list, 'Feature':f_list, 'Query':q_list, 'Sampler':s_list}, {'name':job_name, 'times_to_sample':times_to_sample}
    
    
    exp_result=[]
    for job in jobs:
        exp_result.append(handle_job(job))
    return exp_result

#def __handle_experiments(exps):
#    def handle_experiment(exp):
#        seed=int(exp.getAttribute('seed'))
#        jobs=exp.getElementsByTagName('job')
#        j_list=__handle_jobs(jobs,seed)
        

def read_xml(xml_doc):
    #xml_doc=open(file_name,'r')
    dom=parse(xml_doc)
    exp=dom.getElementsByTagName('experiment')[0]
    seed=int(exp.getAttribute('seed'))
    jobs=exp.getElementsByTagName('job')
    return seed, __handle_jobs(jobs,seed)
    #exps=dom.getElementsByTagName('experiment')
    #return __handle_experiments(exps)