#!/usr/local/bin/python2.7
# encoding: utf-8
'''
sampling -- Sampling Algorithms

This is the main class to run the experiment

@author:     Emrah Cem(emrah.cem@utdallas.edu)
        
@copyright:  2013 The University of Texas at Dallas. All rights reserved.
        
@license:    license

@contact:    emrah.cem@utdallas.edu
@deffield    updated: Updated
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from sampling.experiment.Experiment import Experiment 
from sampling.experiment import ExperimentManager
from sampling.experiment.ExperimentLoader import XMLLoader 

__all__ = []
__version__ = 0.1
__date__ = '2013-11-13'
__updated__ = '2013-11-13'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''
    
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Emrah Cem on %s.
  Copyright 2013 The University of Texas at Dallas. All rights reserved.
  
  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0
  
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)        
        parser.add_argument('-c' , '--config-file', default='defaults.xml', dest="input_file")
        
        # Process arguments
        args = parser.parse_args()

        verbose = args.verbose
        input_file=args.input_file

        if verbose > 0:
            print("Verbose mode on")
          
        sys.path.append("~/eclipse-repos/CONS/")
        exp=Experiment()
        ExperimentManager.load_experiment(exp, XMLLoader(input_file))
        exp.run()
        
        #=======================================================================
        # import networkx as nx
        # import sampling as smp
        # import time
        # print 'creating graph'
        # t=time.time()
        # ng=nx.barabasi_albert_graph(10000,10,seed=1)
        # print 'created graph in ',time.time()-t,' sec'
        # print 'collecting sample'
        # t=time.time()
        # sampler=smp.RandomWalkSampler(5000,seed=1)
        # sg=sampler.sample(ng)
        # #print 'graph:',ng.adjacency_list()
        # #print 'sample:',sg.adjacency_list()
        # print 'collected sample' ,time.time()-t,' sec'
        # #points=random.sample(range(0,50000), 5000)
        # print 'computing'
        # t=time.time()
        # res=smp.FeatureComputer.compute_single_query(smp.SimpleGraphPathLength(),smp.FrontendQuery(ng))
        # print 'computed in ',time.time()-t,' sec'
        # print res
        #=======================================================================
        
#        manager.add_analyzer(exp, SamplerAnalyzer())
#        manager.add_analyzer(exp, DistributionPlotter())
#        manager.add_analyzer(exp, DivergencePlotter(DivergenceMetrics.JensenShannonDivergence))
#        manager.add_analyzer(exp, DivergencePlotter(DivergenceMetrics.KolmogorovSmirnovDistance))
#        manager.add_analyzer(exp, DivergencePlotter(DivergenceMetrics.KLDivergence))
               
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'sampling_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())