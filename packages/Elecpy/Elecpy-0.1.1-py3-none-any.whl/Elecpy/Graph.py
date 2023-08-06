"""
This module is used to draw the graph of circuit calculation result.
"""
import matplotlib.pyplot as pyplot
import matplotlib.patches as patches
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.widgets as widgets
import matplotlib.axes as axes
from math import *
import numpy as np
import tkinter as tk
import os
import copy
from threading import Timer
import Elecpy.GUIElements as gui_elements


class __SinglePhasor:
    """
    class: Phasor Graph, define some method of phasor, has no display method.
    """
    def __init__(self,
                 id,
                 value,
                 **kwargs):
        """
        method:
        :param id: id of phasor
        :param value: a + bj
        :param kwargs: Keyword argument, e.g.,
        name: name of the phasor, default equal to id of the phasor
        sta_crd: coordinate of start point, (x, y)
        sta_phasor_tmnl: sometimes, a phasor's start point(or origin) is other phasor's start or end, i.e.,
        (Phasor, 'sta') or (Phasor, 'end')
        zoom: zoom factor, zoom<1 represent zoom out, zoom>1 represent zoom in
        legend_crd: coordinate of the legend, i.e., (x, y)
        freq: frequency of the phasor, Hz, int
        """
        # id: id of phasor, it's fixed when the phasor is created
        self._id = id
        # value: a + bj
        self._value = value
        # source data of phasor
        # name: name of the phasor
        # sta_crd: start point's coordinate, None or (x, y)
        # end_crd: end point's coordinate, None or (x, y)
        # sta_phasor_tmnl: start point's phasor, None or (Phasor, tmnl), tmnl: 'sta', 'end'
        # zoom: zoom in or zoom out, default value is 1
        # legend_crd: coordinate of legend
        # freq: frequency, Hz
        self._source = {'name': id, 'sta_crd': (0, 0), 'sta_phasor_tmnl': None, 'zoom': 1.0, 'freq': 50}

        # set the parameters
        self._set_params(**kwargs)

    def _set_params(self,
                    **kwargs):
        """
        method: set params
        :param kwargs: Keyword arguments, e.g.,
        name,
        sta_crd,
        end_crd,
        sta_phasor_tmnl,
        zoom,
        freq
        :return: None
        """
        for key in self._source:
            if key == 'end_crd':
                kwargs['sta_crd'] = (kwargs[key][0] - self._source['value'].real,
                                     kwargs[key][1] - self._source['value'].imag)
            if key in kwargs:
                self._source[key] = kwargs[key]

    def set_name(self,
                 name):
        """
        method: set name
        :param name:
        :return: None
        """
        self._set_params(name=name)

    def set_sta_crd(self,
                    crd):
        """
        method: set start coordinate
        :param crd: start coordinate
        :return: None
        """
        self._set_params(sta_crd=crd)

    def set_sta_phasor_tmnl(self,
                            phasor,
                            tmnl):
        """
        method: set the phasor and its terminal in the start point
        :param phasor: SinglePhasor
        :param tmnl: terminal, 'sta', 'end'
        :return: None
        """
        self._set_params(sta_phasor_tmnl=(phasor, tmnl))

    def set_end_crd(self,
                    crd):
        """
        method: set the end coordinate
        :param crd:
        :return: None
        """
        self._set_params(end_crd=crd)

    def set_zoom(self,
                 zoom):
        """
        method: set the zoom factor
        :param zoom:
        :return: None
        """
        self._set_params(end_crd=zoom)

    def set_freq(self,
                 freq):
        """
        method: set frequency
        :param freq:
        :return:
        """
        self._set_params(freq=freq)

    def get_params(self):
        """
        method: get params
        :return:
        """
        return self._source

    def get_id(self):
        """
        method: get id of phasor
        :return: id
        """
        return self._id

    def get_rt_value(self,
                     angle=None,
                     time=None):
        """
        method: get the real time value
        :param angle: rotating angle, radian
        :param time: time, s
        :return: real-time value
        """
        if angle is None:
            if time is not None:
                angle = self._source['freq'] * 2 * pi * time
                return self._value * (cos(angle) + sin(angle) * 1j)
            else:
                return self._value
        else:
            return self._value * (cos(angle) + sin(angle) * 1j)

    def get_name(self):
        """
        method: get name of the phasor
        :return: name, str
        """
        return self._source['name']

    def get_sta_crd(self,
                    time=0.0):
        """
        method: get start coordinate
        :param time: time, second
        :return:
        """
        if self._source['sta_phasor_tmnl'] is not None:
            return self._source['sta_phasor_tmnl'][0].get_crd(tmnl=self._source['sta_phasor_tmnl'][1],
                                                              time=time)
        else:
            return self._source['sta_crd']

    def get_end_crd(self,
                    time=0.0):
        """
        method: get end coordinate
        :param time: time, second
        :return:
        """
        sta_crd = self.get_sta_crd(time=time)
        rt_value = self.get_rt_value(time=time)
        return (sta_crd[0] + self._source['zoom'] * rt_value.real,
                sta_crd[1] + self._source['zoom'] * rt_value.imag)

    def get_crd(self,
                tmnl,
                time=0.0):
        """
        method: get start or end coordinate
        :param tmnl: terminal of phasor: 'sta' or 'end'
        :param time: time, second
        :return:
        """
        if tmnl == 'sta':
            return self.get_sta_crd(time)
        elif tmnl == 'end':
            return self.get_end_crd(time)

    def get_sta_phasor(self):
        """
        method: get start phasor
        :return: start phasor or None
        """
        return self._source['sta_phasor_tmnl']

    def get_freq(self):
        """
        method: get frequency
        :return:
        """
        return self._source['freq']


class SinglePhasorDiagramTk(__SinglePhasor):
    """
    class: Phasor Diagram based on Tkinter
    """
    def __init__(self,
                 id,
                 value,
                 canvas,
                 **kwargs):
        """
        method:
        :param id: id of phasor
        :param value: a + bj
        :param canvas:
        :param kwargs: Keyword arguments, e.g.,
        name: phasor's name, default value is the same with id
        sta_crd: (x, y)
        sta_phasor_tmnl: (Phasor, 'sta'), (Phasor, 'end')
        zoom: zoom factor, zoom<1 represent zoom out, zoom>1 represent zoom in
        freq: frequency of the phasor, Hz, int

        legend_crd:
        fill:
        width:
        dash:
        """
        super().__init__(id=id,
                         value=value,
                         **kwargs)
        # update the source data
        self._source.update({'sta_crd': (500, 500), 'legend_crd': (500, 500), 'fill': None, 'width': None, 'dash': None})
        # tkinter canvas
        self.canvas = None
        # set the parameters
        self._set_params(canvas=canvas,
                         **kwargs)

    def _set_params(self,
                    canvas=None,
                    **kwargs):
        """
        method: get params
        :param canvas: tkinter canvas
        :param kwargs: Keyword arguments, e.g.,
        name: phasor's name, default value is the same with id
        sta_crd: (x, y)
        sta_phasor_tmnl: (Phasor, 'sta'), (Phasor, 'end')
        zoom: zoom factor, zoom<1 represent zoom out, zoom>1 represent zoom in
        freq: frequency of the phasor, Hz, int

        legend_crd:
        fill:
        width:
        dash:
        :return:
        """
        if canvas is not None:
            self.canvas = canvas
        super()._set_params(**kwargs)

    def disp_phasor(self,
                    canvas=None,
                    time=0.0):
        """
        method: display phasor diagram
        :param canvas: tkinter's canvas
        :param time: certain moment, unit is second, float
        :param kwargs: Keyword arguments,
        fill:
        width:
        arrow:
        arrowshape: (18, 21, 6)
        dash: (3, 5)
        :return:
        """
        # get the parameters
        sta_crd = self.get_sta_crd(time=time)
        end_crd = self.get_end_crd(time=time)

        line_option = {'fill': None,
                       'width': 2,
                       'arrow': tk.LAST,
                       'arrowshape': (18, 21, 6),
                       'dash': None}
        for key in line_option:
            if key in self._source:
                line_option[key] = self._source[key]
        line_option['tags'] = self.get_id()
        # create the line
        self.canvas.create_line(sta_crd[0],
                                sta_crd[1],
                                end_crd[0],
                                end_crd[1],
                                **line_option)

    def disp_legend(self,
                    legend_crd):
        """
        method: display legend
        :param legend_crd: coordinate of legend
        :return: None
        """
        line_option = {'fill': self._source['fill'],
                       'width': self._source['width'],
                       'dash': self._source['dash'],
                       'tags': self.get_id() + '-legend'}

        self.canvas.create_line(legend_crd[0] + 100,
                                legend_crd[1],
                                legend_crd[0] + 140,
                                legend_crd[1],
                                **line_option)
        text_option = {'text': self.get_name(),
                       'anchor': tk.W,
                       'fill': self._source['fill'],
                       'tag': self.get_id() + '-legend'}
        self.canvas.create_text(legend_crd[0] + 150,
                                legend_crd[1],
                                **text_option)

    def del_pha_dgm(self):
        """
        method: delete phasor diagram
        :return:
        """
        self.canvas.delete(self.get_id())

    def del_legend(self):
        """
        method: delete legend
        :return:
        """
        self.canvas.delete(self.get_id() + '-legend')


class PhasorsDiagramTk:
    """
    class: Phasors Diagram
    """
    def __init__(self,
                 canvas=None,
                 pha_data=None):
        """
        method: create a diagram with some phasors in it
        :param canvas: tkinter's canvas
        :param pha_data: phasors data,
        {'ph1': {'id': 'ph1', 'value': 10 + 10j, 'sta_crd': (500, 500), 'sta_pid_tmnl': None},
         'ph2': {'id': 'ph2', 'value': 10 + 10j, 'sta_crd': (500, 500), 'sta_pid_tmnl': ('ph1', 'end'))}}
        """
        # tkinter's canvas
        self.canvas = canvas
        # dict of a group of Phasor objects
        self.pha_objs = {}

        # build Phasor object
        self.add_phasors(pha_data=pha_data)

    def add_phasors(self,
                    pha_data=None):
        """
        method: add phasors
        :param pha_data: phasors data,
        {'ph1': {'id': 'ph1', 'value': 10 + 10j, 'sta_crd': (500, 500), 'sta_pid_tmnl': None},
         'ph2': {'id': 'ph2', 'value': 10 + 10j, 'sta_crd': (500, 500), 'sta_pid_tmnl': ('ph1', 'end'))}}
        :return: None
        """
        for key in pha_data:
            value = pha_data[key]['value']
            if 'id' in pha_data[key].keys():
                pha_data[key].pop('id')
            if 'value' in pha_data[key].keys():
                pha_data[key].pop('value')
            self.add_phasor(id=key,
                            value=value,
                            **pha_data[key])

    def add_phasor(self,
                   id,
                   value,
                   **kwargs):
        """
        method: add one Phasor object
        :param id: Phasor's id, str
        :param value: Phasor's value, complex, e.g., 1+1j
        :param kwargs: Keyword arguments
        name: phasor's name, default value is the same with id
        sta_crd: (x, y)
        sta_phasor_tmnl: (Phasor, 'sta'), (Phasor, 'end')
        zoom: zoom factor, zoom<1 represent zoom out, zoom>1 represent zoom in
        legend_crd: coordinate of the legend, e.g., (x, y)
        freq: frequency of the phasor, Hz, int

        legend_crd:
        fill:
        width:
        dash:
        :return: None
        """
        if 'sta_pid_tmnl' in kwargs:
            kwargs['sta_phasor_tmnl'] = (self.pha_objs[kwargs['sta_pid_tmnl'][0]], kwargs['sta_pid_tmnl'][1])

        self.pha_objs[id] = SinglePhasorDiagramTk(id=id,
                                                  value=value,
                                                  canvas=self.canvas,
                                                  **kwargs)

    def disp_phasors(self,
                     canvas=None,
                     time=0.0):
        """
        method: display all phasors' diagram
        :param canvas: tkinter's canvas
        :param time: moment, unit is second, float
        :return: None
        """
        if canvas is not None:
            self.canvas = canvas
        for key in self.pha_objs:
            self.pha_objs[key].disp_phasor(canvas,
                                           time=time)

    def disp_legends(self,
                     legend_crd):
        """
        method: display legends
        :param legend_crd: legend crd
        :return: None
        """
        for i, key in enumerate(self.pha_objs):
            self.pha_objs[key].disp_legend(legend_crd=(legend_crd[0], legend_crd[1] + 10 * i))

    def del_phasors(self):
        """
        method: delete phasors
        :return:
        """
        for key in self.pha_objs:
            self.pha_objs[key].del_pha_dgm()

    def del_legends(self):
        """
        method: delete legends
        :return:
        """
        for key in self.pha_objs:
            self.pha_objs[key].del_legend()

    def animation(self,
                  legend_crd,
                  speed=1.0):
        """
        method: animation
        :param legend_crd: legend crd, e.g., (500, 500)
        :param speed: speed of phasor's rotation
        :return: None
        """
        self.disp_phasors()
        self.disp_legends(legend_crd=legend_crd)
        i = 0

        def rota():
            nonlocal i
            i += 1
            self.del_phasors()
            self.disp_phasors(time=0.002 * i * speed)
            timer = Timer(0.002, rota)
            timer.start()

        rota()


