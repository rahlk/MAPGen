"""
"""
from __future__ import print_function, division

import os
from demo import *
import subprocess
import sys
sys.path.append(os.path.abspath('../problems/'))
# Get the git root directory
root=repo_dir = subprocess.Popen(['git'
                                      ,'rev-parse'
                                      , '--show-toplevel']
                                      , stdout=subprocess.PIPE
                                    ).communicate()[0].rstrip()

sys.path.append(root)
from pdb import set_trace
from models import XOMO, POM3
from functools import partial
from dtlz2 import DTLZ2
from multiprocessing import Pool, cpu_count
from random import shuffle, seed as rseed, randint as randi
import numpy as np
from time import time
from tools.quality import measure

def gale0(model=DTLZ2(n_dec=30,n_obj=3), new=[], pop=int(1e4), popcache=None):
  """
  Recursive FASTMAP clustering.
  """
  # timer = time()
  if len(new)==0 or not popcache:
    frontier = model.generate(pop)
  else:
    frontier=new
    shuffle(popcache)
    frontier.extend(popcache[:pop-len(new)])
  # print("Time 0: ", time()-timer)

  N = np.shape(frontier)[0]
  leaf = []
  norm = np.max(frontier, axis=0) - np.min(frontier, axis=0)

  def cdom(x, y, better=['less','less','less','less']):

    def loss1(i,x,y):
      return (x - y) if better[i] == 'less' else (y - x)

    def expLoss(i,x,y,n):
      return np.exp(loss1(i,x,y) / n)

    def loss(x, y):
      n      = min(len(x), len(y)) #lengths should be equal
      losses = [expLoss(i,xi,yi,n) for i, (xi, yi) in enumerate(zip(x,y))]
      return sum(losses)/n

    "x dominates y if it losses least"
    return loss(x,y) < loss(y,x)

  def distant(lst):
    R, C = np.shape(lst)
    farthest=lambda one,rest: sorted(rest, key=lambda F: aDist(F,one))[-1]
    one=lst[randi(0,R-1)]
    mid=farthest(one, lst)
    two=farthest(mid, lst)
    return one, two

  def mutate(lst,good,g=0.15):
    new=[]
    for l in lst:
        new.append([a+(b-a)*g for a,b in zip(l,good)])
    return new

  def aDist(one, two):
    return np.sqrt(np.sum((np.array(one)-np.array(two))**2))
  def recurse(dataset):
    R, C = np.shape(dataset) # No. of Rows and Col
    # Find the two most distance points.
    one, two = distant(dataset)
    # Project each case on
    def proj(test):
      a = aDist(one, test)
      b = aDist(two, test)
      c = aDist(one, two)
      return (a**2-b**2+c**2)/(2*c)

    if R<int(np.sqrt(N)):
      leaf.extend(dataset)
    else:
      half1 = cdom(model.solve(one), model.solve(two))
      if half1:
        _ = recurse(sorted(dataset,key=lambda F:proj(F))[:int(R/2)])
      else:
        _ = recurse(sorted(dataset,key=lambda F:proj(F))[int(R/2):])

  # timer = time()
  recurse(frontier)
  # print("Resurse time: ", time()-timer)
  timer = time()
  a,b=distant(leaf)
  # print("Time2: ", time()-timer)
  # timer = time()
  (good, bad) = (a,b) if cdom(model.solve(a), model.solve(b)) else (b,a)
  new=mutate(leaf,good,g=0.5)
  # print("Time3: ", time()-timer)
  return new

# def SMOTEish(pop, N=10):
#   new = pop
#   for _ in xrange(len(pop)*N-len(pop)):
#     (a,b,c) = tuple(np.random.choice(range(len(pop)), size=3, replace=False).tolist())
#     try: new.append([i+abs(np.random.random()*(j-k)) for i,j,k in zip(pop[a],pop[b],pop[c])])
#     except: set_trace()
#   return new

def gale1(iter=1000,pop=400,n_proc=2,model=DTLZ2(n_dec=30, n_obj=3), newpop=None):
  iter=max(iter, 10)
  #n_proc = int(1000.00/iter)
  if not newpop: newpop = model.generate(pop*10)
  new = gale0(model,new=[],pop=int(pop/n_proc), popcache=newpop)
  # timer = time()
  while iter>0:
    iter-=1
    new=gale0(model, new, pop=int(pop/n_proc), popcache=newpop)
  #print("Time per iter: ", time()-timer)
  return new

def gale2(pop):
  model = DTLZ2(n_dec=30,n_obj=3)
  # set_trace()
  return gale0(new=model.generate(pop))

def GALE2(n_proc=10,frontSize=100,iters=1000,model=DTLZ2(n_dec=30, n_obj=3)):
  """
  WHY do threads take more time than single processors?? FIX THIS!!!
  :param n_proc:
  :param frontSize:
  :param iters:
  :param model:
  :return:
  """
  t = time()
  collect=[]
  final = []
  popSize = [int(frontSize/n_proc)]*n_proc
  # initpop = [(model, model.generate(1000), 1000) for _ in xrange(n_proc)]
  p=Pool(processes=n_proc)
  collect.extend(p.map(gale2, popSize))
  for cc in collect: final.extend(cc)
  # set_trace()
  ret = gale0(model=DTLZ2(n_dec=30, n_obj=3),new=final,pop=len(final))
  print('Time Taken: ', time()-t)
  return ret

def GALE(n_proc,mdl,frontSize=1600,iters=100):
  collect=[]
  final = []
  # per = [int(iters/n_proc)]*n_proc
  per = [iters]*n_proc
  popSize = [int(frontSize/n_proc)]*n_proc
  p=Pool(processes=n_proc)

  if mdl=='POM':
    model=POM3()
  elif mdl=='XOMO':
    model=XOMO()
  else:
    model=DTLZ2(n_dec=30,n_obj=3)

  newpop = model.generate(4000)
  t = time()
  partial_gale1 = partial(gale1, n_proc=n_proc, pop=int(frontSize/n_proc), model=model, newpop=newpop)
  collect.extend(p.map(partial_gale1, per))
  for cc in collect: final.extend(cc)
  return time()-t

def runner(mdl):
  # init = dEvol(n_proc=1,mdl=mdl);
  timer = []
  for n in [1]+range(2,17,2):
    # print(n)
    time=GALE(n,mdl)
    timer.append(time)
  print("Runtimes: ", timer)
  print("Speed-up: ", [float("%0.2f"%(timer[0]/a)) for a in timer])
  
if __name__=="__main__":
  eval(cmd())
