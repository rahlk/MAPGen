from __future__ import print_function, division
import sys
# Update path
sys.path.append('..')
import pycosat as ps
from os import walk
from pdb import set_trace
import csv
import pandas as pd
import numpy as np
from time import time
from sugar.ascii import progress_bar


class SATsolver:
    "SAT Solver"
    def __init__(self, project, basedir='../data/'):
        self.project = project
        self.basedir = basedir
        self.dir = basedir+'raw/'

    def _getcnffile(self):
        """Locate DIMACS config file on disk"""
        loc = self.dir+self.project
        for a,_,c in walk(loc): pass
        files = [a+'/'+cc for cc in c]
        for f in files:
            if f.split('.')[-1]=='dimacs':
                return f
        raise IOError('Feature model ending with .dimacs not found.')

    def _getobjfile(self):
        """Locate objective file on disk"""
        loc = self.dir+self.project
        for a,_,c in walk(loc): pass
        files = [a+'/'+cc for cc in c]
        for f in files:
            if f.split('.')[-1]=='augment':
                return f
        raise IOError('Feature model ending with .augment not found.')

    def cnf2list(self):
        """Convert cnf format to a python list"""
        cnfaslist = []
        file = self._getcnffile()
        for line in open(file):
            if line.startswith('p'):
                self.features = int(line.split(' ')[-2])
                self.clauses  = int(line.split(' ')[-1])
            elif not line.startswith('c') or line.startswith('p'):
                cnfaslist.append([int(var) for var in line.split(' ')[:-1]])
        return cnfaslist[:-1]

    def obj2dframe(self):
        file = self._getobjfile()
        dframe = pd.read_csv(file, delimiter=' ')
        dframe.columns = ['Features', 'Cost', 'Used_Before', 'Defects']
        return dframe

    def solve(self):
        """"""
        cnf = self.cnf2list()
        return ps.itersolve(cnf)


    def violations(self, X):
        cnf = self.cnf2list()
        invalids = 0
        for constraint in cnf:
            violations = []
            for C in constraint:
                violations.append(C>0 != X[abs(C)-1]>0)
            invalids+= 0 if any(violations) else 1
        return invalids


    def valids_as_csv(self, verbose=True):
        """Save valid configurations to a CSV file"""
        print('Saving to csv:')
        sol = self.solve()
        obj = self.obj2dframe()
        with open(self.basedir+'processed/'+self.project+'.csv', 'w+') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=','
                , quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(range(1, self.features+1) +
                ['Violations', 'Richness', 'Cost', 'Used_Before', 'Defects'])
            for n, val in enumerate(sol):
                violations = self.violations(val)
                richness = sum([1 for xx in val if not xx])
                cost = np.sum([inst for idx, inst in enumerate(
                    obj['Cost'].values) if val[idx]>0])
                used_before = np.sum([inst for idx, inst in enumerate(
                    obj['Used_Before'].values) if val[idx]>0])
                defects = np.sum([inst for idx, inst in enumerate(
                    obj['Defects'].values) if val[idx]>0 and \
                    not obj['Used_Before'].values[idx]==0])
                csvwriter.writerow([int(v>0) for v in val]+[
                    violations, richness, cost, used_before, defects])
                if verbose:
                    progress_bar(now=n, N=2500, marker="+")
                if n>2500:
                    print('\nFile saved.')
                    break;


class RunSolver:
    """Run the SAT solver"""
    def __init__(self):
        pass
    @classmethod
    def toCSV(self, project='linux'):
        print('Feature Model: {0}'.format(project), end='\n------\n')
        ss = SATsolver(project)
        ss.valids_as_csv()

    @classmethod
    def save_all(self):
        for project in ["uClinux","fiasco","freebsd","ecos","linux"]:
            self.toCSV(project)


class _test:

    def __init__(i):
        pass

    @classmethod
    def solver(i):
        """ Test solve
        """
        print("Testing: "+SATsolver.__doc__+"\n.....")
        try:
            start = time()
            ss = SATsolver(project='uClinux')
            sol = ss.solve()
            stop = time() - start
            print("Testing solve. Test succeeded.")
            print("Time to run: %0.2f seconds\n"%(stop))

        except Exception as e:
            print("Test failed!\n")
            raise(e)

    @classmethod
    def writer(i):
        """ Test save to file
        """
        print("Testing: ", end='')
        try:
            print("Testing valid_as_csv", end='\n')
            start = time()
            ss = SATsolver(project='uClinux')
            ss.valids_as_csv()
            stop = time() - start
            print("Test succeeded.")
            print("Test runtime: %0.2f seconds\n"%(stop))

        except Exception as e:
            print("Test failed!\n")
            raise(e)

    @classmethod
    def violations(i):
        """ Test violations
        """
        print("Testing Violations")
        try:
            start = time()
            ss = SATsolver(project='uClinux')
            sol = ss.solve()

            for _ in xrange(10):
                new = sol.next()
                invalids = ss.violations(new)
                print("Invalids: {}.".format(invalids))

            stop = time() - start
            print("Test succeeded.")
            print("Test runtime: {} seconds.\n".format(stop))
        except Exception as e:
            print("Test failed!\n")
            print(e)

if __name__ == '__main__':
    RunSolver.save_all()

    # _test.violations()
    # _test.writer(writer)

    # # ----- DEBUG -----
    # set_trace()