class FigureOnTk:
    """
    class: Create a Matplotlib's Figure on Tkinter widget.
    """
    def __init__(self,
                 master,
                 figsize=None):
        """
        method: init Figure on tkinter
        :param master: tkinter widget, e.g., tkinter.frame
        :param figsize: figure size, [width, height]
        """
        # tkinter widget
        self.master = master
        # figsize
        if figsize is None:
            self.master.update()
            self.figsize = [self.master.winfo_width() / 200 - 0.05,
                            self.master.winfo_height() / 200 - 0.2]
        else:
            self.figsize = figsize
        # gridspec
        self.gridspec = None
        # FigureCanvas
        self.canvas = None
        # Figure object
        self.figure = None

        # build a figure
        self._build_figure()

    def _build_figure(self):
        """
        method: build a figure on tkinter's widget
        :return:
        """
        # create a Figure
        self.figure = pyplot.figure(figsize=self.figsize)
        # put the Figure on the tkinter widget
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.draw()
        # create a toolbar, put it on the canvas
        toolbar = NavigationToolbar2Tk(self.canvas, self.master)
        toolbar.update()
        toolbar.grid(row=0, column=0, sticky=tk.W)

        self.canvas.get_tk_widget().grid(row=1, column=0, sticky=tk.W)
        self.divide()

    def divide(self,
               nrows=1,
               ncols=1,
               **kwargs):
        """
        method: divide the figure to nrows x ncols
        :param nrows: Number of rows in grid
        :param ncols: Number of columns in grid
        :param kwargs: Keyword arguments are passed to class matplotlib.gridspec.GridSpec
        :return:
        """
        self.gridspec = self.figure.add_gridspec(nrows=nrows,
                                                 ncols=ncols,
                                                 **kwargs)

    def add_axes(self,
                 row=0,
                 col=0,
                 grid=None,
                 **kwargs):
        """
        method: add an Axes to the figure as part of a subplot arrangement
        :param row: row
        :param col: column
        :param grid: if there is grid, False
        :param kwargs: Keyword arguments, e.g.,
        xlim: x-axis' limitation, (float, float)
        ylim: y-axis' limitation, (float, float)
        label: Set a label that will be displayed in the legend.
        transparency: a float define the transparency, 0.0 - 1.0
        xlabel: label for the x-axis, str
        ylabel: label for the y-axis, str
        xscale: x-axis scale, "linear", "log", "symlog", "logit"
        yscale: y-axis scale, "linear", "log", "symlog", "logit"
        :return: axes
        """
        if 'xlabel' not in kwargs:
            kwargs['xlabel'] = 't/s'

        self.figure.add_subplot(self.gridspec[row, col],
                                **kwargs)
        if grid:
            pyplot.grid()

        self.canvas.draw_idle()

        return pyplot.gca()

    def add_pha_axes(self,
                     row=0,
                     col=0,
                     grid=None,
                     axis_visible=True,
                     **kwargs):
        """
        method: add a axes for phasor's diagram
        :param row:
        :param col:
        :param grid:
        :param axis_visible:
        :param kwargs: Keyword arguments, e.g.,
        xlim: x-axis' limitation, (float, float)
        ylim: y-axis' limitation, (float, float)
        label: Set a label that will be displayed in the legend.
        transparency: a float define the transparency, 0.0 - 1.0
        xlabel: label for the x-axis, str
        ylabel: label for the y-axis, str
        xscale: x-axis scale, "linear", "log", "symlog", "logit"
        yscale: y-axis scale, "linear", "log", "symlog", "logit"
        :return: axes
        :return: None
        """
        if 'xlabel' not in kwargs:
            kwargs['xlabel'] = '1'
        if 'ylabel' not in kwargs:
            kwargs['ylabel'] = 'j'
        """if 'xlim' not in kwargs:
            kwargs['xlim'] = [-30, 30]
        if 'ylim' not in kwargs:
            kwargs['ylim'] = [-30, 30]"""

        self.figure.add_subplot(self.gridspec[row, col],
                                **kwargs)

        axes = pyplot.gca()

        if grid:
            pyplot.grid()

        if axis_visible is True:
            axes.axis('scaled')
        else:
            axes.axis('off')

        self.canvas.draw_idle()

        return axes


class SinglePhasor(__SinglePhasor):
    """
    class: Single Phasor Graph, including phasor diagram and sine waveform, based on Matplotlib
    """
    def __init__(self,
                 id,
                 value,
                 axes=None,
                 **kwargs):
        """
        method:
        :param id: id of phasor
        :param value: a + bj
        :param axes: matplotlib.axes.Axes to draw phasor or sine waveform
        :param kwargs: Keyword arguments, passing to matplotlib.patches.FancyArrowPatches, e.g.,
        name: phasor's name, default value is the same with id
        sta_crd: (x, y)
        sta_phasor_tmnl: (Phasor, 'sta'), (Phasor, 'end')
        zoom: zoom factor, zoom<1 represent zoom out, zoom>1 represent zoom in
        freq: frequency of the phasor, Hz, int
        step_time: dt when plotting, e.g., 0.000001
        color:
        linestyle:
        linewidth:
        alpha:
        headlength:
        headwidth:
        tailwidth:
        """
        super().__init__(id=id,
                         value=value,
                         **kwargs)
        # update the source data
        self._source.update({'sta_crd': (0, 0),
                             'step_time': 0.0001,
                             'color': None,
                             'linestyle': None,
                             'linewidth': None,
                             'alpha': None,
                             'head_length': 6,
                             'head_width': 3,
                             'tail_width': 0.01})

        # matplotlib.axesAxes,
        self.axes = None
        # arrow of the phasor
        self.arrow = None
        # line of the phasor plot line
        self.line = None

        # set the parameters
        self._set_params(axes=axes,
                         **kwargs)

        # define the sin waveform's line, automatically getting the color.
        self.line, = self.axes.plot([], [],
                                    color=self._source['color'],
                                    linestyle=self._source['linestyle'],
                                    linewidth=self._source['linewidth'],
                                    alpha=self._source['alpha'],
                                    visible=False)
        # if user doesn't give the color of phasor, get the color automatically
        if self._source['color'] is None:
            self._source['color'] = self.line.get_c()

        # define the phasor's arrow
        sta_crd = self.get_sta_crd(time=0)
        end_crd = self.get_end_crd(time=0)
        self.arrow = patches.FancyArrowPatch(posA=(sta_crd[0], sta_crd[1]),
                                             posB=(end_crd[0], end_crd[1]),
                                             arrowstyle=patches.ArrowStyle("Fancy",
                                                                           head_length=self._source['head_length'],
                                                                           head_width=self._source['head_width'],
                                                                           tail_width=self._source['tail_width']),
                                             color=self._source['color'],
                                             linestyle=self._source['linestyle'],
                                             linewidth=self._source['linewidth'],
                                             alpha=self._source['alpha'],
                                             visible=False)
        self.axes.add_patch(self.arrow)

    def _set_params(self,
                    axes=None,
                    **kwargs):
        """
        method: get params
        :param axes: matplotlib.axes.Axes
        :param kwargs: Keyword arguments, passing to matplotlib.patches.FancyArrowPatches, e.g.,
        name,
        sta_crd,
        end_crd,
        sta_phasor_tmnl,
        zoom,
        freq
        color:
        linestyle:
        linewidth:
        alpha:
        headlength:
        headwidth:
        tailwidth:
        :return: None
        """
        if axes is not None:
            self.axes = axes

        super()._set_params(**kwargs)

    def get_appearance(self):
        """
        method: get the appearance, color, linestyle, linewidth, alpha
        :return: {color, linestyle, linewidth, alpha}
        """
        params = {}
        for key in ['color', 'linestyle', 'linewidth', 'alpha']:
            params[key] = self._source[key]
        return params

    def set_appearance(self,
                       **kwargs):
        """
        method: set appearance of the single phasor
        :param kwargs: keyword arguments, e.g.,
        color:
        linestyle:
        linewidth:
        alpha:
        :return:
        """
        self._set_params(**kwargs)
        if kwargs is None:
            return
        if 'color' in kwargs:
            self.line.set_color(kwargs['color'])
            self.arrow.set_color(kwargs['color'])
        if 'linestyle' in kwargs:
            self.line.set_linestyle(kwargs['linestyle'])
            self.arrow.set_linestyle(kwargs['linestyle'])
        if 'linewidth' in kwargs:
            self.line.set_linewidth(kwargs['linewidth'])
            self.arrow.set_linewidth(kwargs['linewidth'])

    def clear_phasor(self):
        """
        method: clear phasor
        :return:
        """
        self.arrow.set_visible(False)

    def disp_phasor(self,
                    time=0.0):
        """
        method: display phasor's phasor diagram
        :param time: time moment, second, float
        :return: None
        """
        # get start and end coordinate
        sta_crd = self.get_sta_crd(time=time)
        end_crd = self.get_end_crd(time=time)
        # set the arrow
        self.arrow.set_positions(posA=(sta_crd[0], sta_crd[1]),
                                 posB=(end_crd[0], end_crd[1]))
        self.arrow.set_visible(True)

    def update_phasor(self,
                      time):
        """
        method: update phasor's phasor diagram
        :param time: current time, second
        :return: arrow, matplotlib.patches.FancyArrowPatch
        """
        # get start and end coordinate
        sta_crd = self.get_sta_crd(time=time)
        end_crd = self.get_end_crd(time=time)
        # set the arrow
        self.arrow.set_positions(posA=(sta_crd[0], sta_crd[1]),
                                 posB=(end_crd[0], end_crd[1]))
        return self.arrow

    def clear_waveform(self):
        """
        method: clear waveform
        :return:
        """
        self.line.set_data([], [])
        self.line.set_visible(False)

    def disp_waveform(self,
                      sta_time=0.0,
                      end_time=0.0,
                      step_time=0.001):
        """
        method: display waveform
        :param sta_time:
        :param end_time:
        :param step_time: interval time between 2 points, second
        :return: None
        """
        # step_time must be less than one tenth of period(T)
        if step_time > 0.1 / self._source['freq']:
            self._source['step_time'] = 0.1 / self._source['freq']
        else:
            self._source['step_time'] = step_time
        # draw
        if sta_time == end_time:
            t = [sta_time, ]
            y = [self.get_rt_value(sta_time).real, ]
        else:
            idx = range(0, int(end_time / self._source['step_time']), 1)
            t = []
            y = []
            for i in idx:
                t.append(i * self._source['step_time'] + sta_time)
                y.append(self.get_rt_value(time=t[i]).real)

        self.line.set_data(t, y)
        self.line.set_visible(True)

    def update_waveform(self,
                        sta_time=0.0,
                        end_time=0.0):
        """
        method: update the sine waveform
        :param sta_time: start time, second
        :param end_time: end time, second
        :return: self.line
        """
        idx = range(0, int(end_time / self._source['step_time']), 1)
        t = []
        y = []
        # draw
        if sta_time == end_time:
            t = [sta_time, ]
            y = [self.get_rt_value(sta_time).real, ]
        else:
            idx = range(0, int(end_time / self._source['step_time']), 1)
            t = []
            y = []
            for i in idx:
                t.append(i * self._source['step_time'] + sta_time)
                y.append(self.get_rt_value(time=t[i]).real)

        self.line.set_data(t, y)
        return self.line


