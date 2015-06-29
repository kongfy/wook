# -*- coding: utf-8 -*-

from Base import BaseSolution
from pulp import *

class LPSolution(BaseSolution):
    def __init__(self):
        self.n = 0
        self.m = 0

    def solve(self, c, T, t, f):
        self.n = len(c)
        self.m = len(t[0])

        prob = LpProblem('opt', LpMinimize)

        y = [LpVariable('y_' + str(i), lowBound=0) for i in xrange(self.n)]
        x = [[LpVariable('x_' + str(i) + '_' + str(j), lowBound=0) for j in xrange(self.m)] for i in xrange(self.n)]

        # optimize target (4a)
        prob += lpSum([c[i] * y[i] for i in xrange(self.n)] + [f[i][j] * x[i][j] for i in xrange(self.n) for j in xrange(self.m)])

        # 4b
        for j in xrange(self.m):
            prob += lpSum([x[i][j] for i in xrange(self.n)]) >= 1.0

        # 4c
        for i in xrange(self.n):
            for j in xrange(self.m):
                prob += y[i] - x[i][j] >= 0.0

        # 4d
        for i in xrange(self.n):
            prob += lpSum([t[i][j] * x[i][j] for j in xrange(self.m)]) <= T[i] * y[i]

        prob.solve()

        print '#======= LP solution =======#'
        print("Status:", LpStatus[prob.status])

        for v in prob.variables():
            print v.name, '=', v.varValue

        return value(prob.objective)
