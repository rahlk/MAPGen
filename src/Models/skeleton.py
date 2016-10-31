from __future__ import division, print_function

from Models._model import *


class XOMO():
    "XOMO"

    def __init__(i, n_dec=None, n_obj=None):
        i.indep = i.indep = Xomo(model="all").names
        i.minMax = Xomo(model="all").collection
        i.depen = ['$>effort', '$>months', '$>defects', '$>risk']
        i.n_dec = len(i.indep)
        i.n_obj = len(i.depen)

    def generate(i, n):
        return xomod(n)[1]

    def solve(i, dec):
        row = {h: el for h, el in zip(i.indep, dec)}
        return howMuchEffort(row)

    def get_pareto(self):
        return None


class POM3():
    "POM3"

    def __init__(i):
        i.indep = Pom().names
        i.depen = ['$>cost', '$<completion', '$>idle']
        i.minMax = Pom().collection
        i.n_dec = len(i.indep)
        i.n_obj = len(i.depen)

    def generate(i, N):
        return pom3d(N)[1][0]

    def solve(i, dec):
        return pom3().simulate(dec)

    def get_pareto(i):
        return None


if __name__ == "__main__":
    pom = POM3()
    row = pom.generate(1)
    print(pom.solve(row))
