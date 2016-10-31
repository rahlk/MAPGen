"""
XTREE
"""
from __future__ import print_function, division
import pandas as pd, numpy as np
from pdb import set_trace
import sys
import os
root = os.getcwd().split('src')[0]+'src'
sys.path.append(root)
from utils.XTREE.tools.sk import *
from utils.XTREE.tools.misc import *
from utils.XTREE.tools.oracle import *
import utils.XTREE.tools.pyC45 as pyC45


def trueValue(all,test):
  set_trace()

def flatten(x):
  """
  Takes an N times nested list of list like [[a,b],[c, [d, e]],[f]]
  and returns a single list [a,b,c,d,e,f]
  """
  result = []
  for el in x:
    if hasattr(el, "__iter__") and not isinstance(el, basestring):
      result.extend(flatten(el))
    else:
      result.append(el)
  return result


class changes():
  """
  Record changes.
  """
  def __init__(self):
    self.log = {}

  def save(self, name=None, old=None, new=None):
    if not old == new:
      self.log.update({name: (old-new)/old*100})

class patches:

  def __init__(i,train,test,trainDF,testDF,tree):
    i.train=train
    i.trainDF = trainDF
    i.test=test
    i.testDF=testDF
    i.tree=tree
    i.change =[]

  def leaves(i, node):
    """
    Returns all terminal nodes.
    """
    L = []
    if len(node.kids) > 1:
      for l in node.kids:
        L.extend(i.leaves(l))
      return L
    elif len(node.kids) == 1:
      return [node.kids]
    else:
      return [node]

  def find(i, testInst, t):
    if len(t.kids)==0:
      return t
    for kid in t.kids:
        if kid.val[0]==testInst[kid.f].values[0]:
          return i.find(testInst,kid)
    return t

  @staticmethod
  def howfar(me, other):
    common = [a for a in me.branch if a not in other.branch]
    return len(me.branch)-len(common)

  @staticmethod
  def loss(me, other):
    N = len(me)
    loss = sum([-np.exp(a-b)/N for a,b in zip(me, other)])/N
    return loss

  def patchIt(i,testInst):
    # 1. Find where t falls
    C = changes() # Record changes
    testInst = pd.DataFrame(testInst).transpose()
    current = i.find(testInst, i.tree)
    node = current

    while node.lvl > -1:
      node = node.up  # Move to tree root

    leaves = flatten([i.leaves(_k) for _k in node.kids])
    try:
        best = sorted([l for l in leaves], key=lambda F: i.loss(current,F))[0]
    except:
      return testInst.values.tolist()[0]


    for ii in best.branch:
      if not ii in current.branch:
        then = testInst[ii[0]].values[0]
        now = ii[1]
        testInst[ii[0]] = now
        C.save(name=ii[0], old=then, new=now)

    i.change.append(C.log)
    return testInst.values.tolist()[0][:-5]


  def main(i):
      newRows = [i.patchIt(i.testDF.iloc[n]) for n in xrange(i.testDF.shape[0])]
      # if not justDeltas:
      return newRows
      # else:
      #   return i.testDF.columns[:-1], i.change

def xtree(train, test):
    """XTREE"""
    # set_trace()
    data = csv2DF(train[1], toBin=False)
    shuffle(data)
    train_DF, test_DF=data[:-100], data[-100:].reset_index(drop=True)
    tree = pyC45.dtree2(train_DF)
    patch = patches(train=train, test=test, trainDF=train_DF, testDF=test_DF, tree=tree)
    return patch.main()
    # set_trace()

if __name__ == '__main__':
  E = []
  for name in ['ant']:#, 'ivy', 'jedit', 'lucene', 'poi']:
    print("##", name)
    train, test = explore(dir='../Data/Jureczko/', name=name)
    aft = [name]
    for _ in xrange(10):
      aft.append(xtree(train, test))
    E.append(aft)
  rdivDemo(E)
