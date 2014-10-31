'''
Created on May 21, 2013
@author: Emrah Cem(emrah.cem@utdallas.edu)
'''
from abc import ABCMeta, abstractmethod #, abstractproperty
from pandas import Panel, Series,DataFrame, Panel4D
import os
#import pickle
import matplotlib.pyplot as plt
from matplotlib import figure

__all__=['AnalyzerList','SeriesPlotter','DataFramePlotter','Panel4DPlotter']

class AnalyzerList(object):
    '''
    The container for analyzers.
    '''
    def __init__(self):
        self.analyzerList=[]
    
    def addAnalyzer(self, analyzer):
        self.analyzerList.append(analyzer)
    
     
    def analyze_result(self,result):
        for analyzer in self.analyzerList:
            analyzer.analyze(result)


class Analyzer:
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def analyze(self, result_panel):
        pass

class SampleAnalyzer(Analyzer):

    def __init__(self, title):
        self.title=title
    
    def _plot(self, df, pdf=True):
        plt.figure()
        if pdf:
            df.plot(kind='line')
        else:
            df.cumsum().plot(kind='line')
        plt.legend()
        plt.ylim((0,1))
        plt.show()
        
    def analyze(self, feature_dic, orig_dic, save_to_file=True):
        df=DataFrame({'sample':Series(feature_dic), 'original':Series(orig_dic)})
        self._plot(df)
        #Series(feature_dic).plot(label='sample',style='r')
        #Series(orig_dic).plot(label='original')
        #plt.legend()
        #plt.ylim((0,1))
        #plt.title(self.title)
        #print 'saving to:', os.path.join(sampling_globals.curr_dir,'pdfs',self.title+'.eps')
        #plt.savefig(os.path.join(sampling_globals.curr_dir,'pdfs',self.title+'.eps'))
        #plt.savefig(os.path.join(sampling_globals.curr_dir,'pdfs',self.title+'.pdf'))
        #plt.show()

    
#===============================================================================
# class SamplerAnalyzer(Analyzer):
#     
#     def __init__(self, pop_dic, sampler_dic):
#         self.sampler_dic=sampler_dic
#         self.pop_dic=pop_dic
#         
#     def analyze(self, divergence=analytics.DivergenceMetrics.JensenShannonDivergence):
#         exp_panel=Panel.from_dict(self.sampler_dic)
#         #orig_panel=Panel.from_dict(self.pop_dic)
#         exp_dic={}
#         for exp_no in exp_panel.items:
#             q_dic={}
#             for query in exp_panel.major_axis:
#                 f_dic={}
#                 for feature in exp_panel.minor_axis:
#                     K=exp_panel.ix[exp_no,query,feature]
#                     H= self.pop_dic[feature]#orig_panel.ix[0,major,minor]
#                     f_dic[feature]=divergence.compute(H, K)
#                 q_dic[query]=Series(f_dic)
#             exp_dic[exp_no]=DataFrame(q_dic)
#         pnl=Panel.from_dict(exp_dic, orient='minor')
#         #temp=os.getcwd()
#         pickle.dump(pnl, open(os.path.join(os.getcwd(),'sampler_panel.pickle'),'w') )
#         
#         for query in exp_panel.major_axis:
#             #pnl[query].to_csv(open(os.path.join(os.getcwd(),divergence().name+'.csv'),'w'))
#             #pnl[query].to_html(open(os.path.join(os.getcwd(),divergence().name+'.html'),'w'))
#             plt.figure()
#             pnl[query].T.boxplot()
#             plt.ylim(0,1.01)
#             plt.ylabel(divergence().name+' score')
#             plt.savefig(open(os.path.join(os.getcwd(),divergence().name+'_'+query+'_boxplot.pdf'),'w'))
#             with open(os.path.join(os.getcwd(),divergence().name+'_'+query+'.txt'),'w') as f:
#                 f.write(pnl[query].T.describe().to_string()+'\n')
#         #smp.sampling_globals.curr_dir=temp
#         return pnl
#===============================================================================
 
class Plotter:
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def plot_data(self):
        pass


class SeriesPlotter(Plotter):
    def plot_data(self, series, cumulative=False, *args, **kwds):
        if cumulative:
            series.plot(*args, **kwds)
        else:
            series.cumsum().plot(*args, **kwds)

        plt.legend()
        #plt.ylim((0,1))
        #plt.show()
        
   
class DataFramePlotter(Plotter):
    def plot_data(self, df,  cumulative=False, show=False, saveTo=None, *args, **kwds):
        figure.Figure()
        df=df.fillna(0)
        if cumulative:
            df.cumsum().plot(*args, **kwds)
        else:
            df.plot(*args, **kwds)
        
        plt.title(kwds['title'])
        plt.ylim(0,1.01)
        plt.legend(loc='best')
        #plt.ylim((0,1))
        if show:
            plt.show()
        if saveTo !=None:
            if cumulative:
                if kwds.has_key('title'):
                    plt.savefig(os.path.join(saveTo,kwds['title']+'_cumulative.eps'))
                    plt.savefig(os.path.join(saveTo,kwds['title']+'_cumulative.pdf'))
                else:
                    plt.savefig(os.path.join(saveTo,'cumulative.eps'))
                    plt.savefig(os.path.join(saveTo,'cumulative.pdf'))
            else:
                if kwds.has_key('title'):
                    plt.savefig(os.path.join(saveTo,kwds['title']+'.eps'))
                    plt.savefig(os.path.join(saveTo,kwds['title']+'.pdf'))
                else:
                    plt.savefig(os.path.join(saveTo,'fig.eps'))
                    plt.savefig(os.path.join(saveTo,'fig.pdf'))
        plt.clf()
    
