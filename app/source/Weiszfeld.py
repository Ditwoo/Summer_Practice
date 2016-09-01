from scipy.spatial import distance
import numpy as np
from source.Algo import Pilota, Vardi


class Weiszfeld(Pilota):

    def solve(self, x_0, epsilon=1e-5):
        before_x = x_0
        next_x = self._T(before_x)
        self.x = [before_x, next_x]

        while distance.euclidean(next_x, before_x) >= epsilon:
            tmp = next_x
            next_x = self._T(before_x)
            before_x = tmp

            self.x.append(next_x)


class ProjectedWeiszfeld(Pilota):
    l = []
    u = []

    def __init__(self, points, weights, l, u):
        super().__init__(points, weights)
        self.l = l
        self.u = u

    def _P(self, point):
        ans = point

        for i in range(len(point)):
            if point[i] < self.l[i]:
                ans[i] = self.l[i]
            if point[i] > self.u[i]:
                ans[i] = self.u[i]

        return ans

    def solve(self, x_0, epsilon=1e-5):
        before_x = x_0
        next_x = self._T(x_0)

        self.x = [before_x, next_x]

        while distance.euclidean(next_x, before_x) >= epsilon:
            tmp = next_x
            next_x = self._P(self._T(before_x))
            before_x = tmp
            self.x.append(next_x)


class ModifiedWeiszfeld(Vardi):

    def _T_0(self, y):
        for x in self.p:
            if np.array_equal(y, x):
                return x

        return self._tilde_T(y)

    def solve(self, x_0, epsilon):
        self.x = [x_0, self._T_0(x_0)]

        while not distance.euclidean(self.x[-1], self.x[-2]) < epsilon:
            self.x.append(self._T_0(self.x[-1]))


class NewAlgorithm(Vardi):

    def _tilde_R(self, y):
        ans = np.zeros(len(y))
        for i in range(len(self.p)):
            if not np.array_equal(self.p[i], y):
                ans = ans + (self.p[i] - y) * self.w[i] / distance.euclidean(self.p[i], y)
        return ans

    def _r(self, y):
        return distance.euclidean(0, self._tilde_R(y))

    def _eta(self, y):
        for k in range(len(self.p)):
            if np.array_equal(y, self.p[k]):
                return self.w[k]

        return 0

    def _new_tilde_T(self, y):
        tmp = self._eta(y) / self._r(y)
        return max(0, 1 - tmp) * self._tilde_T(y) + min(1, tmp) * y

    def solve(self, x_0, epsilon):
        self.x = [x_0, self._new_tilde_T(x_0)]

        while not distance.euclidean(self.x[-1], self.x[-2]) < epsilon:
            self.x.append(self._new_tilde_T(self.x[-1]))
