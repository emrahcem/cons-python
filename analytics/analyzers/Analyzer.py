'''
Created on Aug 4, 2013

@author: Emrah Cem{emrah.cem@utdallas.edu}
'''

from abc import ABCMeta, abstractmethod 
from pandas import Panel, Series, DataFrame
import pickle
import os
import matplotlib.pyplot as plt

import analytics.divergence.DivergenceMetrics as divergence_metrics
import analytics.helpers.Dict_operations as dict_ops
import analytics.plotting.SamplerPlotter as sampler_plotter
import analytics.plotting.DescriptiveStatsPlotter as descriptive_stats_plotter
import analytics.plotting.DistributionPlotter as distribution_plotter
from numpy.core.numeric import broadcast

__all__=['AnalysisGroup','Analysis','SamplerAnalysis', 'SamplerBoxplotAnalysis','SamplerDescriptiveAnalysis','SamplerDistributionPlotAnalysis','SamplerPdfCdfPlotAnalysis', \
         'GraphDistributionPlotAnalysis','GraphDensityPlotAnalysis', 'CombinedAnalysis', 'PopulationAnalysis', 'PopulationFeaturesPlotAnalysis']

class AnalysisGroup:

    def __init__(self):
        self.analysis_list=[]
    
    def add_analysis(self, analysis):
        '''Adds an analyzer to the analysis group.'''
        self.analysis_list.append(analysis)
    
    def remove_analysis(self, analysis):
        self.analysis_list.remove(analysis)
    
    def get_analysis_list(self):
        return self.analysis_list
        
    def analyze(self):
        for analysis in self.analysis_list:
            analysis.analyze()


class Analysis:
    __metaclass__ = ABCMeta
 
    @abstractmethod
    def analyze(self):
        pass

    def set_title(self, title):
        self.title = title
        
    def set_data(self, data):
        self.data = data
    
    def set_file_name(self, file_name):
        self.file_name = file_name
                     
class PopulationAnalysis(Analysis):
    
    def __init__(self, data, title=None, file_name=None):
       self.data = data
       self.title = title
       self.file_name = file_name 
   
    @abstractmethod
    def analyze(self):
        pass


class PopulationFeaturesPlotAnalysis(PopulationAnalysis):
    
    def __init__(self, data, title=None, file_name='features_distribution.pdf'):
        super(PopulationFeaturesPlotAnalysis, self).__init__(data, title, file_name)
    
    def analyze(self):
        descriptive_stats_plotter.save_pdf_cdf_plot_for_a_single_graph(self.data, self.title, statistics_included=True, file_name=self.file_name, show=False)
        
           
class CombinedAnalysis(Analysis):
    
    def __init__(self, data, title=None, file_name=None):
        self.data = data
        self.title = title
        self.file_name = file_name
    
    @abstractmethod
    def analyze(self):
        pass
    

class GraphDistributionPlotAnalysis(CombinedAnalysis):

    def __init__(self, data, divergence=divergence_metrics.JensenShannonDivergence, title=None, file_name='graph_distribution.pdf'):
        super(GraphDistributionPlotAnalysis, self).__init__(data, title, file_name)
        self.divergence = divergence
        
    def analyze(self):
        distribution_plotter.save_distributions_for_single_graph(self.data, fig_title=self.title, divergence=self.divergence, single_fig_size=(6,4), plot_dims=(3,2), file_name=self.file_name)


class GraphDensityPlotAnalysis(CombinedAnalysis):

    def __init__(self ,data, divergence=divergence_metrics.JensenShannonDivergence, title=None, file_name='graph_density.pdf'):
        super(GraphDensityPlotAnalysis, self).__init__(data, title, file_name)
        
    def analyze(self):
        distribution_plotter.save_distributions_for_single_graph(self.data, fig_title=self.title, divergence=self.divergence, cdf= False, single_fig_size=(6,4), plot_dims=(3,2), file_name=self.file_name)


class SamplerAnalysis(Analysis):
    
    def __init__(self, sampler_dic,pop_dic, title=None, file_name=None):
        self.sampler_dic=sampler_dic
        self.pop_dic=pop_dic
        self.title=title
        self.file_name=file_name
        
    @abstractmethod
    def analyze(self):
        pass
      
    def get_divergence_scores_panel(self, divergence=divergence_metrics.JensenShannonDivergence):
        exp_panel=Panel.from_dict(self.sampler_dic)
        exp_dic={}
        for exp_no in exp_panel.items:
            q_dic={}
            for query in exp_panel.major_axis:
                f_dic={}
                for feature in exp_panel.minor_axis:
                    K=exp_panel.ix[exp_no,query,feature]
                    H= self.pop_dic[feature]#orig_panel.ix[0,major,minor]
                    f_dic[feature]=divergence.compute(H, K)
                q_dic[query]=Series(f_dic)
            exp_dic[exp_no]=DataFrame(q_dic)
        return Panel.from_dict(exp_dic, orient='minor')


