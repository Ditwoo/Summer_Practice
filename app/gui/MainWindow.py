import random
import tkinter as tk
from os import getcwd
from tkinter import ttk
from tkinter.filedialog import askopenfilename

import numpy as np

from gui.PlotWindow import PlotWindow
from source import Weiszfeld, Utils


class MainWindow(ttk.Frame):
    _epsilon = 1e-5
    _methods = ('Weiszfeld',
                'Projected Weiszfeld',
                'Modified Weiszfeld',
                'New Algorithm')

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.points = []
        self.weights = []
        self.init_gui()

    def _first_load(self):
        # show started point
        self.start_point_frame.grid(row=5, column=0, rowspan=4)
        self._init_start_frame(parent=self.start_point_frame, dim=len(self.points[0]))

        sz = [int(it.get()) for it in self.size_entry]

        if sz[0] < 0 or sz[1] < 0:
            self.frame = PlotWindow(self.out_frame, 'Points', self.points, figure_size=(6, 6))
        else:
            self.frame = PlotWindow(self.out_frame, 'Points', self.points, figure_size=sz)
        self.frame.grid(column=0, row=0, sticky="nsew")
        self.frame.tkraise()

    def on_load_file(self):
        fname = askopenfilename(initialdir=getcwd(),
                                filetypes=(("Template files", "*.txt"),
                                           (".txt files", "*.txt"),
                                           ("All files", "*.*")))
        self.points, self.weights = Utils.read_points(fname)
        self._first_load()

    def on_random_test(self):
        dim = 3
        self.points, self.weights = Utils.gen_random_points(dim)
        self._first_load()

    def on_quit(self):
        self.quit()
        self.destroy()

    def on_run(self):
        if self.size_entry[0].get() is '' or self.size_entry[0].get() is '':
            return

        sz = [int(it.get()) for it in self.size_entry]

        if sz[0] < 0 or sz[1] < 0:
            return

        if len(self.points) == 0:
            self.status_lbl['text'] = 'There is no points'
            return

        if len(self.weights) == 0:
            self.weights = np.array([random.randint(1, 1e1) for i in range(len(self.points))])

        for entry in self.spoint:
            if '' is entry.get():
                self.status_lbl['text'] = 'There is no started point'
                return

        y_0 = np.array([float(entry.get()) for entry in self.spoint])

        curr_method = self.method.get()

        if curr_method == self._methods[0]:
            algo = Weiszfeld.Weiszfeld(self.points, self.weights)

        elif curr_method == self._methods[1]:
            l = [float(entry.get()) for entry in self.lpoint]
            u = [float(entry.get()) for entry in self.upoint]

            algo = Weiszfeld.ProjectedWeiszfeld(self.points, self.weights, l, u)

        elif curr_method == self._methods[2]:
            algo = Weiszfeld.ModifiedWeiszfeld(self.points, self.weights)

        else:
            algo = Weiszfeld.NewAlgorithm(self.points, self.weights)

        algo.solve(y_0, self._epsilon)
        self.status_lbl['text'] = str(algo.x[-1])

        if curr_method == self._methods[1]:
            # self.lu_lbl['text'] = str(algo.l) + '\n' + str(algo.u)
            self.frame = PlotWindow(self.out_frame, curr_method, self.points, algo.x, algo.l, algo.u,
                                    figure_size=sz)
        else:
            # self.lu_lbl['text'] = ''
            self.frame = PlotWindow(self.out_frame, curr_method, self.points, algo.x, figure_size=sz)

        self.frame.grid(column=0, row=0, sticky="nsew")
        self.frame.tkraise()

    def _init_file_menu(self, parent):
        self.filemenu = tk.Menu(parent, tearoff=0)
        self.filemenu.add_command(label='Random test', command=self.on_random_test)
        self.filemenu.add_command(label='Load from file', command=self.on_load_file)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Quit', command=self.on_quit)

        self.menubar.add_cascade(menu=self.filemenu, label='File')

    def _init_figure_size_params(self, parent):
        wlbl = ttk.Label(parent, text='Width: ')
        wlbl.grid(column=0, row=0)
        hlbl = ttk.Label(parent, text='Height: ')
        hlbl.grid(column=2, row=0)
        self.size_entry = []

        for i in range(1, 4, 2):
            entry = ttk.Entry(parent, width=5)
            entry.grid(column=i, row=0)
            entry.delete(0, tk.END)
            entry.insert(0, '6')

            self.size_entry.append(entry)

    def _init_start_frame(self, parent, dim):
        self.spoint = []
        self.lpoint = []
        self.upoint = []

        for i in range(dim):
            lbl = ttk.Label(parent, text='x{0}'.format(i + 1))
            lbl.grid(column=0, row=i)

            entry = ttk.Entry(parent, width=5)
            entry.grid(column=1, row=i)
            entry.delete(0, tk.END)
            entry.insert(0, '1')
            self.spoint.append(entry)

            lbl = ttk.Label(parent, text='l{0}'.format(i + 1))
            lbl.grid(column=2, row=i)

            entry = ttk.Entry(parent, width=5)
            entry.grid(column=3, row=i)
            entry.delete(0, tk.END)
            entry.insert(0, '-1')

            self.lpoint.append(entry)

            lbl = ttk.Label(parent, text='u{0}'.format(i + 1))
            lbl.grid(column=4, row=i)

            entry = ttk.Entry(parent, width=5)
            entry.grid(column=5, row=i)
            entry.delete(0, tk.END)
            entry.insert(0, '1')

            self.upoint.append(entry)

    def init_gui(self):
        self.root.title('Algorithmico')
        self.root.configure(background='black')
        self.root.resizable(width=False, height=False)  # not resizable window

        self.grid(column=0, row=0, sticky='nsew')

        # menu section
        self.menubar = tk.Menu(self.root)
        self._init_file_menu(self.menubar)

        self.root.config(menu=self.menubar)

        # methods section
        self.method = tk.StringVar(self)
        self.method.set(self._methods[0])

        self.metbox = tk.OptionMenu(self, self.method, *self._methods)
        self.metbox.config(width=20)
        self.metbox.grid(row=1, column=0)

        # run
        self.calc_button = ttk.Button(self, text='Run', command=self.on_run)
        self.calc_button.grid(row=2, column=0)

        # label for algorithm
        # self.lu_lbl = ttk.Label(self, text='')
        # self.lu_lbl.grid(column=0, row=3)

        # figure size
        self.size_frame = ttk.LabelFrame(self, text='Figure size')
        self.size_frame.grid(row=3, column=0)
        self._init_figure_size_params(self.size_frame)

        # started point
        self.start_point_frame = ttk.LabelFrame(self, text='Started point')

        # status
        self.status_frame = ttk.LabelFrame(self, text='Status:')
        self.status_frame.grid(row=4, column=0, sticky='nesw')
        self.status_lbl = ttk.Label(self.status_frame, text='OK')
        self.status_lbl.grid(column=0, row=0)

        # output section
        self.out_frame = ttk.LabelFrame(self, text='Output', width=600, height=600)
        self.out_frame.grid(row=1, column=1, columnspan=4, rowspan=8, sticky='nesw')

        # initialise all widgets
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)
