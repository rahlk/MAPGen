#! /home/rahul/miniconda2/bin/python -B
from __future__ import print_function, division

import os
import sys

root = os.path.abspath(os.getcwd().split('src')[0] + 'src')
if root not in sys.path:
    sys.path.append(root)
from pdb import set_trace
from utils.XTREE.Planners.xtree2 import xtree
from utils.XTREE.tools.misc import explore
import pandas as pd

__author__ = 'rkrsn'


def csv2generations(dir=None):
    """convert raw pareto dumps to a proper dataframe to process."""
    if dir is None:
        dir = os.path.abspath()


def delve():
    for name in ['xomo', 'pom']:
        print("##", name)
        data = explore(
                dir=os.path.abspath(
                        "{}/logs/generations/{}/".format(root, name)))
        set_trace()
        aft = xtree(train=data, test=None)
        new = pd.DataFrame([_model_bare(row, name) for row in aft])
        new.to_csv(os.path.abspath(
                '{0}/data/paretos/{1}/xtree.csv'.format(root, name)),
                index=False)


if __name__ == '__main__':
    delve()