class MergePhasors(SinglePhasor):
    """
    class: Merge multiple phasors to get a new phasor
    """
    def __init__(self,
                 id,
                 phasors,
                 pha_axes=None,
                 sin_axes=None,
                 **kwargs):
        """
        method:
        :param id: merged phasor's id
        :param phasors: phasors to be merged
        :param pha_axes: axes to display the phasor diagram
        :param sin_axes: axes to display the sine waveform
        :param kwargs: Keyword argument, e.g., passing to matplotlib.patches.FancyArrowPatches, e.g.,
        name: phasor's name, default value is the same with id
        sta_crd: (x, y)
        sta_phasor_tmnl: (Phasor, 'sta'), (Phasor, 'end')
        zoom: zoom factor, zoom<1 represent zoom out, zoom>1 represent zoom in
        freq: frequency of the phasor, Hz, int

        color:
        linestyle:
        linewidth:
        alpha:
        headlength:
        headwidth:
        tailwidth:
        """
        self.phasors = phasors
        super().__init__(id=id,
                         value=self.get_rt_value(time=0),
                         pha_axes=pha_axes,
                         sin_axes=sin_axes,
                         sta_phasor_tmnl=self.phasors[0].get_sta_phasor(),
                         **kwargs)

    def get_rt_value(self,
                     angle=None,
                     time=None):
        """
        method: get real-time value according to the angle or time
        :param angle:
        :param time: the moment of the rotating phasor
        :return: real-time value of the merged phasor
        """
        value = 0
        for phasor in self.phasors:
            value += phasor.get_rt_value(time=time)
        return value

    def get_sta_crd(self,
                    time=0.0):
        """
        method: get start coordinate
        :param time: time, second
        :return: start coordinate
        """
        if self._source['sta_phasor_tmnl'] is not None:
            return self._source['sta_phasor_tmnl'][0].get_crd(tmnl=self._source['sta_phasor_tmnl'][1],
                                                              time=time)
        else:
            return self._source['sta_crd']

    def get_end_crd(self,
                    time=0.0):
        """
        method: get end coordinate
        :param time: time, second
        :return: end coordinate
        """
        sta_crd = self.get_sta_crd(time=time)
        rt_value = self.get_rt_value(time=time)
        return (sta_crd[0] + self._source['zoom'] * rt_value.real,
                sta_crd[1] + self._source['zoom'] * rt_value.imag)

    def get_crd(self,
                tmnl,
                time=0.0):
        """
        method: get the terminal's coordinate of the phasor
        :param tmnl: terminal of the phasor, e.g., 'sta', 'end'
        :param time: moment, unit is second, float
        :return:
        """
        if tmnl == 'sta':
            return self.get_sta_crd(time)
        elif tmnl == 'end':
            return self.get_end_crd(time)


class SingleAxesPhasors:
    """
    class: Phasors include several phasors, these phasors can be displayed on one matplotlib.axes.Axes.
    """
    def __init__(self,
                 phasors_data,
                 fig,
                 axes):
        """
        method: init
        :param phasors_data: phasors data, {'pha_id1': value1, 'pha_id2': value2,..}
        :param fig: matplotlib.figure.Figure
        :paarm axes: matplotlib.axes.Axes
        """
        # phasors data
        self.phasors_data = phasors_data
        # matploblib.figure.Figure
        self.fig = fig
        # matplotlib.axes.Axes
        self.axes = axes

        # Phasor objects, {'ph1': SinglePhasor, 'ph2': SinglePhasor,..}
        self.phasor_objs = {}
        # display id list, ['ph1', 'ph2']
        self.disp_id_list = []
        # display style, 'phasor', 'waveform'
        self.graph_style = None
        # step time
        self.step_time = 0.0001
        # start time
        self.sta_time = 0.0
        # end_time
        self.end_time = 0.5
        # animation variable, matplotlib.animation.FuncAnimation()
        self.animation_var = None
        # animation status, 'start', 'suspend', 'stop'
        self.anim_status = 'stop'
        # drive mode, 'auto', 'manual'
        self.drive_mode = 'auto'
        # mark the initial value of axes's t-axis
        self.init_xlim = [0, 1]

    def build_phasor_objs(self,
                          appearances=None):
        """
        method: add phasors
        :param appearances: appearance of Phsors on axes_id, e.g.,
        {'ph1': {'color': ,'linestyle': , 'linewidth': },
         'ph2':{'color': ,'linestyle': , 'linewidth': }}
        :return: None
        """
        if self.phasor_objs != {}:
            return False

        # add phasors data
        for key in self.phasors_data:
            if appearances is not None:
                self.phasor_objs[key] = SinglePhasor(id=key,
                                                     value=self.phasors_data[key],
                                                     axes=self.axes,
                                                     **appearances[key])
            else:
                self.phasor_objs[key] = SinglePhasor(id=key,
                                                     value=self.phasors_data[key],
                                                     axes=self.axes)

    def get_appearances(self):
        """
        method: get the appearance
        :return:
        """
        phasor_appearances = {}
        for key in self.phasors_data:
            phasor_appearances[key] = self.phasor_objs[key].get_appearance()
        return phasor_appearances

    def set_appearance(self,
                       phasor_id,
                       **kwargs):
        """
        method: set the appearance
        :param phasor_id: phasor_obj's id or key
        :param kwargs: keyword arguments, e.g.,
        color:
        linestyle:
        linewidth:
        alpha:
        :return:
        """
        if kwargs is None:
            return
        if 'color' in kwargs:
            self.phasor_objs[phasor_id].set_appearance(**kwargs)

    def set_sta_pid_tmnl(self,
                         phasor_id,
                         sta_pid_tmnl):
        """
        method: set start point's phasor id and terminal
        :param phasor_id: phasor id
        :param sta_pid_tmnl: start point's phasor id and terminal, tuple, ('ph1', 'sta'), ('ph1', 'end')
        :return: None
        """
        self.phasor_objs[phasor_id].set_sta_phasor_tmnl(phasor=self.phasor_objs[sta_pid_tmnl[0]], tmnl=sta_pid_tmnl[1])

    def set_freq(self,
                 phasor_id,
                 freq):
        """
        method: set freq
        :param phasor_id:
        :param freq:
        :return:
        """
        self.phasor_objs[phasor_id].set_freq(freq=freq)

    def set_time(self,
                 sta_time=None,
                 end_time=None,
                 step_time=None):
        """
        method: set the time
        :param sta_time:
        :param end_time:
        :param step_time:
        :return:
        """
        if sta_time is not None:
            self.sta_time = sta_time
        if end_time is not None:
            self.end_time = end_time
        if step_time is not None:
            self.step_time = step_time

    def get_phasor_num(self):
        """
        method: get phasor number
        :return: 0, 1, 2,..
        """
        return len(self.phasor_objs)

    def get_max_freq(self):
        """
        method: get the maxmium frequency of the phasors
        :return: max frequency
        """
        max_freq = list(self.phasor_objs.values())[0].get_freq()
        for key in self.phasor_objs:
            if self.phasor_objs[key].get_freq() > max_freq:
                max_freq = self.phasor_objs[key].get_freq()
        return max_freq

    def get_min_freq(self):
        """
        method: get the minimum frequency of the phasors
        :return: min frequency
        """
        min_freq = list(self.phasor_objs.values())[0].get_freq()
        for key in self.phasor_objs:
            if self.phasor_objs[key].get_freq() < min_freq:
                min_freq = self.phasor_objs[key].get_freq()
        return min_freq

    def clear_phasors(self):
        """
        method: clear phasor
        :return:
        """
        for key in self.phasor_objs:
            self.phasor_objs[key].clear_phasor()
        self.graph_style = None
        self.fig.canvas.draw_idle()

    def disp_phasors(self,
                     disp_id_list=None,
                     time=0.0):
        """
        method: display phasors' phasor diagram, including original phasors
        :param disp_id_list: id list of phasors to be displayed
        :param time: time moment, second, float, e.g., 1.0
        :return: None
        """
        if disp_id_list is not None:
            self.disp_id_list = disp_id_list

        # display all the phasors
        for key in self.disp_id_list:
            self.phasor_objs[key].disp_phasor(time=time)

        self.graph_style = 'phasor'
        self.fig.canvas.draw_idle()

    def update_phasors(self,
                       curr_time):
        """
        method: update phasors's diagram
        :param curr_time: current time moment, second, float, e.g., 1.0
        :return: [arrow_1, arrow_2, ..], arrow_n is matplotlib.patches.FancyArrowPatch
        """
        arrows = []

        for key in self.disp_id_list:
            arrow = self.phasor_objs[key].update_phasor(time=curr_time)
            arrows.append(arrow)
        return arrows

    def clear_waveforms(self):
        """
        method: clear sin waveforms
        :return:
        """
        for key in self.phasor_objs:
            self.phasor_objs[key].clear_waveform()
        self.graph_style = None
        self.fig.canvas.draw_idle()

    def disp_waveforms(self,
                       disp_id_list=None,
                       sta_time=None,
                       end_time=None,
                       step_time=None):
        """
        method: display phasors' sine waveform
        :param disp_id_list: list of phasors' id to be displayed as sine waveform
        :param sta_time: start time moment, second, float, e.g., 0.0
        :param end_time: end time moment, second, float, e.g., 1.0
        :param step_time: time step, second, float, e.g., 0.001
        :return: None
        """
        # start time
        if sta_time is not None:
            self.sta_time = sta_time
        # step_time must be less than one-tenth of the minimum period of phasors
        if step_time is not None:
            if step_time > 0.1 / self.get_max_freq():
                self.step_time = 0.1 / self.get_max_freq()
            else:
                self.step_time = step_time
        # end time
        if end_time is not None:
            self.end_time = end_time

        # display id list
        if disp_id_list is not None:
            self.disp_id_list = disp_id_list

        # get the initial value of xlim
        self.init_xlim = self.axes.get_xlim()
        # display all the phasors
        for key in self.disp_id_list:
            self.phasor_objs[key].disp_waveform(sta_time=self.sta_time,
                                                end_time=self.end_time,
                                                step_time=self.step_time)
        self.graph_style = 'waveform'
        self.fig.canvas.draw_idle()

    def update_waveforms(self,
                         curr_time):
        """
        method: update the phasor's sine waveform
        :param curr_time: time moment, second, float, e.g., 1.0
        :return: [line_1, line_2, ..], line_n is matplotlib.lines.Line2D
        """
        lines = []
        for key in self.disp_id_list:
            line = self.phasor_objs[key].update_waveform(sta_time=self.sta_time,
                                                         end_time=curr_time)
            lines.append(line)
        return lines

    def clear_legend(self):
        """
        method: clear legend
        :return:
        """
        self.axes.legend((), ())

    def disp_pha_legend(self):
        """
        method: display legend for phasor graph
        :return:
        """
        handles = []
        for key in self.disp_id_list:
            handles.append(self.phasor_objs[key].arrow)
        self.axes.legend(handles, self.disp_id_list, loc='upper right')

    def disp_wav_legend(self):
        """
        method: display legend for waveform graph
        :return:
        """
        handles = []
        for key in self.disp_id_list:
            handles.append(self.phasor_objs[key].line)
        self.axes.legend(handles, self.disp_id_list, loc='upper right')

    def expand_time_axis(self,
                         curr_time=None,
                         ratio=None):
        """
        method: expand the time axis, there are two ways to expand the time axis. The first way is to expand according
        to a ratio, The second way is to expand according to the curr_time(current time moment)
        :param curr_time: current time moment
        :param ratio: expand ratio, >1
        :return: None
        """
        tmin, tmax = self.axes.get_xlim()

        if curr_time > tmax:
            if ratio is None:
                self.axes.set_xlim(tmin, curr_time)
            else:
                self.axes.set_xlim(tmin, tmax * ratio)

    def shift_time_axis(self,
                        curr_time=None):
        """
        method: shift the time axis
        :return: None
        """
        tmin, tmax = self.axes.get_xlim()
        time_period = tmax - tmin
        if curr_time > tmax:
            self.axes.set_xlim(curr_time - time_period, curr_time)
        elif curr_time < tmax and curr_time - time_period > self.init_xlim[0]:
            self.axes.set_xlim(curr_time - time_period, curr_time)

    def restore_time_axis(self):
        """
        method: restore the time axis
        :return:
        """
        self.axes.set_xlim(self.init_xlim)

    def animation_phasors(self,
                          disp_id_list=None,
                          speed=10.0,
                          period_num=None):
        """
        method: animation phasors
        :param disp_id_list: id list of phasors to be displayed, e.g., [phasor_id_1, phasor_id_2, ..]
        :param speed: speed factor, speed>1 accelarate the speed, speed<1 slow down the speed
        :param period_num: number of the maximum period of phasors
        :return: None
        """
        # end time
        if period_num is not None:
            end_time = period_num / self.get_min_freq()

        # init the display
        self.disp_phasors(disp_id_list=disp_id_list)

        def gen_func():
            """generator function for FuncAnimation"""
            i = 0
            while True:
                i += 1
                if period_num is not None and i >= end_time / (self.step_time * speed):
                    i = 0
                yield i

        def animate(count):
            return self.update_phasors(count * self.step_time * speed)

        self.animation_var = animation.FuncAnimation(fig=self.fig, func=animate, frames=gen_func, save_count=10,
                                                     interval=1, repeat=True, blit=False)

    def animation_waveforms(self,
                            disp_id_list=None,
                            speed=1.0,
                            mode='expand',
                            period_num=None):
        """
        method: animation waveforms
        :param disp_id_list: id list of phasors to be displayed, e.g., [phasor_id_1, phasor_id_2, ..]
        :param speed: speed factor, speed>1 accelarate the speed, speed<1 slow down the speed
        :param mode: when the time achieve limitation of the time axis of the sine waveform, the animation will go on
        according to the mode.
        'expand':
        'shift':
        'fixed':
        :param period_num: number of the maximum period of phasors
        :return: None
        """
        # end time
        if period_num is not None:
            end_time = period_num / self.get_min_freq()

        # init display
        self.disp_waveforms(disp_id_list=disp_id_list, end_time=0.0)

        def gen_func():
            """generator function for FuncAnimation"""
            i = 0
            while True:
                i += 1
                if period_num is not None and i >= end_time / (self.step_time * speed):
                    i = 0
                yield i

        def animate(count):
            """generator function for FuncAnimation"""
            if mode == 'expand':
                self.expand_time_axis(curr_time=count * self.step_time * speed)
            elif mode == 'shift':
                self.shift_time_axis(curr_time=count * self.step_time * speed)

            return self.update_waveforms(count * self.step_time * speed)

        self.animation_var = animation.FuncAnimation(fig=self.fig, func=animate, init_func=self.restore_time_axis,
                                                     frames=gen_func, save_count=10, interval=1,
                                                     repeat=True, blit=False)

    def animation(self,
                  disp_id_list=None,
                  speed=1.0,
                  mode='expand',
                  period_num=None):
        """
        method: animation, end time is the axes' limit time, i.e., xlim
        :param disp_id_list: id list of phasors to be displayed, e.g., [phasor_id_1, phasor_id_2, ..]
        :param speed: speed factor, speed>1 accelarate the speed, speed<1 slow down the speed
        :param mode: when the time achieve limitation of the time axis of the sine waveform, the animation will go on
        according to the mode.
        'expand':
        'shift':
        'fixed':
        :param period_num: number of the maximum period of phasors
        :return: None
        """
        if self.graph_style == 'phasor':
            self.animation_phasors(disp_id_list=disp_id_list,
                                   speed=speed,
                                   period_num=period_num)
        elif self.graph_style == 'waveform':
            self.animation_waveforms(disp_id_list=disp_id_list,
                                     speed=speed,
                                     mode=mode,
                                     period_num=period_num)

    def gui_animation_phasors(self,
                              disp_id_list=None):
        """
        method: gui controlled animation for phasors
        :param disp_id_list: id list of phasors to be displayed, e.g., [phasor_id_1, phasor_id_2, ..]
        :return: None
        """
        speed = 1.0
        # end time, 10 period
        end_time = 10 / self.get_min_freq()
        exit_flag = False

        pop_win = tk.Toplevel()
        pop_win.title('Animation Controller')
        pop_win.geometry('800x70')

        def exit_animation():
            """exit animation function"""
            nonlocal exit_flag
            exit_flag = True
            self.clear_phasors()
            self.disp_phasors(time=self.sta_time)
            pop_win.destroy()

        pop_win.protocol("WM_DELETE_WINDOW", exit_animation)

        def spd_adj_func(value):
            """speed down function"""
            nonlocal speed
            speed = eval(value.replace('x', ''))

        def start_func():
            """start function"""
            self.anim_status = 'start'

        def stop_func():
            """stop function"""
            self.anim_status = 'stop'

        def suspend_func():
            """suspend function"""
            self.anim_status = 'suspend'

        def position_func(value):
            """position function"""
            print(value)

        def axis_mode_func(value):
            """mode function"""
            pass

        def drive_mode_func(value):
            """drive mode function"""
            self.drive_mode = value

        ctr_page = gui_elements.PhasorAnimationControlPage(master=pop_win,
                                                           from_=0,
                                                           to=int(end_time / (self.step_time * speed)),
                                                           speed_adj_func=spd_adj_func,
                                                           start_func=start_func,
                                                           stop_func=stop_func,
                                                           suspend_func=suspend_func,
                                                           position_func=position_func,
                                                           axis_mode_func=axis_mode_func,
                                                           drive_mode_func=drive_mode_func)
        # init the display
        self.disp_phasors(disp_id_list=disp_id_list)

        def gen_func():
                i = 0
                while not exit_flag:
                    if self.drive_mode == 'manual':
                        i = ctr_page.position_var.get()
                        i /= speed
                    elif self.drive_mode == 'auto':
                        if self.anim_status == 'start':
                            i += 1
                            if i >= end_time / (self.step_time * speed):
                                i = 0
                        elif self.anim_status == 'stop':
                            i = 0
                        ctr_page.position_var.set(value=i)
                    yield i

        def animate(count):
            """animate"""
            return self.update_phasors(count * 0.1 / self.get_max_freq() * speed)

        self.animation_var = animation.FuncAnimation(fig=self.fig, func=animate, frames=gen_func, save_count=10,
                                                     interval=1, repeat=False, blit=False)

    def gui_animation_waveforms(self,
                                disp_id_list=None, ):
        """
        method: gui controlled animation
        :param disp_id_list: id list of plots to be displayed, e.g., [phasor_id_1, phasor_id_2, ..]
        :return: None
        """
        mode = 'expand'
        speed = 1.0
        exit_flag = False

        pop_win = tk.Toplevel()
        pop_win.title('Animation Controller')
        pop_win.geometry('800x70')

        def exit_animation():
            """exit animation function"""
            nonlocal exit_flag
            exit_flag = True
            self.clear_waveforms()
            self.disp_waveforms()
            pop_win.destroy()

        pop_win.protocol("WM_DELETE_WINDOW", exit_animation)

        def spd_adj_func(value):
            """speed down function"""
            nonlocal speed
            speed = eval(value.replace('x', ''))

        def start_func():
            """start function"""
            self.anim_status = 'start'

        def stop_func():
            """stop function"""
            self.anim_status = 'stop'

        def suspend_func():
            """suspend function"""
            self.anim_status = 'suspend'

        def position_func(value):
            """position function"""
            pass

        def axis_mode_func(value):
            """mode function"""
            nonlocal mode
            mode = value

        def drive_mode_func(value):
            """drive mode function"""
            self.drive_mode = value

        ctr_page = gui_elements.PhasorAnimationControlPage(master=pop_win,
                                                           from_=0,
                                                           to=int(self.end_time / (self.step_time * speed)),
                                                           speed_adj_func=spd_adj_func,
                                                           start_func=start_func,
                                                           stop_func=stop_func,
                                                           suspend_func=suspend_func,
                                                           position_func=position_func,
                                                           axis_mode_func=axis_mode_func,
                                                           drive_mode_func=drive_mode_func)
        # init the display
        self.disp_waveforms(disp_id_list=disp_id_list)

        def gen_func():
            i = 0
            while not exit_flag:
                if self.drive_mode == 'manual':
                    i = ctr_page.position_var.get()
                    i /= speed
                elif self.drive_mode == 'auto':
                    if self.anim_status == 'start':
                        i += 1
                        if i >= self.end_time / (self.step_time * speed):
                            i = 0
                    elif self.anim_status == 'stop':
                        i = 0
                        self.restore_time_axis()
                    ctr_page.position_var.set(value=i * speed)
                yield i

        def animate(count):
            """animate"""
            nonlocal speed

            if mode == 'expand':
                self.expand_time_axis(curr_time=count * self.step_time * speed)
            elif mode == 'shift':
                self.shift_time_axis(curr_time=count * self.step_time * speed)

            return self.update_waveforms(count * self.step_time * speed)

        self.animation_var = animation.FuncAnimation(fig=self.fig, func=animate, init_func=self.restore_time_axis,
                                                     frames=gen_func, save_count=10, interval=1,
                                                     repeat=False, blit=False)

    def gui_animation(self,
                      disp_id_list=None):
        """
        method: animation, end time is the axes' limit time, i.e., xlim
        :param disp_id_list: id list of phasors to be displayed, e.g., [phasor_id_1, phasor_id_2, ..]
        :return: None
        """
        if self.graph_style == 'phasor':
            self.gui_animation_phasors(disp_id_list=disp_id_list)
        elif self.graph_style == 'waveform':
            self.gui_animation_waveforms(disp_id_list=disp_id_list)


