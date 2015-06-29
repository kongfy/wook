# -*- coding: utf-8 -*-

"""
Generate input for all the algorithms
"""

from config import CFG
from random import randint
from math import sqrt, ceil

def generate():
    c = []
    T = []
    t = []

    n = CFG['N']
    m = CFG['M']
    E = CFG['E']
    P = CFG['P']
    a = CFG['a']
    b = CFG['b']

    for i in xrange(n):
        c.append(randint(*CFG['c']))
        T.append(randint(*CFG['T']))

        temp = []
        for j in xrange(m):
            bound = ceil(float(b ** 2 * E) / (a * P))
            l, r = CFG['t']
            l += bound
            r += bound
            temp.append(randint(l, r))

        t.append(temp)

    f = get_f_list(t)

    return (c, T, t, f)

def get_f_list(t):
    n = CFG['N']
    m = CFG['M']
    E = CFG['E']
    P = CFG['P']
    a = CFG['a']
    b = CFG['b']

    d = []
    for i in xrange(n):
        temp = []
        for j in xrange(m):
            temp.append(sqrt(float(t[i][j] * a * P) / E) - b)
        d.append(temp)

    f = []
    for i in xrange(n):
        temp = []
        for j in xrange(m):
            temp.append(((d[i][j] + b) ** 2 / a - 1) * E)

        f.append(temp)

    return f
