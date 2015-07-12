# -*- coding: utf-8 -*-

from pprint import pprint
from generator import generate

import solution.HeuristicSolution
import solution.LPSolution
import solution.HeuristicSolution2
import solution2.LPSolution
import solution2.PDBSolution
import solution2.HeuristicSolution

def worker():
    c, T, t, f = generate()

    solvers1 = [solution.LPSolution.LPSolution(),
                solution.HeuristicSolution2.HeuristicSolution2(),
                solution.HeuristicSolution.HeuristicSolution()]


    solvers2 = [solution2.LPSolution.LPSolution(),
                solution2.PDBSolution.PDBSolution(),
                solution2.HeuristicSolution.HeuristicSolution()]

    return [[solver.solve(c, T, t, f) for solver in solvers1], [solver.solve(c, T, t, f) for solver in solvers2]]

def main():
    result = worker()
    print result

if __name__ == '__main__':
    main()
