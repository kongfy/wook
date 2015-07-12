# -*- coding: utf-8 -*-

from Base import BaseSolution

class IPDA(BaseSolution):
    def __init__(self):
        self.n = 0
        self.m = 0

    def calculateG(self, R, S, f):
        g = [[0] * self.m for i in xrange(self.n)]

        for j in xrange(self.m):
            if S[j] == 1:
                continue

            for i in xrange(self.n):
                # compute g_{ij} using given i & j
                temp = 0.0
                for k in xrange(self.n):
                    if k == i:
                        continue
                    temp += f[k][j]

                g[i][j] = temp / (self.n - 1)

        return g

    def knapsack(self, S, T, c, v):
        f = [0.0] * (T + 1)
        g = [[False] * (T + 1) for i in xrange(self.m)]

        for i in xrange(self.m):
            if S[i] == 1:
                continue
            for j in xrange(T, 0, -1):
                if j - c[i] < 0:
                    break
                if f[j - c[i]] + v[i] > f[j]:
                    f[j] = f[j - c[i]] + v[i]
                    g[i][j] = True

        res = [0] * self.m
        i = self.m - 1
        j = T

        while i >= 0 :
            if g[i][j] == True:
                res[i] = 1
                j -= c[i]
            i -= 1

        return res


    def calculateSs(self, R, S, T, t, g):
        Ss = [[]] * self.n

        for i in xrange(self.n):
            Ss[i] = self.knapsack(S, T[i], t[i], g[i])

        return Ss

    def solve(self, c, T, t, f):
        self.n = len(c)
        self.m = len(t[0])

        R = [0] * self.n
        S = [0] * self.m
        cost = 0

        while True:
            # step 1. compute g_ij
            g = self.calculateG(R, S, f)

            # step 2. compute S_i
            Ss = self.calculateSs(R, S, T, t, g)

            # step 3. compute e_i
            e = [0] * self.n
            for i in xrange(self.n):
                e[i] = sum([f[i][j] for j in xrange(self.m) if Ss[i][j] == 1]) + c[i]

            # step 4. choose route
            temp = None
            index = None
            for i in xrange(self.n):
                num = sum(Ss[i])
                if num == 0:
                    continue
                if temp == None or e[i] < temp:
                    temp = e[i]
                    index = i

            if index == None:
                raise Exception("Can not cover all device")

            # update
            cost += temp
            R[index] += 1
            for j in xrange(self.m):
                if Ss[index][j] == 1:
                    S[j] = 1

            # step 6
            if sum(S) == self.m:
                return cost
