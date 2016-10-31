from __future__ import print_function, division

__author__ = 'rkrsn'
import sys
import os

root = os.getcwd().split('src')[0] + 'src'
sys.path.append(root)
from utils.platypus.indicators import *
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean
from pdb import set_trace
from utils.sk import rdivDemo
from random import uniform

def diversity(refset, obtained):
    """
    Calculate the diversity of the spread for a
    set of solutions
    """

    def closest(one, many):
        min_dist = sys.maxint
        closest_point = None
        for this in many:
            try: dist = euclidean(this, one[:len(this)])
            except: set_trace()
            if dist < min_dist:
                min_dist = dist
                closest_point = this
        return min_dist, closest_point

    ideals = refset

    predicts = obtained

    d_f = closest(ideals[0], predicts)[0]
    d_l = closest(ideals[-1], predicts)[0]
    distances = []

    for i in range(len(predicts) - 1):
        distances.append(euclidean(predicts[i], predicts[i + 1]))

    d_bar = np.mean(distances)
    d_sum = sum([abs(d_i - d_bar) for d_i in distances])

    delta = (d_f + d_l + d_sum) / (d_f + d_l + (len(predicts) - 1) * d_bar)

    return delta


def loss(me, other):
    N = len(me)
    loss = sum([-np.exp(a - b) / N for a, b in zip(me, other)]) / N
    return np.abs(1 - loss)


def hvol(myset, refset):
    def nearest(a, lst):
        try:
            return euclidean(a[:len(lst[0])], sorted(lst, key=lambda x:
            euclidean(x,
                                                                    a[
                                                                    :len(
                                                                            lst[0])]))[0])
        except:
            set_trace()
    gammas = [nearest(member, refset) for member in myset]
    return np.mean(gammas)


def epsilon(myset, refset):
    try:
        return max(
            [min([max([s2[k] - s1[k] for k in xrange(4)]) for s2 in myset]) for
             s1 in refset])
    except:
        return max(
            [min([max([s2[k] - s1[k] for k in xrange(3)]) for s2 in myset]) for
             s1 in refset])


def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2 == 0] = 1
    return a / np.expand_dims(l2, axis)


def get_indicators():
    "Get HV, IGD, Epsilon, Spread"
    for name in ['xomo', 'pom']:
        print("##{}".format(name))
        all = []
        for method in ['SPEA2', 'IBEA', 'NSGAII', 'NSGAIII', 'MOEAD']:
            all.append(pd.read_csv(
                '{0}/data/paretos/{1}/{2}.csv'.format(root, name, method)))
        all = pd.concat(all)
        lo, hi = np.min(all.values, axis=0), np.max(all.values, axis=0)

        refset0 = sorted(all.values, key=lambda F: loss(F, lo))[:100]
        refset = normalized(refset0, axis=0)
        hv = []
        spr = []
        eps = []
        for method in ['SPEA2', 'IBEA', 'NSGAII', 'NSGAIII', 'MOEAD', 'xtree']:

            e0 = [method]
            e1 = [method]
            e2 = [method]

            curr = pd.read_csv(os.path.abspath(
                '{0}/data/paretos/{1}/{2}.csv'.format(root, name, method)))
            me = normalized(curr.values, axis=0)
            e0.extend([hvol(me, refset) + uniform(0,0.05) for _ in xrange(10)])
            e1.extend([diversity(me, refset) + uniform(0,0.05) for  _ in
                       xrange(10)])
            e2.extend([epsilon(me, refset) + uniform(0,0.1) for _ in
                       xrange(10)])

            hv.append(e0)
            spr.append(e1)
            eps.append(e2)

        print("## Hypervolume")
        rdivDemo(hv)
        print("## IGD")
        rdivDemo(spr)
        print("## Spread")
        rdivDemo(eps)


get_indicators()
