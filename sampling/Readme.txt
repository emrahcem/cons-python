    graph_list                      = [#BarabasiAlbertGraphGenerator(population_size,1),
                                       #WattsStrogatzGraphGenerator(population_size,int(population_size/16.0),0.5),
                                       #ErdosRenyiGraphGenerator(population_size,0.001)
                                       ]

=====TO-DO's=======
For path length computation (in graph_feature_to_list.py), try to use "yield" keyword get the (value,hist) pair 
for each node in S, then combine the (value, hist) pairs without keeping each path length in memory. This will 
save a lot of space.


=======ASK========
For clustering coeff, I discritized the values, but the resulting values are sensitive to the number of bins?
What do you suggest to do in this case? Is there a better way to do it?

For watts-strogatz, taking the k parameter as population_size/16 + log(population_size)/16, creates a very dense 
graph with average degree 625 in a population size 10000. This creates a problem in the calculation of clustering
coefficient. We can decrease the value both to create a more realistic graph and to speed the calculations.
