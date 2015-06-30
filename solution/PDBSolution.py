# -*- coding: utf-8 -*-

from Base import BaseSolution
from math import trunc

class PDBSolution(BaseSolution):
    def __init__(self):
        self.n = 0
        self.m = 0
        self.selected = None
        self.covered = None
        self.edges = None
        self.alpha = None
        self.beta = None

    def cost(self, c, f, x, y):
        return sum([c[i] * y[i] for i in xrange(self.n)]) + sum([f[i][j] * x[i][j] for i in xrange(self.n) for j in xrange(self.m)])

    def solve(self, c, T, t, f):
        self.n = len(c)
        self.m = len(t[0])

        # alg1
        self.selected = [0] * self.n # 0-None 1-Temporarily 2-Finally
        self.covered = [0] * self.m
        self.covered_by = [0] * self.m # covering host
        self.edges = [[0] * self.m for i in xrange(self.n)]   # 0-None 1-Full 2-Positive
        self.alpha = [0] * self.m
        self.beta = [[0] * self.m for i in xrange(self.n)]

        limit_alpha = [[trunc(f[i][j] + float(9 * c[i] * t[i][j]) / (10 * T[i])) for j in xrange(self.m)] for i in xrange(self.n)]
        limit_beta = [trunc(float(c[i]) / 10) for i in xrange(self.n)]

        while sum(self.covered) != self.m:
            for j in xrange(self.m):
                # already covered, skip
                if self.covered[j]:
                    continue

                # increase alpha
                self.alpha[j] += 1

                for i in xrange(self.n):
                    if self.alpha[j] == limit_alpha[i][j]:
                        self.edges[i][j] = 1
                        if self.selected[i] == 1:
                            self.covered[j] = 1
                            self.covered_by[j] = i
                            break

                    elif self.edges[i][j] >= 1:
                        self.edges[i][j] = 2
                        self.beta[i][j] += 1

                        if sum(self.beta[i]) == limit_beta[i]:
                            self.selected[i] = 1
                            for k in xrange(self.m):
                                if self.covered[k] == 0 and self.edges[i][k] >= 1:
                                    self.covered[k] = 1
                                    self.covered_by[k] = i
                            break

        # alg2
        g = [[0] * self.n for i in xrange(self.n)]

        for i in xrange(self.n):
            for j in xrange(self.n):
                if i == j:
                    continue
                # induced by R_t
                if self.selected[i] != 1 or self.selected[j] != 1:
                    continue
                for k in xrange(self.m):
                    if self.edges[i][k] == 2 and self.edges[j][k] == 2:
                        g[i][j] = 1

        D = [False] * self.n
        color = [False] * self.n
        for i in xrange(self.n):
            # induced by R_t
            if self.selected[i] != 1:
                continue
            if not color[i]:
                color[i] = True
                D[i] = True
                for j in xrange(self.n):
                    if g[i][j] == 1:
                        color[j] = True

        y = [0] * self.n
        for i in xrange(self.n):
            if D[i]:
                y[i] = 1
                self.selected[i] = 2


        x = [[0] * self.m for i in xrange(self.n)]
        for j in xrange(self.m):
            flag = False
            for i in xrange(self.n):
                if self.selected[i] >= 1 and self.beta[i][j] > 0:
                    # case 1
                    if self.selected[i] == 2:
                        x[i][j] = 1
                        flag = True
                        break

            if not flag:
                k = self.covered_by[j]
                # case 2.1
                if D[k]:
                    x[k][j] = 1
                else:
                    for h in xrange(self.n):
                        if g[k][h] == 1:
                            assert(D[h])
                            x[h][j] = 1

        from pprint import pprint
        pprint(y)
        pprint(x)

        return self.cost(c, f, x, y)
