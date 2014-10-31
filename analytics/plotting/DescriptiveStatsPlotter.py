'''
Created on Jul 15, 2013

@author: Emrah Cem{emrah.cem@utdallas.edu}
'''

from pandas import Series
import matplotlib.pyplot as plt
import math
import numpy as np
from matplotlib.pylab import subplot
import analytics
import sampling
from analytics.divergence.DistributionOperations import fill_gaps

__all__=['plot_pdf_cdf', 'plot_single_distribution','plot_multiple_distributions', 'compute_stats', "print_stats_on_the_plot",'save_pdf_plot_for_a_single_graph','save_pdf_cdf_plot_for_a_single_graph']
  
    
def compute_stats(distribution_dic):
    
    for key, value in distribution_dic.items():
        if value == 0:
            del distribution_dic[key]

    sum_val=  sum([k*v for k,v in distribution_dic.items() ]) 
    n=float(sum(distribution_dic.values()))
    xbar=sum_val/n
    xf=0
    m2=0
    m3=0
    m4=0
    for x,f in distribution_dic.items():
        xf=xf+x*f
        x_minus_xbar=x-xbar
        x_minus_xbar_2=x_minus_xbar*x_minus_xbar
        m2=m2+x_minus_xbar_2*f
        m3=m3+x_minus_xbar_2*x_minus_xbar*f
        m4=m4+x_minus_xbar_2*x_minus_xbar_2*f

    var=m2/n
    if var != 0:
        skew=(m3/n) / math.pow(m2/n,1.5)
        kurto=(m4/n) / math.pow(m2/n,2) -3
    else:
        skew=np.nan
        kurto=np.nan
    
    range_val= (min(distribution_dic.keys()), max(distribution_dic.keys()))
    
    normalized_distribution_dic={k:v/n for k,v in distribution_dic.items()}
    
    #Normalized Shannon Entropy (Sn) = S/ln(N). 
    #where N is the total number of the species.
    ent = 0.0
    norm_constant=0
    for freq in normalized_distribution_dic.values():
        if freq!=0:
            norm_constant=norm_constant+1
            ent = ent + freq * math.log(freq)
    ent = -ent
    
    ent=ent/math.log(norm_constant) if norm_constant !=1 else np.nan

    coef_of_var=math.sqrt(var)/math.fabs(xbar) if math.fabs(xbar) !=0 else np.nan

    return n, range_val, xbar, var, skew, kurto, ent, coef_of_var



def print_stats_on_the_plot(distribution, xy_pos=(0.6,0.55)):
    
    axis=plt.gca()
    
    left, width = .45, .5
    bottom, height = .45, .5
    right = left + width
    top = bottom + height

    size, min_max, mean_val, var, skew, kurto, ent, coef_of_var= compute_stats(distribution)

    result_str=""
    result_str+='range:['+str(min_max[0])+", "+str(min_max[1])+"]\n"
    result_str+='mean:'+'{0:.3f}'.format(mean_val)+"\n"
    result_str+='variance:'+'{0:.3f}'.format(var)+"\n"
    result_str+='skewness:'+'{0:.3f}'.format(skew)+"\n"
    result_str+='kurtosis:'+'{0:.3f}'.format(kurto)+"\n"
    result_str+='norm. entropy:'+'{0:.3f}'.format(ent)+"\n"
    result_str+='coeff. of var.:'+'{0:.3f}'.format(coef_of_var)
    
    props = dict(boxstyle='square', facecolor='white', alpha=0.9)
    
    #axis.text(xy_pos[0]+0.02,xy_pos[1]+0.02,result_str,transform=axis.transAxes, fontsize=10, bbox=props)
    t=axis.text(right,top,result_str,transform=axis.transAxes, fontsize='medium', horizontalalignment='right',
        verticalalignment='top',  bbox=props)
    
    bb = t.get_bbox_patch()
    bb.set_boxstyle("square", pad=0.7)
        
    return size, min_max, mean_val, var, skew, kurto, ent, coef_of_var
 
 
    
#Given the name of the feature and its distribution as a dict {x_11:y_11, x_12:y_12,... }, plots either PDF or CDF of the feature. 
def plot_single_distribution(normalized_distr, cdf=True, xlabel=None, title=None,  *args, **kwds):
    axis= plt.gca()
    if xlabel is not None:
        axis.set_xlabel(xlabel) 
    if title is not None:
        axis.set_title(title) 

    if not cdf and not analytics.isValidPDF(normalized_distr):
        raise sampling.InvalidProbabilityDensityException('Invalid probability density')
            
    axis.set_ylim(0,1)
    if cdf:
        axis.set_ylabel('CDF')
        if kwds.has_key('kind'):
            fill_gaps(normalized_distr, range(min(normalized_distr.keys()), max(normalized_distr.keys())), cdf=True)
        
        cdf=analytics.pdfTocdf(normalized_distr)
        if analytics.trim_cdf(cdf):
            Series(cdf,copy=True).plot(ax=axis, *args, **kwds)

    else:
        axis.set_ylabel('PDF')
        if kwds.has_key('kind'):
            fill_gaps(normalized_distr, range(min(normalized_distr.keys()), max(normalized_distr.keys())+1), cdf=False)
        if analytics.trim_pdf(normalized_distr):
            Series(normalized_distr,copy=True).plot(ax=axis, *args, **kwds)

    xmin, xmax = plt.xlim()
    axis.set_xlim(xmin-0.10*(xmax-xmin),xmax+0.05*(xmax-xmin))
  
  
    
