import random
import numpy as np
from scipy.spatial import distance


class Algorithm:
    x = []

    def __init__(self, points, weights):
        self.p = points
        self.w = weights

    # x_0 must be np.array
    def solve(self, x_0, epsilon): pass


class Pilota(Algorithm):
    def _T(self, point):
        for i in range(len(self.p)):
            if np.array_equal(point, self.p[i]):
                return self.p[i]

        numerator = 0.
        denominator = 0.

        for i in range(len(self.p)):
            norm = distance.euclidean(point, self.p[i])

            numerator = numerator + self.w[i] * self.p[i] / norm
            denominator = denominator + self.w[i] / norm

        return numerator / denominator


class Vardi(Algorithm):
    def _w(self, i, y):
        ans = self.w[i] / distance.euclidean(y, self.p[i])
        coef = 0.
        for j in range(len(self.p)):
            if not np.array_equal(y, self.p[j]):
                coef = coef + self.w[j] / distance.euclidean(y, self.p[j])
        return ans / coef

    def _tilde_T(self, y):
        ans = 0.
        for i in range(len(self.p)):
            if not np.array_equal(y, self.p[i]):
                ans += self._w(i, y) * self.p[i]

        return ans
