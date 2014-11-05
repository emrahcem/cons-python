cons-python
===========
This project aims to automate the process of analysis of graph sampling algorithms. The source code is modular and easily extensible. The input to the program is an xml file including information about the population graph, which can be generated synthetically or read from a file, graph characteristics, query(observation) types, and sampling algorithms as well as experiment parameters such as seed, number of samples, the output folder name.

Program creates several analysis file including the characteristic distribution (degree, clustering, path length) plots. A subfolder is created for each population graph (whose name is provided in the input xml file) to keep the analysis results. Inside this subfolder, a subfolder is created for each sampling method to keep the performance of the sampling algorithm. Analysis includes the computation of various distribution distance measures such as Kolmogorov-Smirnov, Jeffrey Divergence, Kullback-Leibler Divergence as well as the plots of distributions of graph characteristics in the sample graph.

More detailed information is coming soon...
