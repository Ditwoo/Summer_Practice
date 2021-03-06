import random
import numpy as np
import math
from scipy.spatial import ConvexHull
import copy


class ENorm:
    @staticmethod
    def norm(point):
        ans = 0.
        for item in point:
            ans += item * item
        return math.sqrt(ans)

    @staticmethod
    def norm_in_2(point):
        ans = 0.
        for item in point:
            ans += item * item
        return ans

    @staticmethod
    def normalize(point):
        n = 0.
        for item in point:
            n += item * item
        return point / n

    @staticmethod
    def is_in_hull(point, hpoints):
        hull_points = copy.copy(hpoints)
        hull_points.append(point)
        hull_points = np.array(hull_points)

        hull = ConvexHull(hull_points)
        print(' * Created convex hull.')

        for i in hull.vertices:
            if np.array_equal(point, hull_points[i]):
                return True

        return False

    @staticmethod
    def is_in_eps_neighborhood(point1, point2=None, eps=1e-5):
        ans = 0.
        if point2 is None:
            for i in point1:
                ans += math.fabs(i)
            return True if ans <= eps else False

        for i in range(len(point1)):
            ans += math.fabs(point1[i] - point2[i])
        return True if ans <= eps else False


class PManager:
    @staticmethod
    def parse_point(point):
        return [point[0]], [point[1]], [point[2]]

    @staticmethod
    def parse_points(points):
        x = [elem[0] for elem in points]
        y = [elem[1] for elem in points]
        z = [elem[2] for elem in points]
        return x, y, z

    @staticmethod
    def read_points(file, dimensions=0, separator='|'):
        points = []
        weights = []

        with open(file, 'r') as data:
            for line in data:
                words = line.split(separator)
                numbers = words[0][:-1].split(' ')
                if dimensions > 0:
                    points.append(np.array([float(numbers[i]) for i in range(dimensions)]))
                else:
                    points.append(np.array([float(numb) for numb in numbers]))

                weights.append(int(words[1]))

        return np.array(points), np.array(weights)

    @staticmethod
    def norm(point):
        return point / math.sqrt(np.dot(point, point))

    # @staticmethod
    # def save_points(points, file):
    #     figure = plt.figure(figsize=(6, 6))
    #     ax = figure.gca(projection='3d')
    #
    #     x, y, z = PManager.parse_points(points)
    #     ax.plot(x, y, z, 'g.', alpha=0.6)
    #
    #     ax.set_xlabel('x axis')
    #     ax.set_ylabel('y axis')
    #     ax.set_zlabel('z axis')
    #     figure.suptitle('Points')
    #     plt.savefig(file, dpi=100)


class PGenerator:
    @staticmethod
    def gen_point_on_a_sphere(R=1):
        phi = random.uniform(0, 2 * math.pi)
        costheta = random.uniform(-1, 1)
        u = random.uniform(0, 1)

        theta = math.acos(costheta)
        r = R * math.sqrt(u)

        x = r * math.sin(theta) * math.cos(phi)
        y = r * math.sin(theta) * math.sin(phi)
        z = r * math.cos(theta)

        return np.array([x, y, z])

    @staticmethod
    def gen_random_point(dim, lower, upper):
        return [random.uniform(lower, upper) for i in range(dim)]

    @staticmethod
    def gen_random_points(dimension):
        from scipy.spatial import ConvexHull
        count = random.randint(100, 1000)
        points = np.random.rand(count, dimension)  # points from [0;1)
        hull = ConvexHull(points)
        points = [np.array(points[index]) for index in hull.vertices]
        weights = np.array([random.randint(1, 1000) for i in range(count)])

        return points, weights


# class PPloter:
#     @staticmethod
#     def get_surface(point, surf, border, step=0.025):
#         if surf == 'x':
#             y = np.arange(border[0], border[1], step)
#             stp = (border[3] - border[2]) / len(y)
#             z = np.arange(border[2], border[3], stp)
#             y, z = np.meshgrid(y, z)
#             x = np.ones(len(y)) * point[0]
#             return x, y, z
#
#         if surf == 'y':
#             x = np.arange(border[0], border[1], step)
#             stp = (border[3] - border[2]) / len(x)
#             z = np.arange(border[2], border[3], stp)
#             x, z = np.meshgrid(x, z)
#             y = np.ones(len(x)) * point[1]
#             return x, y, z
#
#         if surf == 'z':
#             x = np.arange(border[0], border[1], step)
#             stp = (border[3] - border[2]) / len(x)
#             y = np.arange(border[2], border[3], stp)
#             x, y = np.meshgrid(x, y)
#             z = np.ones(len(x)) * point[2]
#             return x, y, z
#
#     @staticmethod
#     def save_plot(points, steps, file, title):
#         figure = plt.figure(figsize=(6, 6))
#         ax = figure.gca(projection='3d')
#
#         x, y, z = PManager.parse_points(points)
#         ax.plot(x, y, z, 'g.', alpha=0.6)
#
#         x, y, z = PManager.parse_points(steps)
#         ax.plot(x, y, z, 'r.', alpha=0.6)
#
#         ax.set_xlabel('x axis')
#         ax.set_ylabel('y axis')
#         ax.set_zlabel('z axis')
#         figure.suptitle(title)
#         ax.legend(['points', 'steps'])
#
#         plt.savefig(file, dpi=100)
#
#     @staticmethod
#     def save_plot_with_borders(points, steps, l, u, file, title='Projected Weiszfeld'):
#         figure = plt.figure(figsize=(6, 6))
#         ax = figure.gca(projection='3d')
#
#         x, y, z = PManager.parse_points(points)
#         ax.plot(x, y, z, 'g.', alpha=0.6)
#
#         x, y, z = PManager.parse_points(steps)
#         ax.plot(x, y, z, 'r.', alpha=0.6)
#
#         # borders
#         srf_alpha = 0.05
#         x, y, z = get_surface(u, 'x', (l[1], u[1], l[2], u[2]))
#         ax.plot_surface(x, y, z, color='b', alpha=srf_alpha)
#
#         x, y, z = get_surface(u, 'y', (l[0], u[0], l[2], u[2]))
#         ax.plot_surface(x, y, z, color='b', alpha=srf_alpha)
#
#         x, y, z = get_surface(u, 'z', (l[0], u[0], l[1], u[1]))
#         ax.plot_surface(x, y, z, color='b', alpha=srf_alpha)
#
#         x, y, z = get_surface(l, 'x', (l[1], u[1], l[2], u[2]))
#         ax.plot_surface(x, y, z, color='b', alpha=srf_alpha)
#
#         x, y, z = get_surface(l, 'y', (l[0], u[0], l[2], u[2]))
#         ax.plot_surface(x, y, z, color='b', alpha=srf_alpha)
#
#         x, y, z = get_surface(l, 'z', (l[0], u[0], l[1], u[1]))
#         ax.plot_surface(x, y, z, color='b', alpha=srf_alpha)
#
#         ax.set_xlabel('x axis')
#         ax.set_ylabel('y axis')
#         ax.set_zlabel('z axis')
#         figure.suptitle(title)
#         ax.legend(['points', 'steps'])
#
#         plt.savefig(file, dpi=100)