#Given a dict in the form of {feature1: {x_11:y_11, x_12:y_12,... },  feature2: {x_21:y_21, x_22:y_22,... },...}, plots both PDF and CDF of each feature 
#along with the descriptive statistics such as range, mean , variance, skewness, kurtosis, entropy, and coefficient of variation.  
def plot_pdf_cdf(norm_distr_dict, single_figure_size=(6,4), stats=True,  *args, **kwds):
    num_of_features=len(norm_distr_dict)
    
    for i, (feature_name, distr) in enumerate(sorted(norm_distr_dict.items())):
        subplot(num_of_features,2,2*i+1)
        
        #plot_single_distribution(distr, cdf=False, xlabel=feature_name, xlim= (min(distr.keys()), max(distr.keys())), *args,**kwds)
        plot_single_distribution(distr, cdf=False, xlabel=feature_name, *args,**kwds)
        if stats:
            print_stats_on_the_plot(norm_distr_dict[feature_name])
           
        subplot(num_of_features,2,2*i+2)
        #plot_single_distribution(distr, cdf=True, xlabel=feature_name, xlim=(min(distr.keys()), max(distr.keys())), *args, **kwds) 
        plot_single_distribution(distr, cdf=True, xlabel=feature_name, *args, **kwds)
    
    
#Given {'feature_1': distr_dict_1, 'feature_2': distr_dict_2, ... }, plots either pdfs or cdfs based on argument "cdf".
def plot_multiple_distributions(norm_distr_dict, cdf=False, single_figure_size=(6,4), stats=True,  *args, **kwds):
    num_of_features=len(norm_distr_dict)
    
    for i, (feature_name, distr) in enumerate(sorted(norm_distr_dict.items())):
        subplot(1,num_of_features,i+1)
        
        plot_single_distribution(distr, cdf=cdf, xlabel=feature_name, xlim= (min(distr.keys()), max(distr.keys())), *args,**kwds)
        if stats:
            print_stats_on_the_plot(norm_distr_dict[feature_name])

#Given {'feature_1': distr_dict_1, 'feature_2': distr_dict_2, ... }, saves the plots for both pdfs and cdfs.
def save_pdf_cdf_plot_for_a_single_graph(feature_dic, title=None, statistics_included=True, file_name='descriptive_statistics.pdf', single_figure_size=(6,4), *args,**kwds):      
    fig= plt.figure()
    fig.set_size_inches(2*single_figure_size[0], len(feature_dic)*single_figure_size[1])
    plot_pdf_cdf(feature_dic, single_figure_size=single_figure_size, stats=statistics_included, grid=False, lw=2, *args,**kwds)
    if title is not None:
        fig.suptitle(title)
        #fig.suptitle('Characteristic Distribution and Descriptive Statistics in \n '+G.graph['name'], fontsize=16)
    plt.savefig(file_name)
    #dump(unnorm_distr_dic,open(G.graph['abbreviation']+"_unnormalized_distr_of_chars.pickle",'w'))
    #dump(feature_dic,open(G.graph['abbreviation']+"_normalized_distr_of_chars.pickle",'w'))

#Given {'feature_1': distr_dict_1, 'feature_2': distr_dict_2, ... }, saves the plots for either pdfs or cdfs based on argument "cdf".
def save_pdf_plot_for_a_single_graph(feature_dic, title=None, statistics_included=True, file_name='descriptive_statistics_pdf_only.pdf', single_figure_size=(6,4), *args,**kwds):      
    fig= plt.figure()
    fig.set_size_inches(len(feature_dic)*single_figure_size[0], single_figure_size[1])
    plot_multiple_distributions(feature_dic, single_figure_size=single_figure_size, stats=statistics_included, grid=False, lw=2, *args,**kwds)
    if title is not None:
        fig.suptitle(title)
        #fig.suptitle('Characteristic Distribution and Descriptive Statistics in \n '+G.graph['name'], fontsize=16)
    plt.savefig(file_name , bbox_inches='tight')
        
if __name__ == "__main__":
    
    #===========================================================================
    res={'feature1':{1:0.4,3:0.1,4:0.1,5:0.1,6:0.1,200:0.2}, 'feature2':{1:0.1,3:0.3,4:0.1,5:0.5}}
    #norm={1:0.2,3:0.2,4:0.2,5:0.2,6:0.1,7:0.1}
    #unnorm={1:2,3:2,4:2,5:2,6:1, 7:1}
    #===========================================================================
    
    save_pdf_cdf_plot_for_a_single_graph(res)
    #save_pdf_plot_for_a_single_graph(res, file_name='line.pdf', ls=':', marker='.')
    #save_pdf_cdf_plot_for_a_single_graph(res, file_name='bar.pdf')
    import matplotlib as mpl
    print mpl.__version__
