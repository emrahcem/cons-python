import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import analytics
import pylab
import networkx as nx
from math import pow,log10
import sampling as smp
from pandas.core.series import Series

G=nx.barabasi_albert_graph(1000, 10, 1)
p=10*G.number_of_edges()*log10(G.number_of_nodes())/G.number_of_nodes() 
sampler=smp.MetropolisSubgraphSampler(100, analytics.DivergenceMetrics.JensenShannonDivergence, smp.SimpleGraphDegree(), 50000, p, 10,2)
best, div=sampler.sample(G)
#best, div=smp.metropolis_subgraph_sampler(G, 100, analytics.DivergenceMetrics.JensenShannonDivergence, smp.SimpleGraphDegree(), 50000, p, 10,2)
Series(div).plot()
plt.gca().set_ylabel('JS-Divergence')
plt.gca().set_xlabel('# of iterations')
nx.write_gml(G, "pop.gml")
plt.gcf().savefig('metropolis_algorithm.pdf')
pylab.show() 
