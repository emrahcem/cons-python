'''
Created on May 17, 2013

@author: ecem
'''

from abc import ABCMeta #, abstractmethod, abstractproperty
from pandas.core import panelnd
from pandas.core.panel4d import Panel4D

from sampling.helpers import Folder_creator, Logger 
from sampling.experiment import SamplingJobExecuter

import os
import logging
import pickle 
import analytics

__all__=['Experiment']

logger= logging.getLogger(__name__)

def createPanel5D(dic):
    Panel5D = panelnd.create_nd_panel_factory(
                                                  klass_name   = 'Panel5D',
                                                  axis_orders  = [ 'graphs', 'samplers','experiments','queries','features'],
                                                  axis_slices  = { 'samplers' : 'labels', 'experiments' : 'items', 'queries' : 'major_axis', 'features' : 'minor_axis' },
                                                  slicer       = Panel4D,
                                                  axis_aliases = { 'major' : 'major_axis', 'minor' : 'minor_axis' },
                                                  stat_axis    = 2)            
    p_5d=Panel5D.from_dict(dic)
    return p_5d


class Experiment():
    __metaclass__ = ABCMeta
     
    def __init__(self):
        self.sampling_jobs=[]
    
    def add_sampling_job(self, job):
        self.sampling_jobs.append(job)
    
    def remove_sampling_job(self, job):
        self.sampling_jobs.remove(job)
    
    def set_seed(self, seed):
        self.seed=seed
    
    def set_input_file(self, file_name):
        self.file_name=file_name
    
    def get_input_file(self):
        return self.file_name
        
    def run(self):
        for job in self.sampling_jobs:
            try:
                if Folder_creator.create_job_folder(job.name, self.get_input_file()):
                    Logger.create_logger()
                    
                    result_dic,graph_attribute=SamplingJobExecuter.execute_all_graphs(job, self.seed)
                    pickle.dump(result_dic, open(os.path.join(os.getcwd(),'result_dic.pickle'),'w'))
                    pickle.dump(analytics.panel5D_to_dataframe(createPanel5D(result_dic)), open(os.path.join(os.getcwd(),'result_df.pickle'),'w'))
                    
                    #analysis_group=analytics.AnalysisGroup();
                    #analysis_group.add_analysis(analytics.PopulationFeaturesPlotAnalysis( os.path.join(graph_attribute['folder_name'], 'population') ))
                    #analysis_group.add_analysis(analytics.GraphDistributionPlotAnalysis())
                    #analysis_group.add_analysis(analytics.GraphDensityPlotAnalysis())
                    
                    #analyzer=analytics.Analyzer(analysis_group, graph_attr)
                    #analyzer.analyze()
                    
                    os.chdir('..')
            except Exception as e:
                logger.exception(e)    
                    
            #pickle.dump(result_dic, open(os.path.join(os.getcwd(),'result_dic.pickle'),'w'))
            
            #panel5d_for_all_graphs=createPanel5D(result_dic)
            #print panel5d_for_all_graphs
            #pickle.dump(analytics.panel5D_to_dataframe(panel5d_for_all_graphs), open(os.path.join(os.getcwd(),'result_df.pickle'),'w'))
            
            
            #result_panel=createPanel5D(SamplingJobExecuter().execute(job,seed_val))
            #analyzer=AnalyzerList()
            #analyzer.addAnalyzer(PlotCDF())
            #analyzer.addAnalyzer(PlotPDF())
            #analyzer.analyze_result(result_panel)
            #print result_panel
            #Plotter.save_plots(result)


#if __name__ =='__main__':
    
    #logging.basicConfig(filename='sampling.log', level=logging.INFO)
    
    
    #g_list=[BarabasiAlbertGraphGenerator(10, 4, 3)]
#     g_list=[FromFileGraphGenerator(path_to_file, name, abbreviation)]
#     q_list=[BackendQuery(), FrontendQuery()]
#     f_list=[SimpleGraphDegree(),SimpleGraphPathLength()]
#     s_list=[InducedRandomVertexSampler(5, True, False, 3)]
#     
#     job=SamplingJob()
#     job.set_number_of_times_to_sample(5)
#     [job.add_graph_gen(gr_gen) for gr_gen in g_list]
#     [job.add_feature(feature) for feature in f_list]
#     [job.add_query(query) for query in q_list]
#     [job.add_sampling_method(smp) for smp in s_list]
#     
#     exp=Experiment()
#     exp.add_sampling_job(job)
#     exp.run()

