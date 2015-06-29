# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class BaseSolution(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def solve(self, c, T, t, f):
        pass