class MultiAxesPhasors:
    """
    class: several SingleAxesPhasors displayed on multiple Axes
    """
    def __init__(self,
                 phasors_data,
                 fig):
        """
        method:
        :param phasors_data:
        :param fig:
        """
        # phasors data
        self.phasors_data = phasors_data
        # matploblib.figure.Figure
        self.fig = fig
        # matplotlib.axes.Axes
        self.axes = {}
        # appearances
        self.appearances = None
        # drive mode, 'auto', 'manual'
        self.drive_mode = 'auto'
        # animation status, 'stop', 'start', 'suspend'
        self.anim_status = 'stop'
        # animation variable
        self.animation_var = None

        # start time
        self.sta_time = 0.0
        # end_time
        self.end_time = 0.5
        # step time
        self.step_time = 0.0001

        # dict of SingleAxesPhasors
        self.single_axes_phasors_objs = {}

    def add_single_axes_phasors(self,
                                axes_id,
                                axes_obj):
        """
        method: add single axes phasors
        :param axes_id: axes's id, str
        :param axes_obj: axes object, matplotlib.axes.Axes
        :return: None
        """
        self.axes[axes_id] = axes_obj
        self.single_axes_phasors_objs[axes_id] = SingleAxesPhasors(phasors_data=self.phasors_data,
                                                                   fig=self.fig,
                                                                   axes=self.axes[axes_id])
        if self.appearances is None:
            self.single_axes_phasors_objs[axes_id].build_phasor_objs()
            self.appearances = self.single_axes_phasors_objs[axes_id].get_appearances()
        else:
            self.single_axes_phasors_objs[axes_id].build_phasor_objs(appearances=self.appearances)

    def set_time(self,
                 sta_time=None,
                 end_time=None,
                 step_time=None):
        """
        method: set the time
        :param sta_time:
        :param end_time:
        :param step_time:
        :return:
        """
        if sta_time is not None:
            self.sta_time = sta_time
        if end_time is not None:
            self.end_time = end_time
        if step_time is not None:
            self.step_time = step_time
        # set all the SingleAxesPhasors' time
        for key in self.single_axes_phasors_objs:
            self.single_axes_phasors_objs[key].set_time(sta_time=self.sta_time,
                                                        end_time=self.end_time,
                                                        step_time=self.step_time)

    def clear_phasors(self,
                      axes_id):
        """
        method:
        :param axes_id:
        :return:
        """
        self.single_axes_phasors_objs[axes_id].clear_phasors()
        self.single_axes_phasors_objs[axes_id].clear_waveforms()
        self.single_axes_phasors_objs[axes_id].clear_legend()

    def disp_phasors(self,
                     axes_id,
                     disp_id_list=None,
                     time=None):
        """
        method: disp phasors
        :param axes_id:
        :param disp_id_list:
        :param time:
        :return:
        """
        self.single_axes_phasors_objs[axes_id].disp_phasors(disp_id_list=disp_id_list, time=time)
        self.disp_pha_legend(axes_id=axes_id)

    def disp_waveforms(self,
                       axes_id,
                       disp_id_list=None):
        """
        method: disp waveforms
        :param axes_id:
        :param disp_id_list:
        :return:
        """
        self.single_axes_phasors_objs[axes_id].disp_waveforms(disp_id_list=disp_id_list, sta_time=self.sta_time,
                                                              end_time=self.end_time, step_time=self.step_time)
        self.disp_wav_legend(axes_id=axes_id)

    def disp_pha_legend(self,
                        axes_id):
        """
        method: display legend for phasor
        :param axes_id:
        :return:
        """
        self.single_axes_phasors_objs[axes_id].disp_pha_legend()

    def disp_wav_legend(self,
                        axes_id):
        """
        method: display legend for waveform
        :param axes_id:
        :return:
        """
        self.single_axes_phasors_objs[axes_id].disp_wav_legend()

    def gui_animation(self,
                      axes_id_list):
        """
        method:
        :param axes_id_list:
        :return:
        """
        mode = 'expand'
        speed = 1.0
        exit_flag = False

        pop_win = tk.Toplevel()
        pop_win.title('Animation Controller')
        pop_win.geometry('800x70')

        def exit_animation():
            """exit animation function"""
            nonlocal exit_flag
            exit_flag = True
            self.anim_status = 'stop'
            for key in axes_id_list:
                if self.single_axes_phasors_objs[key].graph_style == 'phasor':
                    self.single_axes_phasors_objs[key].clear_phasors()
                    self.single_axes_phasors_objs[key].disp_phasors()
                elif self.single_axes_phasors_objs[key].graph_style == 'waveform':
                    self.single_axes_phasors_objs[key].clear_waveforms()
                    self.single_axes_phasors_objs[key].disp_waveforms()

            pop_win.destroy()

        pop_win.protocol("WM_DELETE_WINDOW", exit_animation)

        def spd_adj_func(value):
            """speed down function"""
            nonlocal speed
            speed = eval(value.replace('x', ''))

        def start_func():
            """start function"""
            self.anim_status = 'start'

        def stop_func():
            """stop function"""
            self.anim_status = 'stop'

        def suspend_func():
            """suspend function"""
            self.anim_status = 'suspend'

        def position_func(value):
            """position function"""
            pass

        def axis_mode_func(value):
            """mode function"""
            nonlocal mode
            mode = value

        def drive_mode_func(value):
            """drive mode function"""
            self.drive_mode = value

        ctr_page = gui_elements.PhasorAnimationControlPage(master=pop_win,
                                                           from_=0,
                                                           to=int(self.end_time / (self.step_time * speed)),
                                                           speed_adj_func=spd_adj_func,
                                                           start_func=start_func,
                                                           stop_func=stop_func,
                                                           suspend_func=suspend_func,
                                                           position_func=position_func,
                                                           axis_mode_func=axis_mode_func,
                                                           drive_mode_func=drive_mode_func)
        # init the display
        for key in axes_id_list:
            if self.single_axes_phasors_objs[key].graph_style == 'phasor':
                self.disp_phasors(axes_id=key)
            elif self.single_axes_phasors_objs[key].graph_style == 'waveform':
                self.disp_waveforms(axes_id=key)

        def gen_func():
            i = 0
            while not exit_flag:
                if self.drive_mode == 'manual':
                    i = ctr_page.position_var.get()
                    i /= speed
                elif self.drive_mode == 'auto':
                    if self.anim_status == 'start':
                        i += 1
                        if i >= self.end_time / (self.step_time * speed):
                            i = 0
                    elif self.anim_status == 'stop':
                        for key in axes_id_list:
                            if self.single_axes_phasors_objs[key].graph_style == 'waveform':
                                self.single_axes_phasors_objs[key].restore_time_axis()
                        i = 0
                    ctr_page.position_var.set(value=i * speed)
                yield i

        def animate(count):
            """animate"""
            nonlocal speed
            result = []

            for key in axes_id_list:
                if self.single_axes_phasors_objs[key].graph_style == 'phasor':
                    result += self.single_axes_phasors_objs[key].update_phasors(count * self.step_time * speed)
                elif self.single_axes_phasors_objs[key].graph_style == 'waveform':
                    result += self.single_axes_phasors_objs[key].update_waveforms(count * self.step_time * speed)
                    if mode == 'expand':
                        self.single_axes_phasors_objs[key].expand_time_axis(curr_time=count * self.step_time * speed)
                    elif mode == 'shift':
                        self.single_axes_phasors_objs[key].shift_time_axis(curr_time=count * self.step_time * speed)

            return result

        self.animation_var = animation.FuncAnimation(fig=self.fig, func=animate, frames=gen_func, save_count=10,
                                                     interval=1, repeat=False, blit=False)


