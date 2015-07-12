# -*- coding: utf-8 -*-

from multiprocessing import Pool
import timeit
from pprint import pprint

from generator import generate
from config import CFG
import solution.LPSolution
import solution.SCA
import solution.ISCA
import solution2.LPSolution
import solution2.PDA
import solution2.IPDA

def worker():
    c, T, t, f = generate()
    s1 = []
    s2 = []

    tic = timeit.default_timer()
    anser = solution.LPSolution.LPSolution().solve(c, T, t, f)
    toc = timeit.default_timer()
    s1.append((toc - tic, anser))

    tic = timeit.default_timer()
    anser = solution.SCA.SCA().solve(c, T, t, f)
    toc = timeit.default_timer()
    s1.append((toc - tic, anser))

    tic = timeit.default_timer()
    anser = solution.ISCA.ISCA().solve(c, T, t, f)
    toc = timeit.default_timer()
    s1.append((toc - tic, anser))

    tic = timeit.default_timer()
    anser = solution2.LPSolution.LPSolution().solve(c, T, t, f)
    toc = timeit.default_timer()
    s2.append((toc - tic, anser))

    tic = timeit.default_timer()
    anser = solution2.PDA.PDA().solve(c, T, t, f)
    toc = timeit.default_timer()
    s2.append((toc - tic, anser))

    tic = timeit.default_timer()
    anser = solution2.IPDA.IPDA().solve(c, T, t, f)
    toc = timeit.default_timer()
    s2.append((toc - tic, anser))

    return [s1, s2]

def main():
    """main function."""
    pool = Pool(CFG['worker'])

    tasks = [pool.apply_async(worker) for i in xrange(CFG['times'])]

    pool.close()
    pool.join()

    results = [task.get() for task in tasks]

    result1 = [[0, float('inf'), 0], [0, float('inf'), 0], [0, float('inf'), 0]]
    result2 = [[0, float('inf'), 0], [0, float('inf'), 0], [0, float('inf'), 0]]

    for result in results:
        s1, s2 = result

        for i in xrange(3):
            result1[i][0] = max(result1[i][0], s1[i][1])
            result1[i][1] = min(result1[i][1], s1[i][1])
            result1[i][2] += s1[i][0]

            result2[i][0] = max(result2[i][0], s2[i][1])
            result2[i][1] = min(result2[i][1], s2[i][1])
            result2[i][2] += s2[i][0]

    for i in xrange(3):
        result1[i][2] /= CFG['times']
        result2[i][2] /= CFG['times']

    f = open('summary.txt', 'a')
    f.write('N=' + str(CFG['N']) + ', M=' + str(CFG['M']) + ': ' + str([result1, result2]) + '\n')
    f.close()

    result = worker()
    print result

if __name__ == '__main__':
    main()
