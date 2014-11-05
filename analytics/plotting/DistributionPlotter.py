'''
Created on Aug 6, 2013

@author: Emrah Cem{emrah.cem@utdallas.edu}
'''

__all__=['plot_distributions_for_all_graphs','plot_divergence_boxplot','plot_distributions_for_single_graph', \
         'plot_distribution_for_single_query_and_feature','plot_divergence_boxplot_as_inset_axes', \
         'save_distributions_for_single_graph']

import matplotlib.pyplot as plt
from matplotlib.transforms import BlendedGenericTransform
import pandas as pnd
import mpl_toolkits.axes_grid.inset_locator as ins_loc
import sampling.global_vars as global_vars
import analytics

#Given a dataframe with columns as sampling methods and rows are experiments , and a series of population distribution for each experiment,
#returns a dataframe of divergence scores
#
#                 DATAFRAME(samplers)                       SERIES(orig)                                     DATAFRAME
#  ---------------------------------------------------     --------------                  ---------------------------------------------------
# |         SMP_METHOD_1   SMP_METHOD_2  SMP_METHOD_M |   |              |                |         SMP_METHOD_1   SMP_METHOD_2  SMP_METHOD_M |
# |      0     {distr}       {distr}       {distr}    |   | 0    {distr} |                |      1   div_score      div_score     div_score   |
# |      1     {distr}       {distr}       {distr}    |   | 1    {distr} |                |      2   div_score      div_score     div_score   |                 
# |      .        .             .             .       | , | .      .     |    ====>       |      .        .             .             .       |
# |      .        .             .             .       |   | .      .     |                |      .        .             .             .       |
# |      n-1   {distr}       {distr}       {distr}    |   | n-1  {distr} |                |      n   div_score      div_score     div_score   |  
#  ---------------------------------------------------     --------------                  ---------------------------------------------------
# 
def distribution_to_divergence_score(samplers, orig, divergence):

    dic = {}
    for column in samplers.columns:
        l = []
        for index, dist in samplers[column].iteritems():
            if dist is not None:
                l.append(divergence.compute(orig[index], dist))
        
        if len(l) != 0:
            dic[column] = l
    
    df=pnd.DataFrame(dic)
    
    sampler_list=list(samplers.columns)
    sampler_list = sorted(sampler_list, key=lambda x:global_vars.SAMPLER_ORDER.get(x,100))
    df=df[sampler_list]
    return df

def plot_divergence_boxplot(samplers, orig, divergence, ax=None, *args, **kwds):
    
    if ax==None:
        ax=plt.gca()
    
    ax.set_ylim(-0.02,1.02)
    
    
    div_scores = distribution_to_divergence_score(samplers, orig, divergence) 
    div_scores.columns = [global_vars.SAMPLER_MAPPING[ss] for ss in sorted(list(samplers.columns), key=lambda x:global_vars.SAMPLER_ORDER.get(x,100))]
    
    div_scores.boxplot(ax=ax, *args, **kwds)
    
    ax.patch.set_alpha(0.5)

    for tick in ax.xaxis.get_major_ticks():
                tick.label.set_fontsize('xx-small') 
                tick.label.set_rotation(90)
                #tick.label.set_ha('right')
    for tick in ax.yaxis.get_major_ticks():
                tick.label.set_fontsize('xx-small') 
                #tick.label.set_ha('right')
     
def plot_divergence_boxplot_as_inset_axes(divergence, cdf, curr_axes, orig, samplers):
    box_plot_loc = 4 if cdf else 1
    bbox_anchor = (-.02, .12, 1, 1) if cdf else (-.02, -.09, 1, 1)
    in_axes = ins_loc.inset_axes(curr_axes, width="40%", # width = 40% of parent_bbox
        height="40%", # height : 40% of parent box
        loc=box_plot_loc, 
        bbox_to_anchor=bbox_anchor, 
        bbox_transform=curr_axes.transAxes, 
        borderpad=0)
    plot_divergence_boxplot(samplers, orig, divergence, ax=in_axes, notch=1, grid=False)
    return in_axes



def plot_distribution_for_single_query_and_feature(curr_axes, df, cdf=True):
    sampler_list = list(df.columns)
    sampler_list = sorted(sampler_list, key=lambda x:global_vars.SAMPLER_ORDER.get(x,100))
    
    for sampler in sampler_list:
        if cdf:
            series_to_plot = df[sampler].cumsum()
            s_dict = series_to_plot.to_dict()
            existing_x_values = list([key for (key, value) in s_dict.iteritems() if abs(1 - value) < 0.0000001])
            if len(existing_x_values) > 0:
                series_to_plot = pnd.Series(dict((key, value) for (key, value) in s_dict.iteritems() if key <= min(existing_x_values)))
        else:
            series_to_plot = df[sampler]
            s_dict = series_to_plot.to_dict()
            if len(s_dict) > 0:
                series_to_plot = pnd.Series(dict((key, value) for (key, value) in s_dict.iteritems() if key <= max(key for (key, value) in s_dict.iteritems() if value > 0) and key >= min(key for (key, value) in s_dict.iteritems() if value > 0)))
        series_to_plot = series_to_plot.dropna()

        if len(series_to_plot) > 0:
            series_to_plot.plot(ax=curr_axes, ylim=(-0.01, 1.01), legend=False, label=sampler, style=global_vars.LINE_STYLES[sampler], linewidth=global_vars.LINE_WIDTHS[sampler]) #series_to_plot.plot(ax=curr_axes, ylim=(-0.01,1.01), legend=False, label=sampler,  style=line_styles[sampler], linewidth=line_widths[sampler])            

