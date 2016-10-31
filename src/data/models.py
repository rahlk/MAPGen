from __future__ import division, print_function

import os
import sys

root = os.getcwd().split('src')[0] + 'src'
sys.path.append(root)
from utils.platypus.core import Problem
from utils.platypus.types import Real, Integer, Binary
from utils.platypus.algorithms import IBEA
from Models.skeleton import XOMO, POM3
from functools import partial
from pdb import set_trace


def _model_bare(x, model):
    """ 
    Generic model

    Note: To prevent redundancies, I pass one of the objectives (violations)
    and the objectives are computed using the dataframe called obj.
    """
    if isinstance(model, str):
        if model.lower() == 'xomo':
            model = XOMO()
        elif model.lower() == 'pom' or 'pom':
            model = POM3()

    try:
        return model.solve(x)
    except:
        return model.solve(x[:-model.n_obj])


def generator(model):
    if not isinstance(model, str):
        raise TypeError

    if model.lower() == 'xomo':
        mdl = XOMO()
    elif model.lower() == 'pom' or 'POM':
        mdl = POM3()
    problem = Problem(mdl.n_dec, mdl.n_obj)  # No. indp features, No. of objectives
    problem.indep = mdl.indep
    problem.depen = mdl.depen
    problem.name = model.lower()
    problem.types[:] = [Real(mdl.minMax[key].low, mdl.minMax[key].up) for key in
                        mdl.indep]
    problem.function = partial(_model_bare, model=mdl)
    return problem


def _test_generator():
    problem = generator(model="XOMO")
    algorithm = IBEA(problem)
    try:
        algorithm.run(100)
        print('Works!')
    except Exception as e:
        print("Test failed!\n")
        raise (e)
    # ----- DEBUG -----
    set_trace()


if __name__ == "__main__":
    _test_generator()