class SingleAxesNumericals:
    """
    class: Numerical Plot, used to plot graph using numerical data
    """
    def __init__(self,
                 numerical_data,
                 fig,
                 axes):
        """
        method:
        :param numerical_data: data, dict, e.g.,
        {'time': [], 'line1': [], 'line2': [],..}
        :param fig: matplotlib.figure.Figure
        :param axes: matplotlib.axes.Axes
        """
        # numerical data
        self.numerical_data = numerical_data
        # matplotlib's figure
        self.fig = fig
        # matplotlib's axes
        self.axes = axes

        # dict of lines, which is matplotlib.lines.Line2D
        self.line_objs = {}
        # data id list to be displayed, ['line1', 'line2']
        self.disp_id_list = []
        # animation variable
        self.animation_var = None
        # animation variable, matplotlib.animation.FuncAnimation()
        self.anim_status = 'stop'
        # drive mode, 'auto', 'manual'
        self.drive_mode = 'auto'
        # mark the initial value of axes's t-axis
        self.init_xlim = [0, 1]

    def build_line_objs(self,
                        appearances=None):
        """
        method: create the 2DLines, give them to self.lines
        :param appearances: appearance data,
        {'line1': {'color': ,'linestyle': , 'linewidth': },
         'line2': {'color': ,'linestyle': , 'linewidth': }}
        :return: None
        """
        if self.line_objs != {}:
            return False

        # add matplotlib.line.Line2D
        for key in self.numerical_data:
            if appearances is not None:
                self.line_objs[key], = self.axes.plot([],
                                                      [],
                                                      **appearances[key])
            else:
                self.line_objs[key], = self.axes.plot([],
                                                      [])

    def get_appearances(self):
        """
        method: get the apperances
        :return:
        """
        line_appearances = {}
        for key in self.line_objs:
            line_appearances[key] = {}
            line_appearances[key]['color'] = self.line_objs[key].get_color()
            line_appearances[key]['linestyle'] = self.line_objs[key].get_linestyle()
            line_appearances[key]['linewidth'] = self.line_objs[key].get_linewidth()
        return line_appearances

    def set_appearance(self,
                       line_id,
                       **kwargs):
        """
        method: set the appearance
        :param line_id: line_obj's id or key
        :param kwargs: keyword arguments, e.g.,
        color:
        linestyle:
        linewidth:
        :return:
        """
        if kwargs is None:
            return
        if 'color' in kwargs:
            self.line_objs[line_id].set_color(kwargs['color'])
        if 'linestyle' in kwargs:
            self.line_objs[line_id].set_linestyle(kwargs['linestyle'])
        if 'linewidth' in kwargs:
            self.line_objs[line_id].set_linewidth(kwargs['linewidth'])

    def get_line_num(self):
        """
        method: get line number
        :return: int
        """
        return len(self.line_objs)

    def get_numerical_length(self):
        """
        method: get numerical data length
        :return:
        """
        return len(self.numerical_data['time'])

    def clear_legend(self):
        """
        method: clear legend
        :return:
        """
        self.axes.legend((), (), loc='upper left')

    def disp_legend(self):
        """
        method: display legend
        :return:
        """
        handles = []
        for key in self.disp_id_list:
            handles.append(self.line_objs[key])
        self.axes.legend(handles, self.disp_id_list, loc='upper left')

    def clear_lines(self):
        """
        method: clear plot
        :return:
        """
        for key in self.numerical_data:
            self.line_objs[key].set_data([],
                                          [])
            self.line_objs[key].set_visible(False)
        # refresh the canvas of fig(matplotlib.figure.Figure)
        self.fig.canvas.draw_idle()

    def disp_lines(self,
                   disp_id_list=None):
        """
        method: display the lines
        :param disp_id_list: a list consist of values' id to be displayed, e.g., [id_1, id_2,..]
        :return:
        """
        if disp_id_list is not None:
            self.disp_id_list = disp_id_list
        # get the initial value of xlim
        self.init_xlim = self.axes.get_xlim()
        # display all the lines
        for key in self.disp_id_list:
            self.line_objs[key].set_data(self.numerical_data['time'],
                                         self.numerical_data[key])
            self.line_objs[key].set_visible(True)
        self.fig.canvas.draw_idle()

    def update_lines(self,
                     numerical_data=None,
                     idx=0):
        """
        method: update
        :param numerical_data: {'time': [], 'line1': [], 'line2': [],..}
        :param idx: iterator
        :return: self.lines
        """
        if numerical_data is None:
            for key in self.disp_id_list:
                self.line_objs[key].set_data(self.numerical_data['time'][0: idx], self.numerical_data[key][0: idx])
        else:
            for key in self.disp_id_list:
                self.line_objs[key].set_data(self.numerical_data['time'], self.numerical_data[key])
        return self.line_objs

    def expand_time_axis(self,
                         curr_time=None,
                         ratio=None):
        """
        method: expand the time axis
        :param curr_time: current time
        :param ratio: expand ratio, >1
        :return:
        """
        tmin, tmax = self.axes.get_xlim()

        if curr_time > tmax:
            if ratio is None:
                self.axes.set_xlim(tmin, curr_time)
            else:
                self.axes.set_xlim(tmin, tmax * ratio)

    def expand_value_axis(self,
                          numerical_data):
        """
        method: expand the value axis
        :param numerical_data:
        :return:
        """
        ymin, ymax = self.axes.get_ylim()
        for key in numerical_data:
            if max(numerical_data[key]) > ymax:
                ymax = max(numerical_data[key])
            elif min(numerical_data[key]) < ymin:
                ymin = min(numerical_data[key])
        self.axes.set_ylim(ymin, ymax)

    def shift_time_axis(self,
                        curr_time=None):
        """
        method: shift the time x axis
        :return:
        """
        tmin, tmax = self.axes.get_xlim()
        time_period = tmax - tmin
        if curr_time > tmax:
            self.axes.set_xlim(curr_time - time_period, curr_time)
        elif curr_time < tmax and curr_time - time_period > self.init_xlim[0]:
            self.axes.set_xlim(curr_time - time_period, curr_time)

    def restore_time_axis(self):
        """
        method: restore the time axis
        :return:
        """
        self.axes.set_xlim(self.init_xlim)

    def animation(self,
                  disp_id_list=None,
                  speed=1.0,
                  mode='expand',
                  repeat=None):
        """
        method: animation
        :param disp_id_list: id list of lines to be displayed
        :param speed: float, 1.0
        :param mode: when the time achieve limitation of the time axis of the sine waveform, the animation will go on
        according to the mode.
        'expand':
        'shift':
        'fixed'
        :param repeat: if the sine wave will repeat animation, True, False
        :return:
        """
        self.clear_lines()
        # init the display
        self.disp_lines(disp_id_list=disp_id_list)

        frames = int(self.get_numerical_length() / speed)

        def animate(count):
            self.expand_value_axis(numerical_data=self.numerical_data)

            if mode == 'expand':
                if count*speed < len(self.numerical_data['time']):
                    self.expand_time_axis(curr_time=self.numerical_data['time'][int(count*speed)])

            elif mode == 'shift':
                if count * speed < len(self.numerical_data['time']):
                    self.shift_time_axis(curr_time=self.numerical_data['time'][int(count*speed)])

            return self.update_lines(idx=int(count * speed))

        self.animation_var = animation.FuncAnimation(fig=self.fig, func=animate, init_func=self.restore_time_axis,
                                                     frames=frames, save_count=10, interval=1,
                                                     repeat=repeat, blit=False)

    def gui_animation(self,
                      disp_id_list=None):
        """
        method: gui controlled animation
        :param disp_id_list: ids for displaying
        :return:
        """
        pop_win = tk.Toplevel()
        pop_win.title('Animation Controller')
        pop_win.geometry('800x70')
        mode = 'expand'
        speed = 1
        exit_flag = False

        def exit_animation():
            """exit animation function"""
            nonlocal exit_flag
            exit_flag = True
            self.clear_lines()
            self.disp_lines()
            pop_win.destroy()

        pop_win.protocol("WM_DELETE_WINDOW", exit_animation)

        def spd_adj_func(value):
            """speed adjust function"""
            nonlocal speed
            speed = eval(value.replace('x', ''))

        def start_func():
            """start function"""
            self.anim_status = 'start'

        def stop_func():
            """stop function"""
            self.anim_status = 'stop'

        def suspend_func():
            """suspend function"""
            self.anim_status = 'suspend'

        def position_func(value):
            """position function"""
            print(value)

        def axis_mode_func(value):
            """axis mode function"""
            nonlocal mode
            mode = value

        def drive_mode_func(value):
            """drive mode function"""
            self.drive_mode = value

        ctr_page = gui_elements.PlotAnimationControlPage(master=pop_win,
                                                         from_=0,
                                                         to=int(self.get_numerical_length() / speed),
                                                         speed_adj_func=spd_adj_func,
                                                         start_func=start_func,
                                                         stop_func=stop_func,
                                                         suspend_func=suspend_func,
                                                         position_func=position_func,
                                                         axis_mode_func=axis_mode_func,
                                                         drive_mode_func=drive_mode_func)
        self.clear_lines()
        # init the display
        self.disp_lines(disp_id_list=disp_id_list)

        def gen_func():
            i = 0
            while not exit_flag:
                if self.drive_mode == 'manual':
                    i = ctr_page.position_var.get()
                    i /= speed
                elif self.drive_mode == 'auto':
                    if self.anim_status == 'start':
                        i += 1
                        if i >= len(self.numerical_data['time']) / speed:
                            i = 0
                    elif self.anim_status == 'stop':
                        i = 0
                        self.restore_time_axis()
                    ctr_page.position_var.set(value=i)
                yield i

        def animate(count):
            """animate"""
            nonlocal speed
            self.expand_value_axis(numerical_data=self.numerical_data)

            if mode == 'expand':
                if count * speed < len(self.numerical_data['time']):
                    self.expand_time_axis(curr_time=self.numerical_data['time'][int(count * speed)])

            elif mode == 'shift':
                if count * speed < len(self.numerical_data['time']):
                    self.shift_time_axis(curr_time=self.numerical_data['time'][int(count * speed)])

            return self.update_lines(idx=int(count * speed))

        self.animation_var = animation.FuncAnimation(fig=self.fig, func=animate, init_func=self.restore_time_axis,
                                                     frames=gen_func, save_count=10, interval=1,
                                                     repeat=False, blit=False)


