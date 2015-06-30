# -*- coding: utf-8 -*-

from pprint import pprint
from generator import generate

import solution.HeuristicSolution
import solution.LPSolution
import solution.PDBSolution

def worker():
    c, T, t, f = generate()

    solvers = [solution.HeuristicSolution.HeuristicSolution(),
               solution.LPSolution.LPSolution(),
               solution.PDBSolution.PDBSolution(),
               ]

    return [solver.solve(c, T, t, f) for solver in solvers]

def main():
    print worker()

if __name__ == '__main__':
    main()
