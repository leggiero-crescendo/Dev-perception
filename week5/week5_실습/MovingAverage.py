#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import deque
import numpy as np

class MovingAverage(object):
    def __init__(self, n):
        self.samples = n
        self.data = deque()
        self.weights = list(range(1, n+1))

    def add_sample(self, new_sample):
        if self.data and self.data[-1]*new_sample < 0:
            self.data = deque()
            self.data.append(new_sample)
        elif len(self.data) < self.samples:
            self.data.append(new_sample)
        else:
            self.data.popleft()
            self.data.append(new_sample)

    def get_mm(self):
        return float(sum(self.data)) / len(self.data)

    def get_wmm(self):
        total = 0
        length = 0
        for i, data in enumerate(self.data):
            total += (i+1) * data
            length += (i+1)
        vector = np.vectorize(np.float)
        total = vector(total)
        return total / length

    def get_emm(self):
        total = 0
        length = 0
        for i, data in enumerate(self.data):
            total += ((i+1)**2) * data
            length += (i+1)**2
        vector = np.vectorize(np.float)
        total = vector(total)
        return total / length