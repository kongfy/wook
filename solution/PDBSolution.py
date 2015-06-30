# -*- coding: utf-8 -*-

from Base import BaseSolution
from math import trunc
from pprint import pprint

class PDBSolution(BaseSolution):
    def __init__(self):
        self.n = 0
        self.m = 0

    def output(self, x, y):
        print '<================ PDBSolution ==================>'
        pprint(x)
        pprint(y)

    def cost(self, c, f, x, y):
        return sum([c[i] * y[i] for i in xrange(self.n)]) + sum([f[i][j] * x[i][j] for i in xrange(self.n) for j in xrange(self.m)])

    def solve(self, c, T, t, f):
        self.n = len(c)
        self.m = len(t[0])

        # alg1
        selected = [0] * self.n # 0-None 1-Temporarily 2-Finally
        covered = [0] * self.m
        covered_by = [0] * self.m # covering host
        edges = [[0] * self.m for i in xrange(self.n)]   # 0-None 1-Full 2-Positive
        alpha = [0] * self.m
        beta = [[0] * self.m for i in xrange(self.n)]

        limit_alpha = [[trunc(f[i][j] + float(9 * c[i] * t[i][j]) / (10 * T[i])) for j in xrange(self.m)] for i in xrange(self.n)]
        limit_beta = [trunc(float(c[i]) / 10) for i in xrange(self.n)]

        while sum(covered) != self.m:
            for j in xrange(self.m):
                # already covered, skip
                if covered[j]:
                    continue

                # increase alpha
                alpha[j] += 1

                for i in xrange(self.n):
                    if alpha[j] == limit_alpha[i][j]:
                        edges[i][j] = 1
                        if selected[i] == 1:
                            covered[j] = 1
                            covered_by[j] = i
                            break

                    elif edges[i][j] >= 1:
                        edges[i][j] = 2
                        beta[i][j] += 1

                        if sum(beta[i]) == limit_beta[i]:
                            selected[i] = 1
                            for k in xrange(self.m):
                                if covered[k] == 0 and edges[i][k] >= 1:
                                    covered[k] = 1
                                    covered_by[k] = i
                            break

        # alg2
        g = [[0] * self.n for i in xrange(self.n)]

        for i in xrange(self.n):
            for j in xrange(self.n):
                if i == j:
                    continue
                # induced by R_t
                if selected[i] != 1 or selected[j] != 1:
                    continue
                for k in xrange(self.m):
                    if edges[i][k] == 2 and edges[j][k] == 2:
                        g[i][j] = 1

        D = [False] * self.n
        color = [False] * self.n
        for i in xrange(self.n):
            # induced by R_t
            if selected[i] != 1:
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
                selected[i] = 2

        x = [[0] * self.m for i in xrange(self.n)]
        for j in xrange(self.m):
            flag = False
            for i in xrange(self.n):
                if selected[i] >= 1 and beta[i][j] > 0:
                    # case 1
                    if selected[i] == 2:
                        x[i][j] = 1
                        flag = True
                        break

            if not flag:
                k = covered_by[j]
                # case 2.1
                if D[k]:
                    x[k][j] = 1
                else:
                    for h in xrange(self.n):
                        if g[k][h] == 1 and D[h]:
                            x[h][j] = 1
                            break

        assert(sum([x[i][j] for i in xrange(self.n) for j in xrange(self.m)]) == self.m)

        self.output(x, y)

        return self.cost(c, f, x, y)
