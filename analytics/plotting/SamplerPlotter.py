'''
Created on Jul 31, 2013

@author: Emrah Cem{emrah.cem@utdallas.edu}
'''

from pandas import Series
import matplotlib.pyplot as plt

import analytics

__all__=['save_sampler_distribution','plot_sampler_distribution']


def save_sampler_distribution(panel, pop_dic=None, cdf=True, plot_each_exp=False, title=None , share_x=False, share_y=True, single_fig_size=(8,6), file_name='sampler_distribution.pdf', *args, **kwds):
    fig=plt.figure()
    fig.set_size_inches(single_fig_size[0]*len(panel.major_axis), single_fig_size[1]*len(panel.minor_axis))
    plot_sampler_distribution(panel, pop_dic=pop_dic, cdf=cdf, plot_each_exp=plot_each_exp, title=title , share_x=share_x, share_y=share_y, single_fig_size=single_fig_size, *args, **kwds)
    fig.savefig(file_name, bbox_inches='tight')
    
def plot_sampler_distribution(panel, pop_dic=None, cdf=True, plot_each_exp=False, title=None , share_x=False, share_y=True, single_fig_size=(8,6), *args, **kwds):
    
    if kwds.has_key('title'):
        plt.suptitle(kwds['title'], fontsize=16)

    shared_ax=None
    for i,feature in enumerate(panel.minor_axis):
        for j,(query,distribution) in enumerate(panel.minor_xs(feature).apply(analytics.Dict_operations.avg_list_of_dictionaries,axis=1).iteritems()): # row:query name , values= Series where each element is a distribution from a single experiment 
            if i+j==0:
                axes=plt.subplot(len(panel.minor_axis),len(panel.major_axis),i*len(panel.major_axis)+j+1)
                axes.set_ylim((0,1))
            else:
                axes=plt.subplot(len(panel.minor_axis),len(panel.major_axis),i*len(panel.major_axis)+j+1, sharey=shared_ax)
            
            #plot each experiment
            if plot_each_exp:
                for _,v in panel.minor_xs(feature).ix[query].iteritems(): 
                    if cdf:
                        if(analytics.trim_cdf(v)):
                            Series(v).cumsum().plot(ax=axes) 
                    else:
                        if(analytics.trim_pdf(v)):
                            Series(v).plot(ax=axes)
            
            #plot population distribution
            if pop_dic is not None and len(pop_dic)>0:
                analytics.plot_single_distribution(pop_dic[feature], cdf=cdf, xlabel=feature, title=query, label='population', color='g', lw=3)
            
            #plot average of all experiments
            if distribution is not None or len(distribution)>0:
                analytics.plot_single_distribution(distribution, cdf=cdf, xlabel=feature, title=query, label='sample(avg)', color='r', lw=3)
                analytics.print_stats_on_the_plot(distribution)
            
    plt.plot(*args,**kwds)
    plt.legend(loc = 'lower right')
    plt.ylim((0,1.01))
    if title is not None:
        plt.gcf().suptitle(title, fontsize=22, y=0.99)

if __name__ =='__main__':
    import pickle
    dic=pickle.load(open('/home/ecem/eclipse-repos/CONS_RESULTS/networks_synthetic/50000_nodes/30_exp_10percent/result_dic.pickle','r'))
    input_dic=dic['Barabasi-Albert']
    plot_sampler_distribution(input_dic['KK Path Sampling'], cdf=False, single_fig_size=(6,4))