class MultiAxesNumericals:
    """
    class: several SingleAxesNumerical displayed on multiple Axes
    """
    def __init__(self,
                 numerical_data,
                 fig):
        """
        method:
        :param numerical_data:
        :param fig:
        """
        # numerical data
        self.numerical_data = numerical_data
        # matploblib.figure.Figure
        self.fig = fig
        # matplotlib.axes.Axes
        self.axes = {}
        # appearances
        self.appearances = None
        # drive mode, 'auto', 'manual'
        self.drive_mode = 'auto'
        # animation status, 'stop', 'start', 'suspend'
        self.anim_status = 'stop'
        # animation variable
        self.animation_var = None

        # dict of SingleAxesPhasors
        self.single_axes_numerical_objs = {}

    def add_single_axes_numericals(self,
                                   axes_id,
                                   axes_obj):
        """
        method: add single axes numerical data
        :param axes_id: axes's id, str
        :param axes_obj: axes object, matplotlib.axes.Axes
        :return: None
        """
        self.axes[axes_id] = axes_obj
        self.single_axes_numerical_objs[axes_id] = SingleAxesNumericals(numerical_data=self.numerical_data,
                                                                        fig=self.fig,
                                                                        axes=self.axes[axes_id])
        if self.appearances is None:
            self.single_axes_numerical_objs[axes_id].build_line_objs()
            self.appearances = self.single_axes_numerical_objs[axes_id].get_appearances()
        else:
            self.single_axes_numerical_objs[axes_id].build_line_objs(appearances=self.appearances)

    def get_numerical_length(self):
        """
        method: get numerical data length
        :return:
        """
        return len(self.numerical_data['time'])

    def clear_lines(self,
                    axes_id):
        """
        method:
        :param axes_id:
        :return:
        """
        self.single_axes_numerical_objs[axes_id].clear_lines()
        self.single_axes_numerical_objs[axes_id].clear_legend()

    def disp_lines(self,
                   axes_id,
                   disp_id_list=None):
        """
        method: disp line
        :param axes_id:
        :param disp_id_list:
        :return:
        """
        self.single_axes_numerical_objs[axes_id].disp_lines(disp_id_list=disp_id_list)
        self.single_axes_numerical_objs[axes_id].disp_legend()

    def gui_animation(self,
                      axes_id_list):
        """
        method:
        :param axes_id_list:
        :return:
        """
        mode = 'expand'
        speed = 1.0
        exit_flag = False

        pop_win = tk.Toplevel()
        pop_win.title('Animation Controller')
        pop_win.geometry('800x70')

        def exit_animation():
            """exit animation function"""
            nonlocal exit_flag
            exit_flag = True
            self.anim_status = 'stop'
            for key in axes_id_list:
                self.single_axes_numerical_objs[key].clear_lines()
                self.single_axes_numerical_objs[key].disp_lines()

            pop_win.destroy()

        pop_win.protocol("WM_DELETE_WINDOW", exit_animation)

        def spd_adj_func(value):
            """speed down function"""
            nonlocal speed
            speed = eval(value.replace('x', ''))

        def start_func():
            """start function"""
            self.anim_status = 'start'

        def stop_func():
            """stop function"""
            self.anim_status = 'stop'

        def suspend_func():
            """suspend function"""
            self.anim_status = 'suspend'

        def position_func(value):
            """position function"""
            pass

        def axis_mode_func(value):
            """mode function"""
            nonlocal mode
            mode = value

        def drive_mode_func(value):
            """drive mode function"""
            self.drive_mode = value

        ctr_page = gui_elements.PhasorAnimationControlPage(master=pop_win,
                                                           from_=0,
                                                           to=int(self.get_numerical_length() / speed)-1,
                                                           speed_adj_func=spd_adj_func,
                                                           start_func=start_func,
                                                           stop_func=stop_func,
                                                           suspend_func=suspend_func,
                                                           position_func=position_func,
                                                           axis_mode_func=axis_mode_func,
                                                           drive_mode_func=drive_mode_func)
        # init the display
        for key in axes_id_list:
            self.disp_lines(axes_id=key)

        def gen_func():
            i = 0
            while not exit_flag:
                if self.drive_mode == 'manual':
                    i = ctr_page.position_var.get() / speed
                elif self.drive_mode == 'auto':
                    if self.anim_status == 'start':
                        i += 1
                        if i >= self.get_numerical_length()/speed:
                            i = 0
                    elif self.anim_status == 'stop':
                        for key in axes_id_list:
                            self.single_axes_numerical_objs[key].restore_time_axis()
                        i = 0
                    ctr_page.position_var.set(value=i * speed)
                yield i

        def animate(count):
            """animate"""
            nonlocal speed
            result = []

            for key in axes_id_list:
                result += self.single_axes_numerical_objs[key].update_lines(idx=int(count * speed))
                if mode == 'expand':
                    self.single_axes_numerical_objs[key].\
                        expand_time_axis(curr_time=self.numerical_data['time'][int(count * speed)])
                elif mode == 'shift':
                    self.single_axes_numerical_objs[key].\
                        shift_time_axis(curr_time=self.numerical_data['time'][int(count * speed)])

            return result

        self.animation_var = animation.FuncAnimation(fig=self.fig, func=animate, frames=gen_func, save_count=10,
                                                     interval=1, repeat=False, blit=False)


class SingleAxesDecimals:
    """
    class: Decimal Plot, used to plot graph using decimal data
    """
    def __init__(self,
                 decimal_data,
                 fig,
                 axes):
        """
        method:
        :param decimal_data: data, dict, e.g.,
        {'line1': 1.15, 'line2': 2.5,..}
        :param fig: matplotlib.figure.Figure
        :param axes: matplotlib.axes.Axes
        """
        # decimal data
        self.decimal_data = decimal_data
        # matplotlib's figure
        self.fig = fig
        # matplotlib's axes
        self.axes = axes

        # dict of lines, which is matplotlib.lines.Line2D
        self.line_objs = {}
        # data id list to be displayed, ['line1', 'line2']
        self.disp_id_list = None
        # mark the initial value of axes's t-axis
        self.init_xlim = [0, 1]

    def build_line_objs(self,
                        appearances=None):
        """
        method: create the 2DLines, give them to self.lines
        :param appearances: appearance data,
        {'line1': {'color': ,'linestyle': , 'linewidth': },
         'line2': {'color': ,'linestyle': , 'linewidth': }}
        :return: None
        """
        if self.line_objs != {}:
            return False

        # add matplotlib.line.Line2D
        for key in self.decimal_data:
            if appearances is not None:
                self.line_objs[key], = self.axes.plot([],
                                                      [],
                                                      **appearances[key])
            else:
                self.line_objs[key], = self.axes.plot([],
                                                      [])

    def get_appearances(self):
        """
        method: get the apperances
        :return:
        """
        line_appearances = {}
        for key in self.line_objs:
            line_appearances[key] = {}
            line_appearances[key]['color'] = self.line_objs[key].get_color()
            line_appearances[key]['linestyle'] = self.line_objs[key].get_linestyle()
            line_appearances[key]['linewidth'] = self.line_objs[key].get_linewidth()
        return line_appearances

    def set_appearance(self,
                       line_id,
                       **kwargs):
        """
        method: set the appearance
        :param line_id: line_obj's id or key
        :param kwargs: keyword arguments, e.g.,
        color:
        linestyle:
        linewidth:
        :return:
        """
        if kwargs is None:
            return
        if 'color' in kwargs:
            self.line_objs[line_id].set_color(kwargs['color'])
        if 'linestyle' in kwargs:
            self.line_objs[line_id].set_linestyle(kwargs['linestyle'])
        if 'linewidth' in kwargs:
            self.line_objs[line_id].set_linewidth(kwargs['linewidth'])

    def get_line_num(self):
        """
        method: get line number
        :return: int
        """
        return len(self.line_objs)

    def clear_legend(self):
        """
        method: clear legend
        :return:
        """
        self.axes.legend((), (), loc='upper right')

    def disp_legend(self):
        """
        method: disp method
        :return:
        """
        handles = []
        for key in self.disp_id_list:
            handles.append(self.line_objs[key])
        self.axes.legend(handles, self.disp_id_list, loc='upper right')

    def clear_lines(self):
        """
        method: clear plot
        :return:
        """
        for key in self.decimal_data:
            self.line_objs[key].set_data([],
                                          [])
            self.line_objs[key].set_visible(False)
        # refresh the canvas of fig(matplotlib.figure.Figure)
        self.fig.canvas.draw_idle()

    def disp_lines(self,
                   disp_id_list=None):
        """
        method: display the lines
        :param disp_id_list: a list consist of values' id to be displayed, e.g., [id_1, id_2,..]
        :return:
        """
        if disp_id_list is not None:
            self.disp_id_list = disp_id_list
        # get the initial value of xlim
        self.init_xlim = self.axes.get_xlim()
        # display all the lines
        for key in self.disp_id_list:
            self.line_objs[key].set_data(self.init_xlim,
                                         [self.decimal_data[key], self.decimal_data[key]])
            self.line_objs[key].set_visible(True)
        self.fig.canvas.draw_idle()


class MultiAxesDecimals:
    """
    class: several SingleAxesDecimal displayed on multiple Axes
    """
    def __init__(self,
                 decimal_data,
                 fig):
        """
        method:
        :param decimal_data:
        :param fig:
        """
        # decimal data
        self.decimal_data = decimal_data
        # matploblib.figure.Figure
        self.fig = fig
        # matplotlib.axes.Axes
        self.axes = {}
        # appearances
        self.appearances = None

        # dict of SingleAxesDecimal
        self.single_axes_decimal_objs = {}

    def add_single_axes_decimals(self,
                                 axes_id,
                                 axes_obj):
        """
        method: add single axes decimal data
        :param axes_id: axes's id, str
        :param axes_obj: axes object, matplotlib.axes.Axes
        :return: None
        """
        self.axes[axes_id] = axes_obj
        self.single_axes_decimal_objs[axes_id] = SingleAxesDecimals(decimal_data=self.decimal_data,
                                                                    fig=self.fig,
                                                                    axes=self.axes[axes_id])
        if self.appearances is None:
            self.single_axes_decimal_objs[axes_id].build_line_objs()
            self.appearances = self.single_axes_decimal_objs[axes_id].get_appearances()
        else:
            self.single_axes_decimal_objs[axes_id].build_line_objs(appearances=self.appearances)

    def clear_lines(self,
                    axes_id):
        """
        method:
        :param axes_id:
        :return:
        """
        self.single_axes_decimal_objs[axes_id].clear_lines()
        self.single_axes_decimal_objs[axes_id].clear_legend()

    def disp_lines(self,
                   axes_id,
                   disp_id_list=None):
        """
        method: disp line
        :param axes_id:
        :param disp_id_list:
        :return:
        """
        self.single_axes_decimal_objs[axes_id].disp_lines(disp_id_list=disp_id_list)
        self.single_axes_decimal_objs[axes_id].disp_legend()


