#! /home/rahul/miniconda2/bin/python -B 
from __future__ import division, print_function

import os
import sys

root = os.getcwd().split('src')[0] + 'src'
if not root in sys.path: 
    sys.path.append(root)

import sugar.logo
from utils.platypus.algorithms import *
from data.models import generator
from pdb import set_trace
import pandas as pd
from datetime import datetime 

class Optimizer(object):
    def __init__(self, algorithm, problem, fname):
        super(Optimizer, self).__init__()
        self.algorithm = algorithm
        self.problem = problem
        
        # If save path doesn't exist, create one.
        if not os.path.exists(os.path.dirname(fname)): 
            os.makedirs(os.path.dirname(fname))
        
        self.optimized = self.algorithm(self.problem, saveLogs=True, skip=1, log_file=fname)
        self.optimized.run(10)

    def getParetoFrontier(self):
        try:
            return [solution.obj() for solution in self.optimized.result]
        except Exception as e:
            set_trace()

    def getConfigs(self):
        return [solution.values() for solution in self.optimized.result]


def _test_moco():
    for name in ['pom', 'xomo']:
        problem = generator(name)
        for method in [SPEA2, IBEA, NSGAII, NSGAIII, MOEAD]:
            fname = os.path.abspath("{}/logs/generations/{}/{}.csv".format(
                            root, 
                            problem.name,
                            method.__doc__))
            path = os.path.abspath('{0}/data/paretos/{1}/{2}.csv'.format(
                            root, name, method.__doc__))
            if not os.path.exists(os.path.dirname(path)): os.makedirs(os.path.dirname(path))    
            pareto = pd.DataFrame([result for result in Optimizer(
                    method, problem, fname).getParetoFrontier()])
            pareto.to_csv(path)

if __name__ == "__main__":
    _test_moco()
