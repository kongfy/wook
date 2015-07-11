# -*- coding: utf-8 -*-

from Base import BaseSolution

class HeuristicSolution2(BaseSolution):
    def __init__(self):
        self.n = 0
        self.m = 0

    def knapsack(self, S, T, c):
        # greedy
        res = [0] * self.m

        total = 0
        while True:
            index = None
            temp = None
            for i in xrange(self.m):
                if S[i] == 1 or res[i] == 1:
                    continue

                if temp == None or c[i] < temp:
                    index = i
                    temp = c[i]

            if temp == None or total + temp > T:
                break
            res[index] = 1
            total += temp

        return res


    def calculateSs(self, R, S, T, t):
        Ss = [[]] * self.n

        for i in xrange(self.n):
            if R[i] == 1:
                continue

            Ss[i] = self.knapsack(S, T[i], t[i])

        return Ss

    def solve(self, c, T, t, f):
        self.n = len(c)
        self.m = len(t[0])

        R = [0] * self.n
        S = [0] * self.m
        cost = 0

        # at most N interation
        for i in xrange(self.n):
            # step 1. compute S_i
            Ss = self.calculateSs(R, S, T, t)

            # step 2. compute e_i
            e = [0] * self.n
            for i in xrange(self.n):
                if R[i] == 1:
                    continue
                e[i] = sum([f[i][j] for j in xrange(self.m) if Ss[i][j] == 1]) + c[i]

            # step 3. choose route
            temp = None
            index = None
            for i in xrange(self.n):
                if R[i] == 1:
                    continue

                amount = sum([Ss[i][j] for j in xrange(self.m)])
                if amount == 0:
                    continue

                value = e[i] / amount
                if temp == None or value < temp:
                    temp = e[i]
                    index = i

            # update
            cost += temp
            R[index] = 1
            for j in xrange(self.m):
                if Ss[index][j] == 1:
                    S[j] = 1

            # step 6
            if sum(S) == self.m:
                return cost


        print self.m, sum(S)
        if sum(S) != self.m:
            raise Exception("Can not cover all device")

        return cost