class Graph:
    """
    class: graph
    """
    def __init__(self,
                 master,
                 data_ucomps,
                 data_icomps,
                 data_unodes,
                 data_time=None):
        """
        method: init the graph
        :param master: tkinter's widget, e.g., frame
        :param data_ucomps: {'R-1': [], 'C-1': [],..}, or {'R-1': value, 'C-1': value}
        :param data_icomps: {'R-1': [], 'C-1': [],..}, or {'R-1': value, 'C-1': value}
        :param data_unodes: {'node1': [], 'node2': [],..}, or {'node1': value, 'node2': value}
        :param data_time: time consequence, list
        """
        # master
        self.master = master
        # matplotlib's figure on tkinter's widget
        self.fig_tk = None
        # figsize, [8, 6]
        self.figsize = [7.0, 5.0]
        self.nrows = 0
        self.ncols = 0
        # data for entire graph, {'time': [], 'U_R-1': [], 'U_C-1': [], .., 'I_R-1': [], 'I_C-1': [],..}
        self.data = {}
        # time varying Axes, dict
        self.time_varying_axes = {}
        # phasor Axes, dict
        self.phasor_axes = {}
        # Phasor objects, dict
        self.phasor_obj = None
        # Numerical objects, dict
        self.numerical_obj = None
        # Decimal objects, dict
        self.decimal_obj = None
        # id list of data to be displayed, {'axes1': ['U_R-1', 'U_C-1'], 'axes2': [],..}
        self.disp_id_list = {}

        # set data
        self._set_data(data_time=data_time,
                       data_ucomps=data_ucomps,
                       data_icomps=data_icomps,
                       data_unodes=data_unodes)
        #
        self.create_figure()

    def _set_data(self,
                  data_time,
                  data_ucomps,
                  data_icomps,
                  data_unodes):
        """
        method:
        :param data_time:
        :param data_ucomps:
        :param data_icomps:
        :param data_unodes:
        :return:
        """
        if data_time is not None:
            self.data['time'] = data_time
        for key in data_ucomps:
            self.data['U_'+key] = data_ucomps[key]
        for key in data_icomps:
            self.data['I_'+key] = data_icomps[key]
        for key in data_unodes:
            self.data['U_'+key] = data_unodes[key]

    def create_figure(self,
                      figsize=None):
        """
        method: create figure
        :param figsize: figure size
        :return: None
        """
        if figsize is not None:
            self.figsize = figsize

        self.fig_tk = FigureOnTk(master=self.master, figsize=self.figsize)
        self.divide_figure(nrows=1, ncols=1)
        if self.judge_data() == 'phasor':
            self.phasor_obj = MultiAxesPhasors(phasors_data=self.data,
                                               fig=self.fig_tk.figure)
        elif self.judge_data() == 'numerical':
            self.numerical_obj = MultiAxesNumericals(numerical_data=self.data,
                                                     fig=self.fig_tk.figure)
        elif self.judge_data() == 'decimal':
            self.decimal_obj = MultiAxesDecimals(decimal_data=self.data,
                                                 fig=self.fig_tk.figure)

    def divide_figure(self,
                      nrows,
                      ncols):
        """
        method: divide the figure into nrows and ncols
        :param nrows: number of axes in row
        :param ncols: number of axes in column
        :return: None
        """
        self.nrows = nrows
        self.ncols = ncols
        self.fig_tk.divide(nrows=nrows, ncols=ncols)

    def judge_data(self):
        """
        method: judge the data's element's type, return 'phasor', 'numerical', 'decimal' or False
        :return: 'phasor', 'numerical', 'decimal' or False
        """
        pha_flag = True
        num_flag = True
        dec_flag = True
        for key in self.data:
            if key == 'time':
                continue
            if type(self.data[key]) != np.complex128 and not isinstance(self.data[key], complex):
                pha_flag = False
            if not isinstance(self.data[key], list):
                num_flag = False
            if type(self.data[key]) != np.float64 and not isinstance(self.data[key], float):
                dec_flag = False

        if pha_flag:
            return 'phasor'
        elif num_flag:
            return 'numerical'
        elif dec_flag:
            return 'decimal'
        else:
            return False

    def add_axes(self,
                 axes_id,
                 row=0,
                 col=0,
                 grid=True,
                 **kwargs):
        """
        method: add an Axes to the figure as part of a subplot arrangement
        :param axes_id:
        :param row: row
        :param col: column
        :param grid: if there is grid, False
        :param kwargs: Keyword arguments, e.g.,
        xlim: x-axis' limitation, (float, float)
        ylim: y-axis' limitation, (float, float)
        label: Set a label that will be displayed in the legend.
        transparency: a float define the transparency, 0.0 - 1.0
        xlabel: label for the x-axis, str
        ylabel: label for the y-axis, str
        xscale: x-axis scale, "linear", "log", "symlog", "logit"
        yscale: y-axis scale, "linear", "log", "symlog", "logit"
        :return: axes
        """
        self.time_varying_axes[axes_id] = self.fig_tk.add_axes(row=row,
                                                               col=col,
                                                               grid=grid,
                                                               **kwargs)
        if self.judge_data() == 'phasor':
            self.phasor_obj.add_single_axes_phasors(axes_id=axes_id,
                                                    axes_obj=self.time_varying_axes[axes_id])
        elif self.judge_data() == 'numerical':
            self.numerical_obj.add_single_axes_numericals(axes_id=axes_id,
                                                          axes_obj=self.time_varying_axes[axes_id])
        elif self.judge_data() == 'decimal':
            self.decimal_obj.add_single_axes_decimals(axes_id=axes_id,
                                                      axes_obj=self.time_varying_axes[axes_id])
        self.disp_id_list[axes_id] = []

    def add_pha_axes(self,
                     axes_id,
                     row=0,
                     col=0,
                     grid=True,
                     axis_visible=True,
                     **kwargs):
        """
        method: add an Axes to the figure as part of a subplot arrangement
        :param axes_id:
        :param row: row
        :param col: column
        :param grid: if there is grid, False
        :param axis_visible:
        :param kwargs: Keyword arguments, e.g.,
        xlim: x-axis' limitation, (float, float)
        ylim: y-axis' limitation, (float, float)
        label: Set a label that will be displayed in the legend.
        transparency: a float define the transparency, 0.0 - 1.0
        xlabel: label for the x-axis, str
        ylabel: label for the y-axis, str
        xscale: x-axis scale, "linear", "log", "symlog", "logit"
        yscale: y-axis scale, "linear", "log", "symlog", "logit"
        :return: axes
        """
        if self.judge_data() == 'phasor':
            self.phasor_axes[axes_id] = self.fig_tk.add_pha_axes(row=row,
                                                                 col=col,
                                                                 grid=grid,
                                                                 axis_visible=axis_visible,
                                                                 **kwargs)
            self.phasor_obj.add_single_axes_phasors(axes_id=axes_id,
                                                    axes_obj=self.phasor_axes[axes_id])
        self.disp_id_list[axes_id] = []

    def set_phasor_waveform_time(self,
                                 sta_time=None,
                                 end_time=None,
                                 step_time=None):
        """
        method: set the phasor's waveform time
        :param sta_time:
        :param end_time:
        :param step_time:
        :return:
        """
        if self.phasor_obj:
            self.phasor_obj.set_time(sta_time=sta_time,
                                     end_time=end_time,
                                     step_time=step_time)

    def clear_axes(self,
                   axes_id):
        """
        method: clear graph on axes_id
        :param axes_id:
        :return:
        """
        self.clear(axes_id=axes_id)

        self.disp_id_list[axes_id] = []

    def del_axes(self,
                 axes_id):
        """
        method: delete the axes
        :param axes_id:
        :return:
        """
        if axes_id in self.time_varying_axes.keys():
            self.fig_tk.figure.delaxes(self.time_varying_axes[axes_id])
            self.time_varying_axes.pop(axes_id)
        elif axes_id in self.phasor_axes.keys():
            self.fig_tk.figure.delaxes(self.phasor_axes[axes_id])
            self.phasor_axes.pop(axes_id)
        self.fig_tk.canvas.draw_idle()

    def clear(self,
              axes_id):
        """
        method:
        :param axes_id:
        :return:
        """
        if self.judge_data() == 'phasor':
            self.phasor_obj.clear_phasors(axes_id=axes_id)
        elif self.judge_data() == 'numerical':
            self.numerical_obj.clear_lines(axes_id=axes_id)
        elif self.judge_data() == 'decimal':
            self.decimal_obj.clear_lines(axes_id=axes_id)

    def display(self,
                axes_id,
                disp_id_list=None):
        """
        method:
        :param axes_id:
        :param disp_id_list:
        :return:
        """
        if disp_id_list is not None:
            self.disp_id_list[axes_id] = disp_id_list
        if not self.disp_id_list[axes_id]:
            return
        pre_ui = self.disp_id_list[axes_id][0].split('_')[0]
        id_list_check = []
        for key in self.disp_id_list[axes_id]:
            if pre_ui + '_' in key:
                id_list_check.append(key)

        if self.judge_data() == 'phasor':
            if axes_id in self.phasor_axes.keys():
                self.phasor_obj.disp_phasors(axes_id=axes_id, disp_id_list=id_list_check)
            elif axes_id in self.time_varying_axes.keys():
                self.phasor_obj.disp_waveforms(axes_id=axes_id, disp_id_list=id_list_check)
        elif self.judge_data() == 'numerical':
            self.numerical_obj.disp_lines(axes_id=axes_id, disp_id_list=id_list_check)
        elif self.judge_data() == 'decimal':
            self.decimal_obj.disp_lines(axes_id=axes_id, disp_id_list=id_list_check)

    def gui_animation(self,
                      axes_id_list):
        """
        method:
        :param axes_id_list:
        :return:
        """
        if self.judge_data() == 'phasor':
            self.phasor_obj.gui_animation(axes_id_list=axes_id_list)
        elif self.judge_data() == 'numerical':
            self.numerical_obj.gui_animation(axes_id_list=axes_id_list)