#===============================================================================
# class Panel4DPlotter(Plotter):
#     def plot_data(self,panel4D, cumulative=False, show=False, saveTo=False,*args, **kwds):
#         meaned=panel4D.mean(axis=0)
#         for feature in meaned.items:
#                 res=meaned[feature]
#                 for query in meaned.minor_axis:
#                     df=DataFrame.from_dict({'population': Series(self.G.graph['distribution'][0][feature][query]).fillna(0),'sample':res[query][(res[query]>0) & (res[query]<.999999)]})
#                     if kwds.has_key('title'):
#                         DataFramePlotter().plot_data(df, cumulative, show, saveTo, title=kwds['title']+','+feature+','+query)
#                     else:
#                         DataFramePlotter().plot_data(df, cumulative, show, saveTo, title=feature+','+query)
# 
# class Panel5DPlotter(Plotter):
#     def plot_data(self,panel5D, cumulative=False, *args, **kwds):
#         for label in panel5D.labels:
#             Panel4DPlotter().plot_data(panel5D[label], cumulative, title=label)
#===============================================================================
            
class PlotPDF(Analyzer):

    def analyze(self, result_panel):
        print 'PDF will be plotted'
        
    
class PlotCDF(Analyzer):

    def analyze(self, result_panel):
        print 'CDF will be plotted'
        
if __name__ == '__main__':
#DATAFRAME
#     df_plotter=DataFramePlotter() 
#     dii={'sample':{1:2,2:3,4:67,5:70},'orig':{1:20,2:30,4:60,5:80}}
#     df_plotter.plot_data(DataFrame.from_dict(dii), pdf=True)
  
#PANEL    
#     pnl_plotter=PanelPlotter() 
    dp={'minor1':{'item1':{1:2,2:3,4:67,5:70},'item2':{1:20,2:30,4:60,5:80}}, 'minor2':{'item1':{1:5,2:7,4:47,5:10},'item2':{1:2,2:3,4:6,5:8}}, 'minor3':{'item1':{1:32,2:31,4:7,5:30},'item2':{1:30,2:20,4:50,5:80}}}
    pnl=Panel.from_dict(dp, orient='minor')
#     print pnl
#     for item in pnl.items:
#         print pnl[item]
#         DataFramePlotter().plot_data(pnl[item], cumulative=True, title=item)

#PANEL4D
    dp4={'label1':pnl, 'label2':pnl}
    pnl4D=Panel4D(dp4)
    for label in pnl4D.labels:
        #print label
        pnl=pnl4D.ix[label]
        for item in pnl.items:
            #print item
            #print pnl4D.ix[label,item]
            



    #pnl=pnl.transpose(1,0,2)
#     for items in pnl.items:
#         print items
#         for major in pnl.major_axis:
#             print '\t',major
#             for minor in pnl.minor_axis:
#                 print '\t\t',minor, '==','val:',pnl.ix[items,major,minor]
    
    
    #for major in pnl.major_axis:
    #    print pnl[major]    
    #pnl_plotter.plot_data(Panel.from_dict(dp, orient='minor'), pdf=True)
    
    
    
    
#     name_list=['a','b']
#     dic_list=[{0:1,2:4,5:10}]
#     
#     new_dic={}
#     for i,dic in enumerate(dic_list):
#         new_dic[name_list[i]]=dic
#     
        
    #df_plotter.plot_data(DataFrame.from_dict(new_dic),pdf=False, kind='line',grid=True)
        #Analyzer.analyze_result(self, result)
        #             for sampling_method 
#             f = open(''.join([str(job.graph_gen.name),'.out']), 'w')
#             result[job],H[job]=SamplingJobExecuter().compute_all_samplers(job, exp.num_of_samples, exp.seed_val)
#             sys.stdout=f
#             print >>f, '----------------------------'
#             print >>f, 'EXPERIMENTAL RESULTS'
#             print >>f, '----------------------------'
#             for sampling_method, exp_dic in result[job].items():
#                 print >>f, '\t',sampling_method.name
#                 for exp_no, feature_dic in exp_dic.items():
#                     print >>f, '\tsample ', exp_no
#                     print >>f, '\t','-'*len(''.join(['\texperiment ', str(exp_no)]))
#                     for feature, query_dic in feature_dic.items():
#                         print >>f, '\t->',feature.name
#                         for query, distribution in query_dic.items():
#                             print >>f, '\t  ',query.name
#                             print >>f, '\t  ',distribution
#                             if H[job]==None:
#                                 li.append([job.graph_gen.name, job.graph_gen.abbreviation, len(job.graph_gen.G), sampling_method.name, exp_no, feature.name, query.name, None ,distribution])
#                             else:
#                                 li.append([job.graph_gen.name, job.graph_gen.abbreviation, len(job.graph_gen.G), sampling_method.name, exp_no, feature.name, query.name, jeffrey_divergence(H[job][feature],distribution),distribution])
#             sys.stdout=std_out
#         df=DataFrame(li,columns=['graph_name', 'graph_abbreviaton', 'input_population_size','sampling_method','exp_no','feature_name','query_type','divergence','distribution']) 
#         return df