cons-python
===========
This project aims to automate the process of analysis of graph sampling algorithms. The source code is modular and easily extensible. The input to the program is an xml file including information about the population graph, which can be generated synthetically or read from a file, graph characteristics, query(observation) types, and sampling algorithms as well as experiment parameters such as seed, number of samples, the output folder name.

Program creates several analysis file including the characteristic distribution (degree, clustering, path length) plots. A subfolder is created for each population graph (whose name is provided in the input xml file) to keep the analysis results. Inside this subfolder, a subfolder is created for each sampling method to keep the performance of the sampling algorithm. Analysis includes the computation of various distribution distance measures such as Kolmogorov-Smirnov, Jeffrey Divergence, Kullback-Leibler Divergence as well as the plots of distributions of graph characteristics in the sample graph. Please see [this](example/) for example input file and analysis results. 

#####Requirements
===================
* python 2.7
* networkx (>= 1.7)
* scipy (>= 0.13.3)
* numpy (>= 1.9.0)
* matplotlib (>= 1.3.1)
* pandas (>= 0.14.1)
* igraph (>=0.7)

I suggest installing anaconda which is a completely free Python distribution. It includes 195+ of the most popular Python packages for science, math, engineering, data analysis.
Anaconda will install all required packages except igraph. You should install it separately.

More detailed information is coming soon...
