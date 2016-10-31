from __future__ import print_function, division

__author__ = 'rkrsn'
import sys
import os

root = os.getcwd().split('src')[0] + 'src'
sys.path.append(root)
from Planners.xtree2 import xtree
from tools.misc import explore
from data.models import _model_bare
import pandas as pd


def main():
    e = []
    for name in ['xomo', 'pom']:
        print("##", name)
        # set_trace()
        data = explore(directory='Data/SE/', name=name)
        aft = xtree(train=data, test=None)
        new = pd.DataFrame([_model_bare(row, name) for row in aft])
        new.to_csv(os.path.abspath(
            '{0}/data/paretos/{1}/xtree.csv'.format(root, name)), index=False)


if __name__ == '__main__':
    main()
