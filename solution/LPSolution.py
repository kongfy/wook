# -*- coding: utf-8 -*-

from Base import BaseSolution
from pulp import *
from pprint import pprint

class LPSolution(BaseSolution):
    def __init__(self):
        self.n = 0
        self.m = 0

    def output(self, prob, x, y):
        print '<================ LPSolution ==================>'
        print("Status:", LpStatus[prob.status])
        pprint([[v.varValue for v in t] for t in x])
        pprint([v.varValue for v in y])

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
            prob += T[i] * y[i] - lpSum([t[i][j] * x[i][j] for j in xrange(self.m)]) >= 0

        prob.solve()

        self.output(prob, x, y)

        return value(prob.objective)