class GraphGUI(Graph):
    """
    class: graphGUI
    """
    def __init__(self,
                 data_ucomps,
                 data_icomps,
                 data_unodes,
                 data_time=None):
        """
        method: init the graph GUI
        :param data_ucomps: {'R-1': [], 'C-1': [],..}, or {'R-1': value, 'C-1': value}
        :param data_icomps: {'R-1': [], 'C-1': [],..}, or {'R-1': value, 'C-1': value}
        :param data_unodes: {'node1': [], 'node2': [],..}, or {'node1': value, 'node2': value}
        :param data_time: time consequence, list
        """
        self.root_win = None
        self.win_width = None
        self.win_height = None
        # frame operation, project, figure
        self.frame_oper = None
        self.frame_prj = None
        self.frame_fig = None
        # operation page and variable list page
        self.page_oper = None
        self.page_axes_list = None
        self.page_var_list = {}
        # current axes' key
        self.curr_axes_key = None

        self.build_root_win()

        super().__init__(master=self.frame_fig, data_ucomps=data_ucomps, data_icomps=data_icomps,
                         data_unodes=data_unodes, data_time=data_time)
        self.build_var_list(master=self.frame_prj)

        self.build_oper_page(master=self.frame_oper)
        self.mainloop()

    def build_root_win(self,
                       geometry='1800x1200'):
        """
        method: build root window
        :param geometry: window's geometry
        :return: None
        """
        self.root_win = tk.Toplevel()
        self.root_win.grid_propagate(0)
        self.root_win.title('Elecpy->Graph')
        self.win_width = int(geometry.split('x')[0])
        self.win_height = int(geometry.split('x')[1])
        self.root_win.geometry(geometry)

        # operation area
        self.frame_oper = tk.LabelFrame(self.root_win, bg='#F0F0F0', text=None, font=('仿宋', 12),
                                        height=32,
                                        width=self.win_width)
        self.frame_oper.grid(row=0, column=0, columnspan=2)
        self.frame_oper.grid_propagate(0)

        # project area
        self.frame_prj = tk.LabelFrame(self.root_win, bg='#F0F0F0', text=None, font=('仿宋', 12),
                                       height=self.win_height - 32,
                                       width=200)
        self.frame_prj.grid(row=1, column=0)
        self.frame_prj.grid_propagate(0)

        # figure area
        self.frame_fig = tk.LabelFrame(self.root_win, bg='#F0F0F0', text=None, font=('仿宋', 12),
                                       height=self.win_height - 32,
                                       width=self.win_width-200)
        self.frame_fig.grid(row=1, column=1)
        self.frame_fig.grid_propagate(0)
        self.master = self.frame_fig

    def mainloop(self):
        """
        method: mainloop of the root_win
        :return: None
        """
        self.root_win.mainloop()

    def build_oper_page(self,
                        master):
        """
        method: build operation bar
        :param master: the tkinter widget, tkinter.Frame
        :return: None
        """
        self.page_oper = gui_elements.ButtonsPage(master=master,
                                                  btn_lst=['ConfigFig', 'ClearFig', 'NewAxes', 'NewPhaAxes', 'ConfigAxes',
                                                           'ClearAxes', 'DelAxes', 'Animation'],
                                                  wdg_width=800,
                                                  num_per_row=20)
        self.page_oper.command(btn_nm='ConfigFig',
                               cal_func=self.config_figure)
        self.page_oper.command(btn_nm='ClearFig',
                               cal_func=self.clear_fig)
        self.page_oper.command(btn_nm='NewAxes',
                               cal_func=self.config_new_axes)
        self.page_oper.command(btn_nm='NewPhaAxes',
                               cal_func=self.config_new_pha_axes)
        self.page_oper.command(btn_nm='ConfigAxes',
                               cal_func=self.config_axes)
        self.page_oper.command(btn_nm='ClearAxes',
                               cal_func=self.clear_curr_axes)
        self.page_oper.command(btn_nm='DelAxes',
                               cal_func=self.del_curr_axes)
        self.page_oper.command(btn_nm='Animation',
                               cal_func=self.config_animation)

        # disable condition
        if self.judge_data() != 'phasor':
            self.page_oper.disable(btn_lst=['NewPhaAxes'])
        self.page_oper.disable(btn_lst=['ConfigAxes', 'ClearAxes', 'DelAxes', 'Animation'])

    def set_current_axes(self, axes_key):
        """
        method: get the current axes
        :param axes_key:
        :return:
        """
        self.curr_axes_key = axes_key

    def build_var_list(self,
                       master):
        """
        method: build variable list
        :param master: the tkinter widget, tkinter.Frame
        :return: None
        """
        self.page_axes_list = gui_elements.RadiobuttonPage(master=master,
                                                           row=0,
                                                           height=200,
                                                           label='Axes',
                                                           list_data=list(self.time_varying_axes.keys()),
                                                           func=self.set_current_axes)

        voltage_key = []
        current_key = []
        for key in self.data:
            if 'U_' in key:
                voltage_key.append(key)
            elif 'I_' in key:
                current_key.append(key)

        self.page_var_list['voltage'] = gui_elements.ListboxPage(master=master,
                                                                 row=1,
                                                                 height=250,
                                                                 label='Voltage',
                                                                 list_data=voltage_key)
        self.page_var_list['voltage'].command(cal_func=self.display_curr_axes)
        self.page_var_list['current'] = gui_elements.ListboxPage(master=master,
                                                                 row=2,
                                                                 height=250,
                                                                 label='current',
                                                                 list_data=current_key)
        self.page_var_list['current'].command(cal_func=self.display_curr_axes)

    def display_curr_axes(self,
                          var_category,
                          var_key):
        """
        method: display
        :param var_category: variable category, e.g., 'voltage', 'current'
        :param var_key: var key, e.g., 'U_R-1'
        :return:
        """
        if self.curr_axes_key is None:
            return
        if var_key in self.disp_id_list[self.curr_axes_key]:
            index = self.disp_id_list[self.curr_axes_key].index(var_key)
            self.disp_id_list[self.curr_axes_key].pop(index)
        else:
            self.disp_id_list[self.curr_axes_key].append(var_key)

        # set the y label
        if self.curr_axes_key in self.time_varying_axes.keys():
            if self.disp_id_list[self.curr_axes_key]:
                if 'U_' in self.disp_id_list[self.curr_axes_key][0]:
                    self.time_varying_axes[self.curr_axes_key].set_ylabel('U/V')
                elif 'I_' in self.disp_id_list[self.curr_axes_key][0]:
                    self.time_varying_axes[self.curr_axes_key].set_ylabel('I/A')
            else:
                self.time_varying_axes[self.curr_axes_key].set_ylabel('')
        self.clear(axes_id=self.curr_axes_key)
        self.display(axes_id=self.curr_axes_key)

    def clear_fig(self):
        """
        method: clear figure
        :return:
        """
        self.time_varying_axes.clear()
        self.phasor_axes.clear()
        self.fig_tk.figure.clear()
        self.fig_tk.canvas.draw_idle()
        self.page_axes_list.set_data(list_data=[])
        if not self.time_varying_axes and not self.phasor_axes:
            self.page_oper.disable(btn_lst=['ConfigAxes', 'ClearAxes', 'DelAxes', 'Animation'])

    def config_figure(self):
        """
        method: config the figure
        :return: None
        """
        pop_win = gui_elements.NormalWin(title='Fig Config',
                                         width=300,
                                         height=400)

        def cal_func(value):
            """cal function"""
            self.clear_fig()
            self.figsize = value[2]
            self.fig_tk.figure.set_figwidth(val=self.figsize[0], forward=True)
            self.fig_tk.figure.set_figheight(val=self.figsize[1], forward=True)

            self.divide_figure(nrows=int(value[0]),
                               ncols=int(value[1]))
            pop_win.destroy()

        data = [{'style': 'Entry', 'name': 'nrows', 'value': self.nrows},
                {'style': 'Entry', 'name': 'ncols', 'value': self.ncols},
                {'style': 'Range', 'name': 'figsize', 'value': self.figsize}]

        edit_page = gui_elements.NormalEditPage(master=pop_win.root_win,
                                                save_butt_label='confirm',
                                                save_butt_func=cal_func,
                                                data=data)

    def config_axes(self):
        """
        method: config the current selected axes
        :return: None
        """
        pop_win = gui_elements.NormalWin(title='Axes Config',
                                         width=300,
                                         height=400)

        def cal_func(value):
            """callback function"""
            if self.curr_axes_key in self.time_varying_axes.keys():
                self.time_varying_axes[self.curr_axes_key].set_xlim(value[0])
                self.time_varying_axes[self.curr_axes_key].set_ylim(value[1])
            elif self.curr_axes_key in self.phasor_axes.keys():
                self.phasor_axes[self.curr_axes_key].set_xlim(value[0])
                self.phasor_axes[self.curr_axes_key].set_ylim(value[1])
            self.fig_tk.canvas.draw()
            pop_win.destroy()

        xlim = [0, 0]
        ylim = [0, 0]
        if self.curr_axes_key in self.time_varying_axes.keys():
            xlim = list(self.time_varying_axes[self.curr_axes_key].get_xlim())
            ylim = list(self.time_varying_axes[self.curr_axes_key].get_ylim())
        elif self.curr_axes_key in self.phasor_axes.keys():
            xlim = list(self.phasor_axes[self.curr_axes_key].get_xlim())
            ylim = list(self.phasor_axes[self.curr_axes_key].get_ylim())

        data = [{'style': 'Range', 'name': 'xlim', 'value': xlim},
                {'style': 'Range', 'name': 'ylim', 'value': ylim}]
        edit_page = gui_elements.NormalEditPage(master=pop_win.root_win,
                                                row=0,
                                                column=0,
                                                save_butt_label='confirm',
                                                save_butt_func=cal_func,
                                                data=data)

    def clear_curr_axes(self):
        """
        method: clear the current axes
        :return:
        """
        if self.curr_axes_key:
            self.clear_axes(axes_id=self.curr_axes_key)
            if self.curr_axes_key in self.time_varying_axes.keys():
                self.time_varying_axes[self.curr_axes_key].set_ylabel('')

    def config_new_axes(self):
        """
        method: config the new axes
        :return:
        """
        pop_win = gui_elements.NormalWin(title='Axes Config',
                                         width=400,
                                         height=400)

        def cal_func(value):
            """cal function"""
            axes_id = str(value[0]) + '-' + str(value[1])
            if axes_id in self.time_varying_axes.keys() or axes_id in self.phasor_axes.keys():
                return

            self.add_axes(axes_id=axes_id, row=value[0], col=value[1], grid=True, xlim=value[2], ylim=value[3],
                          xlabel='t/s')
            self.page_axes_list.set_data(list_data=list(self.time_varying_axes.keys())+list(self.phasor_axes.keys()))

            if not self.time_varying_axes and not self.phasor_axes:
                self.page_oper.disable(btn_lst=['ConfigAxes', 'ClearAxes', 'DelAxes', 'Animation'])
            else:
                self.page_oper.enable(btn_lst=['ConfigAxes', 'ClearAxes', 'DelAxes', 'Animation'])

            pop_win.destroy()

        if self.judge_data() == 'numerical':
            xmax = max(self.data['time']) * 1.1
        else:
            xmax = 1.0

        data = [{'style': 'Radiobutton', 'name': 'row', 'value': range(self.nrows)},
                {'style': 'Radiobutton', 'name': 'column', 'value': range(self.ncols)},
                {'style': 'Range', 'name': 'xlim', 'value': [0, xmax]},
                {'style': 'Range', 'name': 'ylim', 'value': [-30, 30]}]
        edit_page = gui_elements.NormalEditPage(master=pop_win.root_win,
                                                row=0,
                                                column=0,
                                                save_butt_label='confirm',
                                                save_butt_func=cal_func,
                                                data=data)

    def config_new_pha_axes(self):
        """
        method: config the new phasor axes
        :return:
        """
        if self.judge_data() == 'numerical':
            return

        pop_win = gui_elements.NormalWin(title='PhaAxes Config',
                                         width=400,
                                         height=400)

        def cal_func(value):
            """cal function"""
            axes_id = str(value[0]) + '-' + str(value[1])
            if axes_id in self.time_varying_axes.keys() or axes_id in self.phasor_axes.keys():
                return

            self.add_pha_axes(axes_id=axes_id, row=value[0], col=value[1], xlim=value[2], ylim=value[2])
            self.page_axes_list.set_data(list_data=list(self.time_varying_axes.keys())+list(self.phasor_axes.keys()))

            if not self.time_varying_axes and not self.phasor_axes:
                self.page_oper.disable(btn_lst=['ConfigAxes', 'ClearAxes', 'DelAxes', 'Animation'])
            else:
                self.page_oper.enable(btn_lst=['ConfigAxes', 'ClearAxes', 'DelAxes', 'Animation'])

            pop_win.destroy()

        data = [{'style': 'Radiobutton', 'name': 'row', 'value': range(self.nrows)},
                {'style': 'Radiobutton', 'name': 'column', 'value': range(self.ncols)},
                {'style': 'Range', 'name': 'xlim&ylim', 'value': [-30, 30]}]

        edit_page = gui_elements.NormalEditPage(master=pop_win.root_win,
                                                row=0,
                                                column=0,
                                                save_butt_label='confirm',
                                                save_butt_func=cal_func,
                                                data=data)

    def del_curr_axes(self):
        """
        method: delete the current selected axes
        :return:
        """
        if self.curr_axes_key is not None:
            self.del_axes(axes_id=self.curr_axes_key)
            self.page_axes_list.set_data(list_data=list(self.time_varying_axes.keys())+list(self.phasor_axes.keys()))
            self.curr_axes_key = None
            if not self.time_varying_axes and not self.phasor_axes:
                self.page_oper.disable(btn_lst=['ConfigAxes', 'ClearAxes', 'DelAxes', 'Animation'])

    def config_animation(self):
        """
        method: animation
        :return:
        """
        pop_win = gui_elements.NormalWin(title='Animation Config',
                                         width=400,
                                         height=400)

        def cal_func(value):
            """cal function"""
            if self.judge_data() == 'phasor':
                self.set_phasor_waveform_time(sta_time=value[1], end_time=value[2], step_time=value[3])
            if value[0]:
                self.gui_animation(axes_id_list=value[0])
            else:
                return
            pop_win.destroy()

        data = []
        if self.judge_data() == 'phasor':
            data = [{'style': 'Checkbutton', 'name': 'Select Axes',
                     'value': list(self.time_varying_axes.keys())+list(self.phasor_axes.keys())},
                    {'style': 'Entry', 'name': 'start time', 'value': self.phasor_obj.sta_time},
                    {'style': 'Entry', 'name': 'end time', 'value': self.phasor_obj.end_time},
                    {'style': 'Entry', 'name': 'step time', 'value': self.phasor_obj.step_time}]
        elif self.judge_data() == 'numerical':
            data = [{'style': 'Checkbutton', 'name': 'Select Axes',
                     'value': list(self.time_varying_axes.keys())+list(self.phasor_axes.keys())},]

        edit_page = gui_elements.NormalEditPage(master=pop_win.root_win,
                                                save_butt_label='confirm',
                                                save_butt_func=cal_func,
                                                data=data)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('1500x1200')

    fig = FigureOnTk(master=root, figsize=[8, 6])
    fig.divide(nrows=2, ncols=2)
    pha_axes1 = fig.add_pha_axes(row=0, grid=True, xlim=[-30, 30], ylim=[-30, 30])
    pha_axes2 = fig.add_axes(row=0, col=1, grid=True, xlim=[0, 0.1], ylim=[-30, 30])
    pha_axes3 = fig.add_pha_axes(row=1, grid=True, xlim=[-30, 30], ylim=[-30, 30])
    pha_axes4 = fig.add_axes(row=1, col=1, grid=True, xlim=[0, 0.1], ylim=[-30, 30])
    phasors = MultiAxesPhasors(phasors_data={'ph1': 10 + 10j, 'ph2': 15 + 5j},
                               fig=fig.figure)
    phasors.add_single_axes_phasors(axes_id='pha_axes1',
                                    axes_obj=pha_axes1)
    phasors.add_single_axes_phasors(axes_id='pha_axes2',
                                    axes_obj=pha_axes2)
    phasors.set_time(sta_time=0,
                     end_time=0.5,
                     step_time=0.0001)
    phasors.disp_phasors(axes_id='pha_axes1',
                         disp_id_list=['ph1', 'ph2'])
    phasors.disp_waveforms(axes_id='pha_axes2',
                           disp_id_list=['ph1', 'ph2'])
    phasors.gui_animation(axes_id_list=['pha_axes1', 'pha_axes2'])

    root.mainloop()
