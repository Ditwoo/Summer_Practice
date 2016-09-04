import numpy as np
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D

import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

from source.Utils import PManager


class PlotWindow(tk.Frame):
    def __init__(self, parent,
                 method,
                 points, steps=None,
                 l=None, u=None,
                 figure_size=(6, 6)):
        tk.Frame.__init__(self, parent)

        fig = Figure(figsize=figure_size, dpi=100)
        canvas = FigureCanvasTkAgg(fig, self)  # must be before ax (for rotating plot)
        ax = fig.add_subplot(111, projection='3d')

        x, y, z = PManager.parse_points(points)
        ax.plot(x, y, z, 'g.', alpha=0.6)

        if steps is not None:
            x, y, z = PManager.parse_points(steps)
            ax.plot(x, y, z, 'r.', alpha=0.6)

        if 'Projected Weiszfeld' in method:
            if l is None or u is None:
                raise Warning('l or u is None')
            else:
                srf_alpha = 0.05
                try:
                    x, y, z = PlotWindow._get_surface(u, 'x', (l[1], u[1], l[2], u[2]))
                    ax.plot_surface(x, y, z, color='b', alpha=srf_alpha)

                    x, y, z = PlotWindow._get_surface(u, 'y', (l[0], u[0], l[2], u[2]))
                    ax.plot_surface(x, y, z, color='b', alpha=srf_alpha)

                    x, y, z = PlotWindow._get_surface(u, 'z', (l[0], u[0], l[1], u[1]))
                    ax.plot_surface(x, y, z, color='b', alpha=srf_alpha)

                    x, y, z = PlotWindow._get_surface(l, 'x', (l[1], u[1], l[2], u[2]))
                    ax.plot_surface(x, y, z, color='b', alpha=srf_alpha)

                    x, y, z = PlotWindow._get_surface(l, 'y', (l[0], u[0], l[2], u[2]))
                    ax.plot_surface(x, y, z, color='b', alpha=srf_alpha)

                    x, y, z = PlotWindow._get_surface(l, 'z', (l[0], u[0], l[1], u[1]))
                    ax.plot_surface(x, y, z, color='b', alpha=srf_alpha)
                except ValueError as er:
                    print(er)

        ax.set_xlabel('x axis')
        ax.set_ylabel('y axis')
        ax.set_zlabel('z axis')
        fig.suptitle(method)
        ax.legend(['points', 'steps'])

        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    @staticmethod
    def _surface_side(border, step=0.025):
        a = np.arange(border[0], border[1], step)
        stp = (border[3] - border[2]) / len(a)
        b = np.arange(border[2], border[3], stp)
        a, b = np.meshgrid(a, b)
        return a, b

    @staticmethod
    def _get_surface(point, surf, border, step=0.025):

        if surf == 'x':
            y, z = PlotWindow._surface_side(border, step)
            x = np.ones(len(y)) * point[0]
            return x, y, z

        if surf == 'y':
            x, z = PlotWindow._surface_side(border, step)
            y = np.ones(len(x)) * point[1]
            return x, y, z

        if surf == 'z':
            x, y = PlotWindow._surface_side(border, step)
            z = np.ones(len(x)) * point[2]
            return x, y, z