class SamplerDescriptiveAnalysis(SamplerAnalysis):
    
    def __init__(self, sampler_dic,pop_dic, divergence=divergence_metrics.JensenShannonDivergence, file_name='summary.txt'):
        super(SamplerDescriptiveAnalysis, self).__init__(sampler_dic,pop_dic, file_name=file_name)
        self.divergence=divergence
        
    def analyze(self):
        pnl=self.get_divergence_scores_panel(self.divergence)
        for query in pnl.items:
            with open(self.file_name.rsplit('.',1)[0]+'_'+query+'.'+self.file_name.rsplit('.',1)[1],'w') as f:
                f.write(pnl[query].T.describe().to_string()+'\n')


class SamplerBoxplotAnalysis(SamplerAnalysis):
    
    def __init__(self, sampler_dic, pop_dic, divergence=divergence_metrics.JensenShannonDivergence, title=None, file_name='boxplot.pdf', show=False):
        super(SamplerBoxplotAnalysis, self).__init__(sampler_dic,pop_dic, title, file_name)
        self.divergence=divergence
        self.title=title
        self.show=show
        
    def analyze(self):
        pnl=self.get_divergence_scores_panel(self.divergence)
        pickle.dump(pnl, open(os.path.join(os.path.dirname(self.file_name),'divergence_scores_panel.pickle'),'w') )
        
        for query in pnl.items:
            #pnl[query].to_csv(open(os.path.join(os.getcwd(),divergence().name+'.csv'),'w'))
            #pnl[query].to_html(open(os.path.join(os.getcwd(),divergence().name+'.html'),'w'))
            fig=plt.figure()
            pnl[query].T.boxplot()
            plt.ylim(0,1.01)
            plt.ylabel(self.divergence().abbreviation+' score')
            if self.title is None:
                plt.title(self.divergence().abbreviation+' ('+query+')')
            else:
                plt.title(self.title+' ('+query+')')
            fig.savefig(self.file_name.rsplit('.',1)[0]+'_'+query+'.'+self.file_name.rsplit('.',1)[1])
        if self.show:
            plt.show()
            plt.close()
            #plt.clf()

class SamplerDistributionPlotAnalysis(SamplerAnalysis):
    def __init__(self, sampler_dic,pop_dic, title='Characteristic Distributions in the sample graph', file_name='CDF_with_population_distribution.pdf'):
        super(SamplerDistributionPlotAnalysis, self).__init__(sampler_dic,pop_dic, title, file_name=file_name)
    
    def analyze(self):
        sampler_plotter.save_sampler_distribution(Panel.from_dict(self.sampler_dic), pop_dic=self.pop_dic, title=self.title, file_name=self.file_name)


class SamplerPdfCdfPlotAnalysis(SamplerAnalysis):    
    
    def __init__(self, sampler_dic, title='Characteristic Distribution and Descriptive Statistics',file_name='CDF_PDF_plot.pdf'):
        super(SamplerPdfCdfPlotAnalysis, self).__init__(sampler_dic,None, title, file_name=file_name)
        
    def analyze(self):
        panel=Panel.from_dict(self.sampler_dic)
        t_panel=panel.transpose(1,0,2)
        num_of_queries= len(t_panel.items)
        for i,query  in enumerate(t_panel.items):
            dic={}
            #for (feature,distribution) in t_panel[query].apply(dict_ops.avg_list_of_dictionaries,axis=0, reduce=False).iteritems():
            #    dic[feature]=distribution          
            for feature in t_panel[query].columns:
                dic[feature] = dict_ops.avg_list_of_dictionaries(t_panel[query][feature].tolist())
            descriptive_stats_plotter.save_pdf_cdf_plot_for_a_single_graph(dic, self.title+'\n('+query+')', statistics_included=True, file_name= self.file_name.rsplit('.',1)[0]+'_'+query+'.'+self.file_name.rsplit('.',1)[1], show=True if i==num_of_queries-1 else False)
            