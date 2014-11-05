'''
Created on Nov 13, 2013

@author: Emrah Cem{emrah.cem@utdallas.edu}
'''
import pandas as pnd
from pandas.core import panelnd
from pandas.core.panel4d import Panel4D


__all__=['create_5D_panel_from_dic', 'create_graph_panel_from_dic']

def create_graph_panel_from_dic(graph_dic):
    GraphPanel= panelnd.create_nd_panel_factory(
                                      klass_name   = 'GraphPanel',
                                      orders  = ['samplers','experiments','queries','features'],
                                      slices  = { 'experiments' : 'items', 'queries' : 'major_axis', 'features' : 'minor_axis' },
                                      slicer       = pnd.Panel,
                                      aliases = { 'major' : 'major_axis', 'minor' : 'minor_axis' },
                                      stat_axis    = 2)
    
    return GraphPanel.from_dict(graph_dic)

def create_5D_panel_from_dic(dic):
    Panel5D = panelnd.create_nd_panel_factory(
                                      klass_name   = 'Panel5D',
                                      orders  = [ 'graphs', 'samplers','experiments','queries','features'],
                                      slices  = { 'samplers' : 'labels', 'experiments' : 'items', 'queries' : 'major_axis', 'features' : 'minor_axis' },
                                      slicer       = Panel4D,
                                      aliases = { 'major' : 'major_axis', 'minor' : 'minor_axis' },
                                      stat_axis    = 2)            
    return Panel5D.from_dict(dic)