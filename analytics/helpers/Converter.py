'''
Created on May 23, 2013

@author: ecem
'''

import pandas as pnd

import analytics
 
__all__=['panel5D_to_dataframe']

    
def panel5D_to_dataframe(panel5d):
    df=pnd.DataFrame(columns=['graph','sampler','exp','query','feature','p-dist','s-dist'])
    for graph in panel5d.graphs:
        for sampler in panel5d.samplers:
                for exp in panel5d.experiments:
                    for query in panel5d.queries:
                        for feature in panel5d.features:
                            if 'Original' in panel5d.samplers:
                                dic={'graph':graph,'sampler':sampler,'exp':exp,'query':query,'feature':feature,'p-dist':panel5d.ix[graph,'Original',exp,query,feature],'s-dist':panel5d.ix[graph,sampler,exp,query,feature]}
                            else:
                                dic={'graph':graph,'sampler':sampler,'exp':exp,'query':query,'feature':feature,'s-dist':panel5d.ix[graph,sampler,exp,query,feature]}
                            df=df.append(pnd.Series(dic), ignore_index=True)
        
    jd={}
    jsd={}
    ksd={}
    if 'Original' in panel5d.samplers:
        for i,(p,s) in enumerate(zip(df['p-dist'],df['s-dist'])):
            jd[i]=analytics.JeffreyDivergence().compute(p,s)
            jsd[i]=analytics.JensenShannonDivergence().compute(p,s)
            ksd[i]=analytics.KolmogorovSmirnovDistance().compute(p,s)
        
        df[analytics.JeffreyDivergence().abbreviation]=pnd.Series(jd)
        df[analytics.JensenShannonDivergence().abbreviation]=pnd.Series(jsd)
        df[analytics.KolmogorovSmirnovDistance().abbreviation]=pnd.Series(ksd)
    
    return df
