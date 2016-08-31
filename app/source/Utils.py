import random
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull


def gen_random_point(dim, lower, upper):
    return [random.uniform(lower, upper) for i in range(dim)]


def gen_random_points(dimension):
    count = random.randint(100, 1000)
    points = np.random.rand(count, dimension)  # points from [0;1)
    hull = ConvexHull(points)
    points = [np.array(points[index]) for index in hull.vertices]
    weights = np.array([random.randint(1, 1000) for i in range(count)])

    return points, weights


def parse_points(points):
    x = [elem[0] for elem in points]
    y = [elem[1] for elem in points]
    z = [elem[2] for elem in points]
    return x, y, z


def get_surface(point, surf, border, step=0.025):
    if surf == 'x':
        y = np.arange(border[0], border[1], step)
        stp = (border[3] - border[2]) / len(y)
        z = np.arange(border[2], border[3], stp)
        y, z = np.meshgrid(y, z)
        x = np.ones(len(y)) * point[0]
        return x, y, z

    if surf == 'y':
        x = np.arange(border[0], border[1], step)
        stp = (border[3] - border[2]) / len(x)
        z = np.arange(border[2], border[3], stp)
        x, z = np.meshgrid(x, z)
        y = np.ones(len(x)) * point[1]
        return x, y, z

    if surf == 'z':
        x = np.arange(border[0], border[1], step)
        stp = (border[3] - border[2]) / len(x)
        y = np.arange(border[2], border[3], stp)
        x, y = np.meshgrid(x, y)
        z = np.ones(len(x)) * point[2]
        return x, y, z


def save_points(points, file):
    figure = plt.figure(figsize=(6, 6))
    ax = figure.gca(projection='3d')

    x, y, z = parse_points(points)
    ax.plot(x, y, z, 'g.', alpha=0.6)

    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_zlabel('z axis')
    figure.suptitle('Points')
    plt.savefig(file, dpi=100)


def save_plot(points, steps, file, title):
    figure = plt.figure(figsize=(6, 6))
    ax = figure.gca(projection='3d')

    x, y, z = parse_points(points)
    ax.plot(x, y, z, 'g.', alpha=0.6)

    x, y, z = parse_points(steps)
    ax.plot(x, y, z, 'r.', alpha=0.6)

    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_zlabel('z axis')
    figure.suptitle(title)
    ax.legend(['points', 'steps'])

    plt.savefig(file, dpi=100)


def save_plot_with_borders(points, steps, l, u, file, title='Projected Weiszfeld'):
    figure = plt.figure(figsize=(6, 6))
    ax = figure.gca(projection='3d')

    x, y, z = parse_points(points)
    ax.plot(x, y, z, 'g.', alpha=0.6)

    x, y, z = parse_points(steps)
    ax.plot(x, y, z, 'r.', alpha=0.6)

    # borders
    srf_alpha = 0.05
    x, y, z = get_surface(u, 'x', (l[1], u[1], l[2], u[2]))
    ax.plot_surface(x, y, z, color='b', alpha=srf_alpha)

    x, y, z = get_surface(u, 'y', (l[0], u[0], l[2], u[2]))
    ax.plot_surface(x, y, z, color='b', alpha=srf_alpha)

    x, y, z = get_surface(u, 'z', (l[0], u[0], l[1], u[1]))
    ax.plot_surface(x, y, z, color='b', alpha=srf_alpha)

    x, y, z = get_surface(l, 'x', (l[1], u[1], l[2], u[2]))
    ax.plot_surface(x, y, z, color='b', alpha=srf_alpha)

    x, y, z = get_surface(l, 'y', (l[0], u[0], l[2], u[2]))
    ax.plot_surface(x, y, z, color='b', alpha=srf_alpha)

    x, y, z = get_surface(l, 'z', (l[0], u[0], l[1], u[1]))
    ax.plot_surface(x, y, z, color='b', alpha=srf_alpha)

    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_zlabel('z axis')
    figure.suptitle(title)
    ax.legend(['points', 'steps'])

    plt.savefig(file, dpi=100)


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
