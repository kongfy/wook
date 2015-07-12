# -*- coding: utf-8 -*-

from pprint import pprint
from generator import generate

import solution.LPSolution
import solution.SCA
import solution.ISCA
import solution2.LPSolution
import solution2.PDA
import solution2.IPDA

def worker():
    c, T, t, f = generate()

    solvers1 = [solution.LPSolution.LPSolution(),
                solution.SCA.SCA(),
                solution.ISCA.ISCA()]


    solvers2 = [solution2.LPSolution.LPSolution(),
                solution2.PDA.PDA(),
                solution2.IPDA.IPDA()]

    return [[solver.solve(c, T, t, f) for solver in solvers1], [solver.solve(c, T, t, f) for solver in solvers2]]

def main():
    result = worker()
    print result

if __name__ == '__main__':
    main()
