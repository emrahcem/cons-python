import numpy as np

__all__=['sum_list_of_dictionaries','avg_list_of_dictionaries']


def sum_list_of_dictionaries(list_of_dic):
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

def avg_list_of_dictionaries(list_of_dic):
    result=sum_list_of_dictionaries(list_of_dic)
    num_of_dics=len(list_of_dic)
    result={k:v/num_of_dics for k,v in result.items()}
    return result

def get_key_and_val_as_sorted_lists(freq_dic,pdf=True):
    key,val=zip(*[(item[0],item[1]) for item in sorted(freq_dic.items())])
    if not pdf:
        val=np.cumsum(val)
    return key,val
