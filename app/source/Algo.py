import random
import numpy as np
from scipy.spatial import distance


class Algorithm:
    x = []

    def __init__(self, points, weights):
        self.points = points
        self.weights = weights

    def solve(self, x_0, epsilon): pass


class Pilota(Algorithm):
    def _T(self, point):
        for i in range(len(self.points)):
            if np.array_equal(point, self.points[i]):
                return self.points[i]

        numerator = 0.
        denominator = 0.

        for j in range(len(point)):
            norm = distance.euclidean(point, self.points[j])

            numerator = numerator + self.weights[j] * self.points[j] / norm
            denominator = denominator + self.weights[j] / norm

        return numerator / denominator


class Vardi(Algorithm):
    def _w(self, i, y):
        ans = self.weights[i] / distance.euclidean(y, self.points[i])
        coef = 0.
        for j in range(len(self.points)):
            if not np.array_equal(y, self.points[j]):
                coef = coef + self.weights[j] / distance.euclidean(y, self.points[j])
        return ans / coef

    def _tilde_T(self, y):
        ans = 0.
        for i in range(len(self.points)):
            if not np.array_equal(y, self.points[i]):
                ans += self._w(i, y) * self.points[i]

        return ans
