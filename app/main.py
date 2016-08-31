import tkinter as tk
import random
import numpy as np
from source import Weiszfeld, Utils
from gui.MainWindow import MainWindow


def some_pilota():
    a = Utils.read_points('data/strange_cube.txt', 3)
    w = np.array([random.randint(1, 1e1) for i in range(len(a))])

    y_0 = np.array([2, 2, 2])

    wsfd = Weiszfeld.Weiszfeld(a, w)
    wsfd.solve(y_0, 1e-10)
    print(wsfd.x[-1])

    prj_wsfd = Weiszfeld.ProjectedWeiszfeld(a, w,
                                            Utils.gen_random_point(len(a[0]), -5, 0),
                                            Utils.gen_random_point(len(a[0]), 0, 5))
    prj_wsfd.solve(y_0, 1e-10)
    print(prj_wsfd.x[-1], prj_wsfd.l, prj_wsfd.u)


def some_vardi():
    x = Utils.read_points('data/strange_cube.txt', 3)
    eta = np.array([random.randint(1, 1e1) for i in range(len(x))])

    y_0 = np.array([1.5, 1.5, 1.5])

    mwzfld = Weiszfeld.ModifiedWeiszfeld(x, eta)
    mwzfld.solve(y_0, 1e-10)
    print(mwzfld.x[-1])

    nalgo = Weiszfeld.NewAlgorithm(x, eta)
    nalgo.solve(y_0, 1e-10)
    print(nalgo.x[-1])


if __name__ == '__main__':
    # some_pilota()
    # some_vardi()

    root = tk.Tk()
    MainWindow(root)
    root.mainloop()