def plot_distributions_for_single_graph(graph_dic, fig_title, divergence=None, cdf=True, single_fig_size=(6,4), plot_dims=None):
    data=analytics.create_graph_panel_from_dic(graph_dic)
    fig= plt.gcf()
    first_axes=0

    for i,feature in enumerate(data.features):
        for j,query in enumerate(data.queries):
            #if feature== 'clustering coefficient' and query == "Frontend Query":
            df=data.ix[:,:,query,feature].dropna(axis=1)
            temp_dic={}
            for column in df.columns:
                temp_dic[column]=analytics.avg_list_of_dictionaries(df[column].tolist())
            df=pnd.DataFrame.from_dict(temp_dic)
            #df=pnd.DataFrame.from_dict(dict([(sampler,dist) for sampler,dist in df.apply(analytics.avg_list_of_dictionaries,axis=0).iteritems()]))
            
            if plot_dims==None or plot_dims[0]*plot_dims[1] != len(data.features)*len(data.queries): 
                #fig.set_size_inches(len(data.features)*len(data.queries)*single_fig_size[0], single_fig_size[1])
                curr_axes=plt.subplot(1, len(data.features)*len(data.queries) , 1 + j + len(data.queries)*i)
            else:
                curr_axes=plt.subplot(plot_dims[0],plot_dims[1], 1 + j + len(data.queries)*i)

            plot_distribution_for_single_query_and_feature(curr_axes, df, cdf=cdf)
            curr_axes.set_xlabel(feature + '(' + query+ ')')    
            curr_axes.grid(b=False, linewidth=0)
            
            
            if plot_dims is not None:
                if (1 + j + len(data.queries)*i) % plot_dims[1] == 1 or plot_dims[1]==1:
                    curr_axes.set_ylabel('CDF' if cdf else 'PDF')
                else:
                    curr_axes.set_yticklabels([])
            else:
                curr_axes.set_ylabel('CDF' if cdf else 'PDF')
           
            
            curr_axes.title.set_fontsize('small')
            curr_axes.tick_params(axis='both', which='major', labelsize=14)
 
     
            if i+j==0:
                first_axes=curr_axes   
            
            
            #################BOXPLOT###################
            if divergence is not None and 'Original' in data.samplers: 
                sampler_list=list(data.ix[:,:,query,feature].columns)
                sampler_list.remove('Original')
                orig=data.ix['Original',:,query,feature]
                samplers=data.ix[sampler_list,:,query,feature]
                 
                in_axes=plot_divergence_boxplot_as_inset_axes(divergence, cdf, curr_axes, orig, samplers)
                 
                if i+j==0:
                    in_axes.set_title(divergence().abbreviation, fontsize='small')
                else:
                    in_axes.set_yticklabels(())
                    
                sampler_list.insert(0,'Original')
            ##################END BOXPLOT################
        plt.draw()
    title=first_axes.text(0.5,1.6, fig_title, fontsize='xx-large', ha='center', va='top', transform=BlendedGenericTransform(fig.transFigure, first_axes.transAxes))      
    handles, labels= curr_axes.get_legend_handles_labels()
    leg=fig.legend(handles, labels, ncol=3, columnspacing=1, mode='extend', fancybox=True, handlelength=3, title='Sampling Methods', borderaxespad=1,  bbox_transform =  BlendedGenericTransform(fig.transFigure, first_axes.transAxes), loc ='upper center', fontsize='x-small', bbox_to_anchor=(0,0.5,1,1))
    leg.get_title().set_color("red")
    leg.get_frame().set_edgecolor('black')
    return title,leg
    
def save_distributions_for_single_graph(graph_dic, fig_title, divergence=None, cdf= True, single_fig_size=(6,4), plot_dims=None, file_name='distribution.pdf'):
    fig= plt.figure()
    fig.set_size_inches(single_fig_size[0]*plot_dims[1],single_fig_size[1]*plot_dims[0])
    fig.subplots_adjust(top=0.8)
    title,leg=plot_distributions_for_single_graph(graph_dic, fig_title, divergence=divergence, cdf=cdf, single_fig_size=single_fig_size, plot_dims=plot_dims)
    fig.savefig(file_name, bbox_inches='tight', bbox_extra_artists=(title,leg))
    
def plot_distributions_for_all_graphs(dic, fig_title, divergence=None, cdf=True, single_fig_size=(6,4), file_name='distribution_for_all_graphs.pdf'):

    data= analytics.create_5D_panel_from_dic(dic)

    fig=plt.figure() 
    w=len(data.graphs)
    h=len(data.features)*len(data.queries)
    
    fig.set_size_inches(single_fig_size[0]*w,single_fig_size[1]*h)
    fig.subplots_adjust(hspace=0.4)
    for i,feature in enumerate(data.features):
        for j,query in enumerate(data.queries):
            for k,graph in enumerate(data.graphs):
                df=data.ix[graph,:,:,query,feature].dropna(axis=1)
                
                df=pnd.DataFrame.from_dict(dict([(sampler,dist) for sampler,dist in df.apply(analytics.Dict_operations.avg_list_of_dictionaries,axis=0).iteritems()]))
                
                curr_axes=plt.subplot(len(data.features)*len(data.queries), len(data.graphs), 1 + k + len(data.graphs)*j + len(data.graphs)*len(data.queries)*i)
                
                curr_axes.grid(b=False, linewidth=0)
                
                if k==0:
                    curr_axes.set_ylabel('CDF' if cdf else 'PDF')
                else:
                    curr_axes.set_yticklabels([])
                
                
                plot_distribution_for_single_query_and_feature(curr_axes, df, cdf=cdf)
                
                curr_axes.set_title(global_vars.GRAPH_MAPPING.get(graph,graph)+'('+query+')')
                curr_axes.set_xlabel(feature)
                curr_axes.title.set_fontsize(14)
                
                
                #################BOXPLOT###################
                if divergence is not None and 'Original' in data.samplers: 
                    sampler_list=list(data.ix[graph,:,:,query,feature].columns)
                    sampler_list.remove('Original')
                    orig=data.ix[graph,'Original',:,query,feature]
                    samplers=data.ix[graph,sampler_list,:,query,feature]
                     
                    in_axes=plot_divergence_boxplot_as_inset_axes(divergence, cdf, curr_axes, orig, samplers)
                     
                    if i+j==0:
                        in_axes.set_title(divergence().abbreviation, fontsize='small')
                    else:
                        in_axes.set_yticklabels(())

                    sampler_list.insert(0,'Original')
                ##################END BOXPLOT################
        
    handles, labels= curr_axes.get_legend_handles_labels()
    leg=fig.legend(handles, labels, ncol=3, columnspacing=1, mode='extend', shadow=True, fancybox=True, handlelength=3, title='Sampling Methods', borderaxespad=1, loc ='upper center', fontsize=14, bbox_transform=fig.transFigure, bbox_to_anchor=(0,-0.02,1,1))
    leg.get_title().set_color("red")
    leg.get_frame().set_edgecolor('black')
    sup_title=fig.suptitle(fig_title, fontsize=22, y=0.99)
    fig.savefig(file_name, bbox_inches='tight', bbox_extra_artists=(leg,sup_title))  
 
if __name__ =='__main__':
    import pickle
    dic=pickle.load(open('/home/ecem/eclipse-repos/CONS_RESULTS/networks_synthetic/50000_nodes/30_exp_10percent/result_dic.pickle','r'))

#############Plot distributions for a single graph (e.g., Watts-Strogatz graph)################################################################################
#                                                                                                                                                             #
    input_dic=dic['Watts-Strogatz']                                                                                                                          #
    save_distributions_for_single_graph(input_dic, 'Test Title', analytics.DivergenceMetrics.JensenShannonDivergence, single_fig_size=(6,4), plot_dims=(3,2))#
#                                                                                                                                                             #
###############################################################################################################################################################

    
#############Plot distributions for all graphs#################################################################################################################
#                                                                                                                                                             #
#    plot_distributions_for_all_graphs(dic, fig_title='Test title', divergence=analytics.DivergenceMetrics.JensenShannonDivergence, single_fig_size=(6,4))    #
#                                                                                                                                                             #
###############################################################################################################################################################
    

######Plot only degree distribution with frontend query#######################################################################################################
#
#     data=analytics.create_graph_panel_from_dic(input_dic)
#     fig=plt.figure()
#     df=data.ix[:,:,'Frontend Query',"degree"].dropna(axis=1)
#     df=pnd.DataFrame.from_dict(dict([(sampler,dist) for sampler,dist in df.apply(smp.avg_list_of_dictionaries,axis=0).iteritems()]))
#     plot_distribution_for_single_query_and_feature(plt.gca(), df, cdf=True)
#
#     handles, labels= plt.gca().get_legend_handles_labels()
#     title=plt.gca().text(0.5,1.3, "TITLE", fontsize='xx-large', ha='center', va='top', transform=BlendedGenericTransform(fig.transFigure, plt.gca().transAxes))
#     leg=fig.legend(handles, labels, ncol=3, columnspacing=1, mode='extend', fancybox=True, handlelength=3, title='Sampling Methods', borderaxespad=1,  bbox_transform =  BlendedGenericTransform(fig.transFigure, plt.gca().transAxes), loc ='upper center', fontsize='x-small', bbox_to_anchor=(0,0.5,1,0.75))
#     fig.savefig("degree_frontend.pdf", bbox_inches='tight', bbox_extra_artists=(title,leg))
#
##############################################################################################################################################################