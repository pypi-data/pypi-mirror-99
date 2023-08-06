"""
module: This module is used for building a circuit through instructions.
"""
import copy
import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import tkinter.font as tkfont
import Elecpy.Default as default
import Elecpy.Diagram as diagram
import Elecpy.Tools as tools
import Elecpy.File as file
import Elecpy.GUIElements as gui_elements
import Elecpy.Calculation as calculation
import Elecpy.Graph as grph
import Elecpy.Templates as templates
import matplotlib.pyplot as pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np


class __Element:
    """
    class: Element, base class of Text, Part, Wire, Graph
    """

    def __init__(self,
                 default_data=None,
                 source_data=None):
        """
        method:
        :param default_data: default data, stored in Elecpy.Default
        :param source_data: source data of the Element, dict
        """
        """default data"""
        # create the default data field
        if default_data is None:
            self.default_data = {'id': '', 'designator': '', 'crd_x': 0, 'crd_y': 0, 'angle': 0, 'visible': True}
        else:
            self.default_data = copy.deepcopy(default_data)
        # create the source data field
        if source_data:
            self.source_data = source_data
            for key in self.default_data:
                if key not in self.source_data.keys():
                    self.source_data[key] = self.default_data[key]
        else:
            self.source_data = self.default_data

        # tkinter canvas
        self.canvas = None
        # contour of the element, [width, height]
        self.square = [0, 0]
        # if the element is selected, e.g., True or False
        self.slct = None
        # mouse right button's pop up menu
        self.rt_menu = None

    def set_data(self,
                 canvas=None,
                 **kwargs):
        """
        method: Set the source data
        :param canvas: tkinter canvas
        :param kwargs: Keyword arguments, e.g.,
        id: id of the element
        designator: a symbol, e.g., 'R-1'
        crd_x:
        crd_y:
        angle:
        visible:
        :return: None
        """
        if canvas is not None:
            self.canvas = canvas
        for key in kwargs:
            if key in self.default_data.keys():
                if 'node' in key:
                    self.source_data[key] = kwargs[key]
                elif kwargs[key] is not None:
                    self.source_data[key] = kwargs[key]

    def get_data(self,
                 key=None):
        """
        method: Get the data
        :param key: data name
        :return:
        """
        # if data is None, return self.source_data
        if key is None:
            return self.source_data
        # if data is not None, return data
        else:
            if key in self.source_data.keys():
                return self.source_data[key]
            else:
                print('This data is not exist!')
                return None

    def display(self,
                canvas=None):
        """
        method: display the element
        :param canvas:
        :return: None
        """
        if canvas is not None:
            self.canvas = canvas
        # if self.canvas is already exist，clear the previous display
        if self.canvas:
            self.clear()

    def move_to(self,
                to_crd):
        """
        method: move the element to to_crd
        :param to_crd: destination location
        :return: None
        """
        x_bias = to_crd[0] - self.source_data['crd_x']
        y_bias = to_crd[1] - self.source_data['crd_y']
        self.source_data['crd_x'] = to_crd[0]
        self.source_data['crd_y'] = to_crd[1]
        self.canvas.move(self.source_data['id'], x_bias, y_bias)

    def move_by(self,
                bias_crd):
        """
        method: move the element to to_crd
        :param bias_crd: bias coordinate
        :return: None
        """
        self.source_data['crd_x'] = bias_crd[0] + self.source_data['crd_x']
        self.source_data['crd_y'] = bias_crd[1] + self.source_data['crd_y']
        self.canvas.move(self.source_data['id'], bias_crd[0], bias_crd[1])

    def rotate(self):
        """
        method: clockwise rotate 90 degree
        :return: None
        """
        self.source_data['angle'] += 90
        self.display()

    def clear(self):
        """
        method: delete the previous display of this element
        :return: None
        """
        # if self.canvas is already exist, delete it
        if self.canvas:
            self.canvas.delete(self.source_data['id'])

    def select(self, crd):
        """
        method: judge if the element is selected by the point with coordinate of crd
        :param crd: coordinate of the point
        :return: if selected, True, if not selected, False
        """
        # judge if the element is selected
        if abs(crd[0] - int(self.source_data['crd_x'])) < self.square[0] / 2 and \
                abs(crd[1] - int(self.source_data['crd_y'])) < self.square[1] / 2:
            self.slct = True
        else:
            self.slct = False
        # return the select status
        return self.slct

    def enclosed_select(self, x0, y0, x1, y1):
        """
        method: enclosed select
        :param x0:
        :param y0:
        :param x1:
        :param y1:
        :return:
        """
        # judge if the element is selected
        if min(x0, x1) < self.source_data['crd_x'] < max(x0, x1) and \
                min(y0, y1) < self.source_data['crd_y'] < max(y0, y1):
            self.slct = True
        else:
            self.slct = False
        return self.slct

    def editable_data(self,
                      nonedit=None):
        """
        method: get editable data of the element
        :param nonedit: non-editable data, None or str or list of str, e.g., 'content', ['content']
        :return: {'designator'}
        """
        if nonedit is None:
            nonedit = []
        elif type(nonedit) == str:
            nonedit = [nonedit]
        nonedit.extend(['id', 'crd_x', 'crd_y', 'angle'])
        edit_data = copy.deepcopy(self.source_data)
        for key in nonedit:
            if key in edit_data.keys():
                edit_data.pop(key)
        return edit_data

    def edit_window(self,
                    nonedit=None,):
        """
        method: an edit window for user to edit the editable window.
        :param nonedit: non-editable data, None or str or list of str, e.g., 'content', ['content']
        :return: None
        """
        edit_data = self.editable_data(nonedit=nonedit)
        edit_win = gui_elements.EditWin(data=edit_data)

        def func_save():
            """
            func: "save" function
            :return: None
            """
            edit_win.destroy()
            self.set_data(**edit_win.page.data)
            self.display()

        edit_win.command(func_save=func_save)
        edit_win.mainloop()


class Text(__Element):
    """
    class: Text, subclass of Element
    """

    def __init__(self,
                 source_data=None,
                 canvas=None,
                 **kwargs):
        """
        method: Create a Text object
        :param source_data: Source data of Text
        :param canvas: tkinter canvas
        :param kwargs: Keyword arguments, refer to Elecpy.Default.dft_text_data, e.g.,
        'id': 'text-1',
        'crd_x': 0,
        'crd_y': 20,
        'angle': 0,
        'color': black,
        'visible': True,
        'content': 'text',
        'font_family': 'Times',
        'font_size': '8',
        'font_weight': 'bold',
        'font_slant': 'roman',
        'font_underline': 0,
        'font_overstrike': 0
        """
        super().__init__(default_data=default.dft_text_data,
                         source_data=source_data)
        self.set_data(canvas=canvas,
                      **kwargs)

    def __get_square(self):
        """
        method: get the contour square of Text
        :return: (width, height)
        """
        # calculate the contour square of Text
        text_width = 0
        if '\n' not in self.source_data['content']:
            text_width = len(self.source_data['content'])
        else:
            for text in self.source_data['content'].split('\n'):
                if text_width < len(text):
                    text_width = len(text)
        return (text_width * int(self.source_data['font_size']),
                (self.source_data['content'].count('\n') + 1) * int(self.source_data['font_size']))

    def display(self,
                canvas=None,
                crd_x=None,
                crd_y=None,
                angle=None):
        """
        method: display the Text
        :param canvas: tkinter canvas
        :param crd_x: coordinate x
        :param crd_y: coordinate y
        :param angle: angle
        :return:
        """
        # set parameters
        self.set_data(canvas=canvas,
                      crd_x=crd_x,
                      crd_y=crd_y,
                      angle=angle)
        # prepare for display
        super().display(canvas=canvas)
        # display Text
        if self.source_data['visible']:
            # define the line color according to the self.slct
            if self.slct:
                lcolor = 'blue'
            else:
                lcolor = self.source_data['color']
            # get the text font
            font = tkfont.Font(family=self.source_data['font_family'],
                               size=self.source_data['font_size'],
                               weight=self.source_data['font_weight'],
                               slant=self.source_data['font_slant'],
                               underline=self.source_data['font_underline'],
                               overstrike=self.source_data['font_overstrike'])

            self.canvas.create_text(self.source_data['crd_x'],
                                    self.source_data['crd_y'],
                                    text=self.source_data['content'],
                                    font=font,
                                    tag=self.source_data['id'],
                                    fill=lcolor,
                                    activefill='blue')
            # get the square of Text
            self.square = self.__get_square()

    def set_data(self,
                 canvas=None,
                 **kwargs):
        """
        method: set data of Text
        :param canvas: tkinter Canvas
        :param kwargs: Keyword arguments, refer to Elecpy.Default.dft_text_data, e.g.,
        'id': 'text-1',
        'crd_x': 0,
        'crd_y': 20,
        'angle': 0,
        'color': black,
        'visible': True,
        'content': 'text',
        'font_family': 'Times',
        'font_size': '8',
        'font_weight': 'bold',
        'font_slant': 'roman',
        'font_underline': 0,
        'font_overstrike': 0
        :return: None
        """
        super().set_data(canvas=canvas,
                         **kwargs)

    def pop_menu(self, x, y):
        """
        method: pop up menu
        :param x:
        :param y:
        :return:
        """
        self.rt_menu = tk.Menu(self.canvas, tearoff=0)
        self.rt_menu.add_command(label='Edit', command=self.edit_window)
        self.rt_menu.add_separator()
        self.rt_menu.post(x + 128, y + 88)


class Part(__Element):
    """
    class: Part of the Component, no designator text and other symbols
    """

    def __init__(self,
                 part_nm,
                 source_data=None,
                 canvas=None,
                 **kwargs):
        """
        method:
        :param part_nm: part name, refer to Elecpy.Default.dft_comps_data's keys, e.g., 'resistor', 'capacitor', ..
        :param source_data: source data of Part
        :param canvas: tkinter canvas
        :param kwargs: Keyword arguments, refer to Elecpy.Default.dft_comps_data, e.g.,
        'id': 'resistor-?',
        'designator': 'R-?',
        'value': 10.0,
        'node1': None,
        'node2': None,
        'vol_dir': 1,
        'cur_dir': 1,
        'crd_x': 60,
        'crd_y': 60,
        'angle': 0
        :return:
        """
        super().__init__(default_data=default.dft_comps_data[part_nm],
                         source_data=source_data)

        # terminals' voltage, V
        self.tmnls_vol = None
        # part's current
        self.cur = None
        # terminals' coordinate, (), ()
        self.tmnls_crd = None

        # set data
        self.set_data(canvas=canvas,
                      **kwargs)

    def set_data(self,
                 tmnls_vol=None,
                 cur=None,
                 canvas=None,
                 **kwargs):
        """
        method: Set the data
        :param tmnls_vol: terminals voltage, V, e.g., [0.0, 0.0](resistor, capactor,..), [0.0, 0.0, 0.0, 0.0]
        (transformer)
        :param cur: part's current, A, 0.0
        :param canvas: tkinter canvas
        :param kwargs: Keyword arguments, refer to Elecpy.Default.dft_comps_data, e.g.,
        'id': 'resistor-?',
        'designator': 'R-?',
        'value': 10.0,
        'node1': None,
        'node2': None,
        'vol_dir': 1,
        'cur_dir': 1,
        'crd_x': 60,
        'crd_y': 60,
        'angle': 0
        :return:
        """
        if tmnls_vol is not None:
            self.tmnls_vol = tmnls_vol
        if cur is not None:
            self.cur = cur
        super().set_data(canvas=canvas,
                         **kwargs)

    def display(self,
                canvas=None,
                crd_x=None,
                crd_y=None,
                angle=None,
                tmnls_vol=None,
                max_vol=1.0,
                cur=None):
        """
        method: display the part
        :param canvas: tkinter canvas
        :param crd_x: coordinate x
        :param crd_y: coordinate y
        :param angle: angle
        :param tmnls_vol: terminals voltage
        :param max_vol: maxmium voltage in the circuit
        :param cur: current of the component
        :return: None
        """
        # set the parameters
        self.set_data(tmnls_vol=tmnls_vol,
                      cur=cur,
                      canvas=canvas,
                      crd_x=crd_x,
                      crd_y=crd_y,
                      angle=angle)

        # prepare for the display
        super().display(canvas=canvas)

        # display the part
        part_name = self.source_data['id'].split('-')[0]
        cnt_crd = (self.source_data['crd_x'], self.source_data['crd_y'])
        angle = self.source_data['angle']
        if part_name == 'resistor':
            comp_data = diagram.draw_resistor_rect(id=self.source_data['id'],
                                                   cnt_crd=cnt_crd,
                                                   angle=angle,
                                                   canvas=self.canvas,
                                                   slct=self.slct,
                                                   tmnls_vol=self.tmnls_vol,
                                                   max_vol=max_vol)
        elif part_name == 'capacitor':
            comp_data = diagram.draw_capacitor(id=self.source_data['id'],
                                               cnt_crd=cnt_crd,
                                               angle=angle,
                                               canvas=self.canvas,
                                               slct=self.slct,
                                               tmnls_vol=self.tmnls_vol,
                                               max_vol=max_vol)
        elif part_name == 'inductor':
            comp_data = diagram.draw_inductor(id=self.source_data['id'],
                                              cnt_crd=cnt_crd,
                                              angle=angle,
                                              canvas=self.canvas,
                                              slct=self.slct,
                                              tmnls_vol=self.tmnls_vol,
                                              max_vol=max_vol)
        elif part_name == 'voltage_dc':
            comp_data = diagram.draw_voltage_dc(id=self.source_data['id'],
                                                cnt_crd=cnt_crd,
                                                angle=angle,
                                                canvas=self.canvas,
                                                slct=self.slct,
                                                tmnls_vol=self.tmnls_vol,
                                                max_vol=max_vol)
        elif part_name == 'voltage_ac':
            comp_data = diagram.draw_voltage_ac(id=self.source_data['id'],
                                                cnt_crd=cnt_crd,
                                                angle=angle,
                                                canvas=self.canvas,
                                                slct=self.slct,
                                                tmnls_vol=self.tmnls_vol,
                                                max_vol=max_vol)
        elif part_name == 'current_dc':
            comp_data = diagram.draw_current_dc(id=self.source_data['id'],
                                                cnt_crd=cnt_crd,
                                                angle=angle,
                                                canvas=self.canvas,
                                                slct=self.slct,
                                                tmnls_vol=self.tmnls_vol,
                                                max_vol=max_vol)
        elif part_name == 'current_ac':
            comp_data = diagram.draw_current_ac(id=self.source_data['id'],
                                               cnt_crd=cnt_crd,
                                               angle=angle,
                                               canvas=self.canvas,
                                               slct=self.slct,
                                               tmnls_vol=self.tmnls_vol,
                                               max_vol=max_vol)
        elif part_name == 'diode':
            comp_data = diagram.draw_diode(id=self.source_data['id'],
                                           cnt_crd=cnt_crd,
                                           angle=angle,
                                           canvas=self.canvas,
                                           slct=self.slct,
                                           tmnls_vol=self.tmnls_vol,
                                           max_vol=max_vol)
        elif part_name == 'switch':
            comp_data = diagram.draw_switch(id=self.source_data['id'],
                                            cnt_crd=cnt_crd,
                                            angle=angle,
                                            canvas=self.canvas,
                                            slct=self.slct,
                                            tmnls_vol=self.tmnls_vol,
                                            max_vol=max_vol)
        elif part_name == 'ground':
            comp_data = diagram.draw_ground(id=self.source_data['id'],
                                            cnt_crd=cnt_crd,
                                            angle=angle,
                                            canvas=self.canvas,
                                            slct=self.slct)
        else:
            raise TypeError('Unknown comp_nm(component name)！！')

        # get the contour square and terminal coordinate
        self.square = comp_data['square']
        self.tmnls_crd = comp_data['tmnls_crd']

        # display a point in two terminals of the part
        diagram.draw_tmnl_circle(self.source_data['id'], self.tmnls_crd, canvas=self.canvas)

    def move_to(self,
                to_crd):
        """
        method: move the part to to_crd
        :param to_crd: destination location, (crd_x, crd_y)
        :return: None
        """
        # move the part
        super().move_to(to_crd)
        # display once after move of the part to refresh the self.tmnls_crd
        self.display()

    def get_value_formula(self):
        """
        method: get the str variable of formula expressing part's value, e.g., 100*sin(50*2*pi*t+20)
        :return: formula str
        """
        # get all the data of the part
        part_data = self.get_data()

        part_name = part_data['id'].split('-')[0]
        if part_name == 'resistor':
            multi, value = tools.get_multi_value(part_data['value'])
            return str(value) + str(multi) + 'Ω'
        elif part_name == 'capacitor':
            multi, value = tools.get_multi_value(part_data['value'])
            return str(value) + str(multi) + 'F'
        elif part_name == 'inductor':
            multi, value = tools.get_multi_value(part_data['value'])
            return str(value) + str(multi) + 'H'
        elif part_name == 'voltage_dc':
            multi, value = tools.get_multi_value(part_data['amp'])
            return str(value) + str(multi) + 'V'
        elif part_name == 'current_dc':
            multi, value = tools.get_multi_value(part_data['amp'])
            return str(value) + str(multi) + 'A'
        elif part_name == 'voltage_ac':
            return str(part_data['amp']) + '*sin(2π*' + str(part_data['freq']) + '*t+' + str(part_data['phase']) + ') V'
        elif part_name == 'current_ac':
            return str(part_data['amp']) + '*sin(2π*' + str(part_data['freq']) + '*t+' + str(part_data['phase']) + ') A'
        else:
            return ''

    def tmnl_select(self,
                    crd):
        """
        method: judge if the terminal is selected by the point with coordinate of crd, if selected, return the terminal
        number, if not selected, return False
        :param crd: coordinate of the point, (crd_x, crd_y)
        :return: selected: terminal number, e.g., 1, 2, not selected: False
        """
        # capture the point
        crd = tools.point_capture(crd)
        # judge if the terminal is selected
        tmnl_slct = False
        for i, tmnl_crd in enumerate(self.tmnls_crd):
            if crd == tmnl_crd:
                tmnl_slct = str(i + 1)
        return tmnl_slct

    def get_tmnl_crd(self,
                     tmnl):
        """
        method: get coordinate of the terminal
        :param tmnl: terminal number, e.g., 1, 2
        :return: coordinate, i.e., (crd_x, crd_y)
        """
        return self.tmnls_crd[int(tmnl) - 1]

    def get_tmnl_net(self,
                     tmnl):
        """
        method: get net id of the terminal
        :param tmnl: terminla number, e.g. 1, 2
        :return: net id, e.g.,
        """
        return self.source_data['node' + str(tmnl)]


class Wire(__Element):
    """
    class: wire for connecting 2 components' terminals
    """

    def __init__(self,
                 source_data=None,
                 comp_objs=None,
                 canvas=None,
                 **kwargs):
        """
        method: create a Wire
        :param source_data: Source data of Wire
        :param comp_objs: Component objects, used for implementing the function that the Connector follows the component
        which moves, e.g., {'comp_id1': Component,..}
        :param canvas: tkinter canvas
        :parma kwargs: Keyword arguments, refer to Elecpy.Default.dft_wire_data, e.g.,
        'id': 'wire-1',
        'designator': 'w-?',
        'net_id': '1',
        'sta_comp': component's id, e.g., 'resistor-1',
        'sta_tmnl': terminal number, e.g. 1, 2,
        'end_comp': component's id, e.g., 'resistor-1',
        'end_tmnl': terminal number, e.g. 1, 2,
        'mid_crds': None or middle points' coordinate, list, i.e., [x1, y1, x2, y2, ...]， e.g., [10, 10, 20, 20]
        """
        # create a Element with wire's default data
        super().__init__(default_data=default.dft_wire_data,
                         source_data=source_data)
        # Component objects, used for create the function that the the wire follows the component which moves, e.g.,
        # {'comp_id1': Component,..}
        self.comp_objs = None
        # set the parameters
        self.set_data(comp_objs=comp_objs,
                      canvas=canvas,
                      **kwargs)

        # wire voltage
        self.wire_vol = 0
        # wire current
        self.wire_cur = 0

    def set_data(self,
                 comp_objs=None,
                 wire_vol=None,
                 wire_cur=None,
                 canvas=None,
                 **kwargs):
        """
        method: Set the parameters of Wire
        :param comp_objs: Component objects, used for implementing the function that the Connector follows the component
        which moves, e.g., {'comp_id1': Component,..}
        :param wire_vol: wire voltage with unit of V, float, e.g., 10.0
        :param wire_cur: wire current with unit of A, float, e.g., 1.0
        :param canvas: tkinter canvas
        :parma kwargs: Keyword arguments, refer to Elecpy.Default.dft_wire_data, e.g.,
        'id': 'wire-1',
        'designator': 'w-?',
        'net_id': '1',
        'sta_comp': component's id, e.g., 'resistor-1',
        'sta_tmnl': terminal number, e.g. 1, 2,
        'end_comp': component's id, e.g., 'resistor-1',
        'end_tmnl': terminal number, e.g. 1, 2,
        'mid_crds': None or middle points' coordinate, list, i.e., [x1, y1, x2, y2, ...]， e.g., [10, 10, 20, 20]
        :return: None
        """
        if comp_objs is not None:
            self.comp_objs = comp_objs
        if wire_vol is not None:
            self.wire_vol = wire_vol
        if wire_cur is not None:
            self.wire_cur = wire_cur
        super().set_data(canvas=canvas,
                         **kwargs)

    def add_comp_tmnl(self,
                      sta_comp=None,
                      sta_tmnl=None,
                      end_comp=None,
                      end_tmnl=None):
        """
        method: Add a Component's key in self.comp_objs and its terminal number to the start terminal or end terminal of
        Wire.
        :param sta_comp: start Component's key, e.g., 'resistor-1', 'capacitor-1', etc,..
        :param sta_tmnl: terminal's number
        :param end_comp: end Component's key, e.g., 'resistor-1', 'capacitor-1', etc,..
        :param end_tmnl: terminal's number
        :return: None
        """
        if sta_comp is not None and sta_tmnl is not None:
            self.source_data['sta_comp'] = sta_comp
            self.source_data['sta_tmnl'] = sta_tmnl
        if end_comp is not None and end_tmnl is not None:
            self.source_data['end_comp'] = end_comp
            self.source_data['end_tmnl'] = end_tmnl

    def tmnl_select(self,
                    crd):
        """
        method: judge if any terminal of components is selected by the point with coordinate of crd, if selected, return
        component id and terminal number, if not selected, return None
        :param crd: coordinate, (crd_x, crd_y)
        :returns: (comp_id, tmnl), e.g. ('resistor-1', 1) or None
        """
        for key in self.comp_objs:
            tmnl = self.comp_objs[key].tmnl_select(crd)
            if tmnl:
                return key, tmnl

    def display(self,
                comp_objs=None,
                wire_vol=None,
                wire_cur=None,
                canvas=None):
        """
        method: display the wire
        :param comp_objs: Component objects, used for create the function that the the wire follows the component which
        moves, e.g., {'comp_id1': Component,..}
        :param wire_vol: wire voltage with unit of V, float, e.g., 10.0
        :param wire_cur: wire current with unit of A, float, e.g., 1.0
        :param canvas: tkinter canvas
        """
        # set the parameters
        self.set_data(comp_objs=comp_objs,
                      wire_vol=wire_vol,
                      wire_cur=wire_cur,
                      canvas=canvas)
        # prepare for display
        super().display(canvas=canvas)

        # get the coordinates of start terminal, middle points and end terminal
        line_pcrds = self.get_sta_tmnl_crd()
        mid_pcrds = self.get_mid_pcrds()
        if mid_pcrds is not None:
            line_pcrds += mid_pcrds
        line_pcrds += self.get_end_tmnl_crd()
        # get the line's width and color according to the select status
        if self.slct:
            color = 'blue'
            width = 4
        else:
            color = 'black'
            width = 2

        # create a line
        self.canvas.create_line(line_pcrds, tags=self.source_data['id'], fill=color, width=width, activewidth=4,
                                activefill='blue')

    def move_by(self,
                bias_crd):
        """
        method: move the element to to_crd
        :param bias_crd: bias coordinate
        :return: None
        """
        if self.source_data['mid_crds'] is not None:
            for i in range(0, int(len(self.source_data['mid_crds'])/2)):
                self.source_data['mid_crds'][2 * i] += bias_crd[0]
                self.source_data['mid_crds'][2 * i + 1] += bias_crd[1]
        self.canvas.move(self.source_data['id'], bias_crd[0], bias_crd[1])

    def get_sta_comp_obj(self):
        """
        method: get the Component object connecting to the start terminal of wire
        :return: Component object
        """
        return self.comp_objs[self.source_data['sta_comp']]

    def get_end_comp_obj(self):
        """
        method: get the Component object connecting to the end terminal of wire
        :return: Component object
        """
        return self.comp_objs[self.source_data['end_comp']]

    def get_sta_tmnl_crd(self):
        """
        method: get the coordinate of the start terminal of wire
        :return: coordinate，tuple, e.g., (x, y)
        """
        return self.get_sta_comp_obj().get_tmnl_crd(self.source_data['sta_tmnl'])

    def get_end_tmnl_crd(self):
        """
        method: get the coordinate of the end terminal of wire
        :return: coordinate，tuple, e.g., (x, y)
        """
        return self.get_end_comp_obj().get_tmnl_crd(self.source_data['end_tmnl'])

    def get_mid_pcrds(self):
        """
        mdthod: get the coordinate list of the middle points on the wire
        :return: coordinate list, tuple, e.g., (x1, y1, x2, y2, ...)
        """
        mid_crds = self.source_data['mid_crds']
        if mid_crds is not None:
            return tuple(mid_crds)
        else:
            return tuple()

    def select(self, crd=None):
        """
        method: Judge if the wire itself(not including the Text) is selected by the point with coordinate of (x, y), if
        selected, self.slct = True, return True, if not selected, self.slct = True, return False, if the select
        status is changed, refresh the display once
        :param crd: coordinate, (x, y)
        :return: selected: True, not selected: False
        """
        # get the coordinate list of start point, middle point and end point
        sta_crd = self.get_sta_tmnl_crd()
        crd_lst = self.get_mid_pcrds() + self.get_end_tmnl_crd()
        # judge the select status by each line segment
        self.slct = None
        for i in range(0, int(len(crd_lst) / 2)):
            x0 = sta_crd[0]
            y0 = sta_crd[1]
            x1 = crd_lst[i * 2]
            y1 = crd_lst[i * 2 + 1]
            if y0 == y1:
                if max(x0, x1) >= crd[0] >= min(x0, x1) and y0 + 2 >= crd[1] >= y0 - 2:
                    self.slct = True
                    break
            elif x0 == x1:
                if max(y0, y1) >= crd[1] >= min(y0, y1) and x0 + 2 >= crd[0] >= x0 - 2:
                    self.slct = True
                    break
            else:
                a = (x1 - x0) / (y0 - y1)
                b = (x0 * y1 - x1 * y0) / (y0 - y1)
                if max(x0, x1) >= crd[0] >= min(x0, x1) and max(y0, y1) >= crd[1] >= min(y0, y1) and \
                        10 >= crd[0] + a * crd[1] + b >= -10:
                    self.slct = True
                    break
            sta_crd = (x1, y1)

        self.display()
        return self.slct

    def enclosed_select(self, x0, y0, x1, y1):
        """
        method: enclosed select
        :param x0:
        :param y0:
        :param x1:
        :param y1:
        :return:
        """
        # get the coordinate list of start point, middle point and end point
        crd_lst = self.get_sta_tmnl_crd() + self.get_mid_pcrds() + self.get_end_tmnl_crd()
        self.slct = None
        for i in range(0, int(len(crd_lst) / 2)):
            if min(x0, x1) < crd_lst[2 * i] < max(x0, x1) and min(y0, y1) < crd_lst[2 * i + 1] < max(y0, y1):
                pass
            else:
                return False
        self.slct = True
        return self.slct

    def get_comp_tmnl(self):
        """
        method: get component id and terminal number connecting to each terminal of the wire
        :return: ((sta_comp_id, sta_comp_tmnl), (end_comp_id, end_comp_tmnl))
        """
        return (self.source_data['sta_comp'], self.source_data['sta_tmnl']), \
               (self.source_data['end_comp'], self.source_data['end_tmnl'])


class Icon(__Element):
    """
    class: icon on the circuit
    """
    def __init__(self,
                 icon_nm,
                 source_data=None,
                 canvas=None,
                 **kwargs):
        """
        method: create a icon
        :param icon_nm: icon name
        :param source_data: source data
        :param canvas: tkinter canvas
        :param kwargs: Keyword arguments, refer to Elecpy.Default.dft_graphs_data, e.g.,
        'id': 'arrow-1',
        'crd_x': 0,
        'crd_y': 20,
        'angle': 0,
        'visible': True,
        'color': '#F64F5F'
        """
        super().__init__(default_data=default.dft_graphs_data[icon_nm],
                         source_data=source_data)
        # set the parameters
        self.set_data(canvas=canvas,
                      **kwargs)

    def display(self,
                canvas=None,
                crd_x=None,
                crd_y=None,
                angle=None):
        """
        method: display the icon
        :param canvas: tkinter canvas
        :param crd_x: coordinate x
        :param crd_y: coordinate y
        :param angle: angle
        :return: None
        """
        # set the parameters
        self.set_data(canvas=canvas,
                      crd_x=crd_x,
                      crd_y=crd_y,
                      angle=angle)
        # prepare for the display
        super().display(canvas=canvas)
        # display
        cnt_crd = (self.source_data['crd_x'], self.source_data['crd_y'])
        angle = self.source_data['angle']
        # define the line color according to the self.slct
        if self.source_data['visible']:
            if self.source_data['id'].split('-')[0] == 'arrow':
                grph_data = diagram.draw_arrow(id=self.source_data['id'],
                                               cnt_crd=cnt_crd,
                                               angle=angle,
                                               canvas=self.canvas,
                                               slct=self.slct,
                                               tail_len=self.source_data['tail_len'],
                                               arrw_len=self.source_data['arrw_len'],
                                               arrw_wid=self.source_data['arrw_wid'],
                                               color=self.source_data['color'])
            elif self.source_data['id'].split('-')[0] == 'pn':
                grph_data = diagram.draw_pn(id=self.source_data['id'],
                                            cnt_crd=cnt_crd,
                                            angle=angle,
                                            canvas=self.canvas,
                                            slct=self.slct,
                                            distance=self.source_data['distance'],
                                            size=self.source_data['size'],
                                            color=self.source_data['color'])
            else:
                raise TypeError('Unknow icon')
            self.square = grph_data['square']

    def pop_menu(self, x, y):
        """
        method: pop up menu
        :param x:
        :param y:
        :return:
        """
        self.rt_menu = tk.Menu(self.canvas, tearoff=0)
        self.rt_menu.add_command(label='Edit', command=self.edit_window)
        self.rt_menu.add_separator()
        self.rt_menu.post(x + 128, y + 88)


class SelectRectangle:
    """
    class: Rcctangle for select several elements once other than click mouse left button once by once
    """
    def __init__(self,
                 canvas=None):
        """
        init
        """
        self.canvas = canvas
        self.slct_from = (0, 0)
        self.exist = False

    def mark_start(self, x0, y0):
        """
        method: mark the start crd
        :param x0:
        :param y0:
        :return:
        """
        self.slct_from = (x0, y0)

    def draw(self, x1, y1):
        """
        method: draw rectangle
        :param x1:
        :param y1:
        :return:
        """
        self.delete()
        self.canvas.create_rectangle(self.slct_from[0], self.slct_from[1], x1, y1, tags='select_rectangle', dash=(3, 5),
                                     width=2, fill='red', stipple='gray25')
        self.exist = True

    def delete(self):
        """
        method: delete the select rectangle
        :return:
        """
        self.canvas.delete('select_rectangle')
        self.exist = False

    def move_by(self,
                bias_crd):
        """
        method:
        :param bias_crd:
        :return:
        """
        self.canvas.move('select_rectangle', bias_crd[0], bias_crd[1])


class Component:
    """
    class: Component, consist of Part, Text and Graph, e.g.,
    'resistor', 'capacitor', 'resistor', 'capacitor', 'inductor', 'diode', 'voltage_ac', 'voltage_dc', 'current_ac',
    'current_dc', 'ground', 'gap', 'vcvs', 'vccs', 'ccvs', 'cccs'
    """
    def __init__(self,
                 comp_nm,
                 source_data=None,
                 canvas=None,
                 **kwargs):
        """
        method: init Component(consist of Part, Text, Graph)
        :param comp_nm: component name, e.g.,
        'resistor', 'capacitor', 'resistor', 'capacitor', 'inductor', 'diode', 'voltage_ac', 'voltage_dc', 'current_ac',
        'current_dc', 'ground', 'gap', 'vcvs', 'vccs', 'ccvs', 'cccs'
        :param source_data: source data
        :param canvas: tkinter canvas
        :param kwargs: Keyword arguments, refer to Elecpy.Default.dft_comps_data, e.g.,
        'id': 'resistor-?',
        'designator': 'R-?',
        'value': 10.0,
        'node1': None,
        'node2': None,
        'vol_dir': 1,
        'cur_dir': 1,
        'crd_x': 60,
        'crd_y': 60,
        'angle': 0
        """
        # source data
        self.source_data = None
        # Part, Texts, Graphs
        self.part_obj = None
        self.text_objs = {}
        self.icon_objs = {}
        # create Component
        if source_data is not None:
            self.create_comp_from_data(comp_nm=comp_nm,
                                       source_data=source_data)
        else:
            # create the Part object
            part_id = self.create_part_from_default(comp_nm=comp_nm,
                                                    canvas=canvas,
                                                    **kwargs)
            # create the Text object
            self.create_text_from_default(part_id=part_id,
                                          canvas=canvas)
            # create the Graph object for voltage symbol
            self.create_volsym_from_default(part_id=part_id,
                                            canvas=canvas)
            # create the Graph object for current symbol
            self.create_cursym_from_default(part_id=part_id,
                                            canvas=canvas)
            # get the source data
            self.source_data = {'part_data': self.part_obj.get_data(),
                                'texts_data': {'default': self.text_objs['default'].get_data()},
                                'grphs_data': {'dft_vol': self.icon_objs['dft_vol'].get_data(),
                                               'dft_cur': self.icon_objs['dft_cur'].get_data()}}

        # select status
        self.slct = {'part': False, 'text': '', 'grph': ''}
        # class for manipulating the file
        self.__file = file.File()
        # mouse right button's pop up menu, tk.Menu
        self.rt_menu = None

    def create_comp_from_data(self,
                              comp_nm,
                              source_data,
                              canvas=None):
        """
        method: create component(consist of Text, Part) from source data
        :param comp_nm: component name
        :param source_data: source data
        :param canvas: tkinter canvas
        :return: None
        """
        # pass the source_data
        self.source_data = source_data
        # create the Part object
        self.part_obj = Part(part_nm=comp_nm,
                             source_data=source_data['part_data'],
                             canvas=canvas)
        # create the Text object
        for key in source_data['texts_data']:
            self.text_objs[key] = Text(source_data=source_data['texts_data'][key],
                                       canvas=canvas)
        # create the Graph object
        for key in source_data['grphs_data']:
            self.icon_objs[key] = Icon(icon_nm=source_data['grphs_data'][key]['id'].split('-')[0],
                                       source_data=source_data['grphs_data'][key],
                                       canvas=canvas)

    def create_part_from_default(self,
                                 comp_nm,
                                 canvas=None,
                                 **kwargs):
        """
        method: create Part object from default data
        :param comp_nm: component name
        :param canvas: tkinter canvas
        :param kwargs: Keyword arguments, refer to Elecpy.Default.dft_comps_data, e.g.,
        'id': 'resistor-?',
        'designator': 'R-?',
        'value': 10.0,
        'node1': None,
        'node2': None,
        'vol_dir': 1,
        'cur_dir': 1,
        'crd_x': 60,
        'crd_y': 60,
        'angle': 0
        :return: part's id
        """
        self.part_obj = Part(comp_nm,
                             canvas=canvas,
                             **kwargs)
        return self.part_obj.get_data(key='id')

    def create_text_from_default(self,
                                 part_id,
                                 canvas=None):
        """
        method: create Text object for the component
        :param part_id: id of the Part object
        :param canvas: tkinter canvas
        :return: None
        """
        self.text_objs['default'] = Text(canvas=canvas,
                                         id='default-' + part_id,
                                         content=self.part_obj.get_data('designator') + '\n' +
                                                 self.part_obj.get_value_formula(),
                                         crd_x=self.part_obj.get_data('crd_x'),
                                         crd_y=self.part_obj.get_data('crd_y') - 30)

    def create_volsym_from_default(self,
                                   part_id,
                                   canvas=None):
        """
        method: create Graph object for the component's voltage symbol
        :param part_id: id of the Part object
        :param canvas: tkinter canvas
        :return: None
        """
        # set the direction of arrow symbol, i.e., reference current
        vol_agl = self.part_obj.get_data('angle') + 90 - 90 * self.part_obj.source_data['vol_dir']
        # set the direction of positive-negative symbol, i.e., reference voltage
        self.icon_objs['dft_vol'] = Icon(icon_nm='pn',
                                         canvas=canvas,
                                         id='pn-' + part_id,
                                         crd_x=self.part_obj.get_data('crd_x'),
                                         crd_y=self.part_obj.get_data('crd_y') + 10,
                                         angle=vol_agl)
        # if the component is ground, the voltage symbol is invisible
        if part_id.split('-')[0] == 'ground':
            self.icon_objs['dft_vol'].set_data(visible=False)

    def create_cursym_from_default(self,
                                   part_id,
                                   canvas=None):
        """
        method: create Graph object for the component's current symbol
        :param part_id: id of the Part object
        :param canvas: tkinter canvas
        :return: None
        """
        # set the direction of arrow symbol, i.e., reference current
        cur_agl = self.part_obj.get_data('angle') + 90 - 90 * self.part_obj.source_data['cur_dir']

        self.icon_objs['dft_cur'] = Icon(icon_nm='arrow',
                                         canvas=canvas,
                                         id='arrow-' + part_id,
                                         crd_x=self.part_obj.get_data('crd_x'),
                                         crd_y=self.part_obj.get_data('crd_y') + 30,
                                         angle=cur_agl)
        # if the component is ground, the current symbol is invisible
        if part_id.split('-')[0] == 'ground':
            self.icon_objs['dft_cur'].set_data(visible=False)

    def open(self,
             path=None,
             file=None):
        """
        method: open a component file(.cmp), pass the data to self.source_data
        :param path: file's path, e.g., 'E:/../'
        :param file: file's name, e.g., 'xxx.cmp'
        :return: None
        """
        # read .cmp file,
        source_data = self.__file.open_cmpfile(path, file)
        comp_nm = source_data['part_data']['id'].split('-')[0]
        # create Component from data
        self.create_comp_from_data(comp_nm=comp_nm,
                                   source_data=source_data)

    def save(self,
             filepath=None,
             overwrite=False):
        """
        method: save self.source_data to filepath, it obeys rules below:
        if filepath is given, self.source_data will be saved to filepath, if the filepath is already exist, the filepath
        will be replaced.
        if filepath is default and self.source_data is read from file xxx.cmp, self.source_data will be saved to file
        xxx.cmp.
        if filepath is default and self.source_data is not from any file, an error will occur.
        :param filepath: file path and file, e.g., 'E:/.../xxx.cmp'
        :param overwrite: if the file can be overwritten.
        When the filepath is already existed, if overwrite is True, overwritten to filepath will occur,
        otherwise, nothing will be done.
        :return: None
        """
        # save self.source_data to file
        self.__file.save_cmpfile(self.source_data, filepath, overwrite=overwrite)

    def set_data(self,
                 text_key=None,
                 grph_key=None,
                 part=None,
                 **kwargs):
        """
        method: set Component's data, including data of Part, data of Texts or data of Graph.
        text_key determines which Text will be modifid, grph_key determins which Graph will be modified, part determines
        whether the Part will be modified.
        If text_key, grph_key and part are all default, it is self.slct which determines which Text or which Graph or
        whether the Part will be modified.
        If text_key is not None, no matter grph_key and part is None or not, Text and Part will not be modified.
        If text_key is None and grph_key is not None, no matter part is None or not, Part will not be modified.
        If text_key and grph_key is both None, Part will be modified if part is not valid.
        If self.slct is empty, then nothing will be done.
        :param text_key: Text's key in self.text_objs
        :param grph_key: Graph's key in self.grph_objs
        :param part: flag determines whether the Part will be modified.
        :param kwargs: source_data of Part or Text or Graph, determined by part or text_key or grph_key
        :return: None
        """
        # if text_key, grph_key or part is default, self.slct will take charge.
        if text_key is None:
            text_key = self.slct['text']
        elif grph_key is None:
            grph_key = self.slct['grph']
        elif part is None:
            part = self.slct['part']

        # set data
        if text_key:
            self.set_text_data(text_key=text_key,
                               **kwargs)
        elif grph_key:
            self.set_graph_data(grph_key=grph_key,
                                **kwargs)
        elif part:
            self.set_part_data(**kwargs)

    def delete(self,
               text_key=None,
               grph_key=None):
        """
        method: Delete Text or Graph of this Component.
        text_key and grph_key determine which Text and Graph will be deleted.
        The default Text and Graph can not be deleted.
        If text_key and grph_key is both default, it is self.slct which determines which Text or Graph will be deleted.
        If self.slct is empty, nothing will be done.
        :param text_key: Text's key in self.text_objs
        :param grph_key: Graph's key in self.grph_objs
        :return: None
        """
        # if text_key or grph_key is default, self.slct will take charge.
        if text_key is None:
            text_key = self.slct['text']
        elif grph_key is None:
            grph_key = self.slct['grph']

        if text_key:
            if text_key != 'default':
                self.text_objs[text_key].clear()
                self.text_objs.pop(text_key)
                self.source_data['texts_data'].pop(text_key)
        elif grph_key:
            if grph_key != 'dft_vol' and grph_key != 'dft_cur':
                self.text_objs.pop(grph_key)
                self.source_data['grphs_data'].pop(grph_key)

    def set_part_data(self,
                      tmnls_vol=None,
                      cur=None,
                      canvas=None,
                      **kwargs):
        """
        method: set part's parameters
        :param tmnls_vol: terminals voltage, V, e.g., [0.0, 0.0](resistor, capactor,..), [0.0, 0.0, 0.0, 0.0]
        (transformer)
        :param cur: part's current, A, 0.0
        :param canvas: tkinter canvas
        :param kwargs: Keyword arguments, refer to Elecpy.Default.dft_comps_data, e.g.,
        'id': 'resistor-?',
        'designator': 'R-?',
        'value': 10.0,
        'node1': None,
        'node2': None,
        'vol_dir': 1,
        'cur_dir': 1,
        'crd_x': 60,
        'crd_y': 60,
        'angle': 0
        :return: None
        """
        # only when the part hasn't displayed, can the id be modified.
        if self.part_obj.canvas is not None and 'id' in kwargs.keys():
            print('Edition of id is not permitted!!')
            kwargs.pop('id')
        self.part_obj.set_data(tmnls_vol=tmnls_vol,
                               cur=cur,
                               canvas=canvas,
                               **kwargs)

        # if the part id is modified, the text and icon need to be modified consequently.
        if 'id' in kwargs.keys():
            self.text_objs['default'].set_data(id='default-' + self.source_data['part_data']['id'])
            self.icon_objs['dft_vol'].set_data(id='pn-' + self.source_data['part_data']['id'])
            self.icon_objs['dft_cur'].set_data(id='arrow-' + self.source_data['part_data']['id'])

        if 'value' in kwargs.keys():
            self.text_objs['default'].set_data(content=self.part_obj.get_data('designator') + '\n' +
                                                        self.part_obj.get_value_formula())

        # if the designator is modified, the text need to be modified consequently
        if 'designator' in kwargs.keys():
            self.text_objs['default'].set_data(content=self.part_obj.get_data('designator') + '\n' +
                                                        self.part_obj.get_value_formula())

    def set_text_data(self,
                      text_key=None,
                      **kwargs):
        """
        method: set Component's Text's part parameters, i.e., visible、content、font_family、font_size、font_weight、
        font_slant、font_underline、font_overstrike.
        :param text_key: key in self.text_objs, if default, set the selected Text, if no selected Text, do nothing.
        :param kwargs: Keyword arguments, refer to Elecpy.Default.dft_text_data, e.g.,
        'crd_x': 0,
        'crd_y': 20,
        'angle': 0,
        'color': black,
        'visible': True,
        'content': 'text',
        'font_family': 'Times',
        'font_size': '8',
        'font_weight': 'bold',
        'font_slant': 'roman',
        'font_underline': 0,
        'font_overstrike': 0
        :return: None
        """
        # get the text_key
        if text_key is None:
            text_key = self.slct['text']

        # judge text_key, when text_key exist and is not 'default', set it's data
        if text_key is None:
            print("No Component's Text object is selected!")
            return
        else:
            legal_key = {}
            for key in kwargs:
                if key == 'crd_x' or key == 'crd_y' or key == 'angle' or key == 'color' or key == 'visible' \
                        or key == 'content' or key == 'font_family' or key == 'font_size' or key == 'font_weight' \
                        or key == 'font_slant' or key == 'font_underline' or key == 'font_overstrike':
                    legal_key[key] = kwargs[key]
            self.text_objs[text_key].set_data(**legal_key)

    def set_graph_data(self,
                       grph_key=None,
                       **kwargs):
        """
        method: set Component's Graph's part parameters, 
        :param grph_key: key in self.grph_objs, if default, set the selected Graph, if no selected Graph, do nothing.
        :param kwargs: Keyword arguments, refer to Elecpy.Default.dft_graphs_data, e.g.,
        'visible': True,
        'color': '#F64F5F'
        :return: None
        """
        if grph_key is None:
            grph_key = self.slct['grph']
        if grph_key is None:
            print("No component's Graph object is selected!")
            return
        self.icon_objs[grph_key].set_data(**kwargs)

    def get_data(self,
                 key=None):
        """
        method: Get data of Component. key is self.source_data's key. When key is default, return self.source_data.
        :param key: key of self.source_data. e.g., 'part_data', 'texts_data', 'grphs_data'
        :return: self.source_data or self.source_data[key]
        """
        # if key is None, return self.source_data
        if key is None:
            return self.source_data
        # if key is not None, return self.source_data[key]
        else:
            if key in self.source_data.keys():
                return self.source_data[key]
            else:
                print('This data is not exist!')
                return None

    def get_elm_data(self):
        """
        method: get data of Component's one element, i.e., Part or Text or Graph. self.slct determines which Text or
        which Graph or whether Part will be the element.
        :return: data of one element，dict, e.g., {'id': , 'crd_x': , 'crd_y': ,..}
        """
        if self.slct['text']:
            return self.text_objs[self.slct['text']].get_data()
        elif self.slct['grph']:
            return self.icon_objs[self.slct['grph']].get_data()
        elif self.slct['part']:
            return self.part_obj.get_data()
        else:
            return None

    def add_text(self,
                 **kwargs):
        """
        method: Add a Text.
        :param kwargs: Keyword arguments, refer to Elecpy.Default.dft_text_data, e.g.,
        'id': 'text-1',
        'crd_x': 0,
        'crd_y': 20,
        'angle': 0,
        'visible': True,
        'content': 'text',
        'font_family': 'Times',
        'font_size': '8',
        'font_weight': 'bold',
        'font_slant': 'roman',
        'font_underline': 0,
        'font_overstrike': 0
        :return: None
        """
        # get the parameters of the Text object
        crd_x = self.part_obj.get_data('crd_x') + 20
        crd_y = self.part_obj.get_data('crd_y')
        num = len(self.text_objs)
        crd_y += (num + 1) * 20
        if 'id' not in kwargs.keys():
            text_id = 'text' + str(num)
        else:
            text_id = kwargs['id']
        if 'content' not in kwargs.keys():
            content = 'text'
        else:
            content = kwargs['content']

        # create a Text object
        self.text_objs[text_id] = Text(canvas=self.part_obj.canvas, id=text_id, crd_x=crd_x, crd_y=crd_y,
                                       content=content)
        # add source_data of Text to the self.source_data
        self.source_data['texts_data'][text_id] = self.text_objs[text_id].get_data()
        # display the new Text
        self.text_objs[text_id].display()

    def display(self,
                canvas=None,
                crd_x=None,
                crd_y=None,
                angle=None):
        """
        method: display the Component, including Part, Texts and Graphs
        :param canvas: tkinter canvas
        :param crd_x: coordinate x
        :param crd_y: coordinate y
        :param angle: angle
        :return: None
        """
        # get the previous coordinate of the part
        part_crd_x = self.part_obj.get_data(key='crd_x')
        part_crd_y = self.part_obj.get_data(key='crd_y')
        # set the parameters
        self.set_part_data(canvas=canvas,
                           crd_x=crd_x,
                           crd_y=crd_y,
                           angle=angle)
        # get the current coordinate of the part
        crd_x = self.part_obj.get_data(key='crd_x')
        crd_y = self.part_obj.get_data(key='crd_y')
        # display
        self.part_obj.display(canvas, crd_x, crd_y, angle)
        for key in self.text_objs:
            bias_x = self.text_objs[key].get_data(key='crd_x') - part_crd_x
            bias_y = self.text_objs[key].get_data(key='crd_y') - part_crd_y
            self.text_objs[key].display(canvas, crd_x + bias_x, crd_y + bias_y, angle)
        for key in self.icon_objs:
            bias_x = self.icon_objs[key].get_data(key='crd_x') - part_crd_x
            bias_y = self.icon_objs[key].get_data(key='crd_y') - part_crd_y
            self.icon_objs[key].display(canvas, crd_x + bias_x, crd_y + bias_y, angle)

    def clear(self):
        """
        method: clear the display of the Component.
        """
        self.part_obj.clear()
        for key in self.text_objs:
            self.text_objs[key].clear()
        for key in self.icon_objs:
            self.icon_objs[key].clear()

    def select(self,
               crd=None):
        """
        method: Judge whether the Part is selected, or which Text or Graph is selected by crd(crd_x, crd_y).
        When any Element(Part, Text or Graph) in Component is selected, return True, otherwise, return False.
        self.slct will indicate whether the Part is selected, or which Text or Graph is selected.
        e.g., self.slct = {'part': True, 'text': '', 'grph': ''} means the Part is selected.
        self.slct = {'part': False, 'text': 'Default', 'grph': ''} means the self.text_objs['Default'] is selected.
        self.slct = {'part': False, 'text': '', 'grph': 'dft_vol'} means the self.grph_objs['dft_vol'] is selected.
        etc..
        :param crd: coordinate of the point
        :return: selected：True, not selected: False
        """
        # judge if any Text is selected
        self.slct['text'] = ''
        for key in self.text_objs:
            if self.text_objs[key].select(crd):
                self.slct['text'] = key
                return True
        # if no Text is selected, judge if any Graph is selected
        self.slct['grph'] = ''
        for key in self.icon_objs:
            if self.icon_objs[key].select(crd):
                self.slct['grph'] = key
                return True
        # if no Text and Graph is selected, judge if Part is selected
        self.slct['part'] = self.part_obj.select(crd)
        return self.slct['part']

    def enclosed_select(self, x0, y0, x1, y1):
        """
        method: enclosed select
        :param x0:
        :param y0:
        :param x1:
        :param y1:
        :return:
        """
        # if no Text and Graph is selected, judge if Part is selected
        self.slct['part'] = self.part_obj.enclosed_select(x0, y0, x1, y1)
        return self.slct['part']

    def move_to(self,
                to_crd=None):
        """
        method: move Component to to_crd
        :param to_crd: destination location coordinate
        """
        # capture the destination location coordinate
        if self.slct['part']:
            to_crd = tools.point_capture(to_crd)
        if to_crd:
            # calculate the bias
            x_bias = to_crd[0] - self.part_obj.get_data('crd_x')
            y_bias = to_crd[1] - self.part_obj.get_data('crd_y')
            # move the Element(Text, Graph or Part) selected to to_crd
            if self.slct['text']:
                self.text_objs[self.slct['text']].move_to(to_crd)
            elif self.slct['grph']:
                self.icon_objs[self.slct['grph']].move_to(to_crd)
            elif self.slct['part']:
                self.part_obj.move_to(to_crd)
                for key in self.text_objs:
                    txt_to_crd = (self.text_objs[key].get_data('crd_x') + x_bias,
                                  self.text_objs[key].get_data('crd_y') + y_bias)
                    self.text_objs[key].move_to(txt_to_crd)
                for key in self.icon_objs:
                    gph_to_crd = (self.icon_objs[key].get_data('crd_x') + x_bias,
                                  self.icon_objs[key].get_data('crd_y') + y_bias)
                    self.icon_objs[key].move_to(gph_to_crd)

    def move_by(self, bias_crd):
        """
        method: move by bias_crd
        :param bias_crd:
        :return:
        """
        # move the Element(Text, Graph or Part) by bias_crd
        if self.slct['text']:
            self.text_objs[self.slct['text']].move_by(bias_crd)
        elif self.slct['grph']:
            self.icon_objs[self.slct['grph']].move_by(bias_crd)
        elif self.slct['part']:
            self.part_obj.move_by(bias_crd)
            for key in self.text_objs:
                self.text_objs[key].move_by(bias_crd)
            for key in self.icon_objs:
                self.icon_objs[key].move_by(bias_crd)

    def rotate(self):
        """
        method: clockwise rotate Component if the Part is selected which is determined by self.slct['part']. If
        self.slct is empty, nothing will be done.
        :return: None
        """
        # only the Component itself can be rotate(when the Part is selected).
        if self.slct['part']:
            self.part_obj.rotate()

            # the default Graph for symbol of voltage and current reference direction must be rotated and moved to
            # maintain the correct location.
            self.icon_objs['dft_vol'].rotate()
            cnt_x, cnt_y = tools.coord_mirr_rota(orig_crd=(self.icon_objs['dft_vol'].source_data['crd_x'],
                                                           self.icon_objs['dft_vol'].source_data['crd_y']),
                                                 cnt_crd=(self.part_obj.source_data['crd_x'],
                                                          self.part_obj.source_data['crd_y']),
                                                 angle=90)
            self.icon_objs['dft_vol'].move_to(to_crd=(cnt_x, cnt_y))

            self.icon_objs['dft_cur'].rotate()
            cnt_x, cnt_y = tools.coord_mirr_rota(orig_crd=(self.icon_objs['dft_cur'].source_data['crd_x'],
                                                           self.icon_objs['dft_cur'].source_data['crd_y']),
                                                 cnt_crd=(self.part_obj.source_data['crd_x'],
                                                          self.part_obj.source_data['crd_y']),
                                                 angle=90)
            self.icon_objs['dft_cur'].move_to(to_crd=(cnt_x, cnt_y))

    def reverse_ref_dir(self):
        """
        method: reverse the reference direction of voltage or current
        :return: None
        """
        # if Graph is selected
        if self.slct['grph']:
            # if self.grph_objs['dft_vol'] is selected, modify source_data
            if self.slct['grph'] == 'dft_vol':
                self.source_data['part_data']['vol_dir'] *= -1
            # if self.grph_objs['dft_cur'] is selected, modify source_data
            elif self.slct['grph'] == 'dft_cur':
                self.source_data['part_data']['cur_dir'] *= -1
            # rotate the Graph twice, just like reverse the direction.
            self.icon_objs[self.slct['grph']].rotate()
            self.icon_objs[self.slct['grph']].rotate()

    def tmnl_select(self,
                    crd):
        """
        method: judge if the terminal is selected by the point with coordinate of crd, if selected, return the terminal
        number, if not selected, return False
        :param crd: coordinate of the point, (crd_x, crd_y)
        :return: selected: terminal number, e.g., 1, 2, not selected: False
        """
        return self.part_obj.tmnl_select(crd)

    def get_tmnl_crd(self,
                     tmnl):
        """
        method: get coordinate of the terminal
        :param tmnl: terminal number, e.g., 1, 2
        :return: coordinate, i.e., (crd_x, crd_y)
        """
        return self.part_obj.get_tmnl_crd(tmnl)

    def get_tmnl_net(self,
                     tmnl):
        """
        method: get net id of the terminal
        :param tmnl: terminla number, e.g. 1, 2
        :return: net id, e.g., 1, 2, etc..
        """
        return self.part_obj.get_tmnl_net(tmnl)

    def edit_window(self):
        """
        method: create a edit window, used for GUI
        :return: None
        """
        if self.slct['text']:
            self.text_objs[self.slct['text']].edit_window(nonedit=['content', 'visible'])
        elif self.slct['grph']:
            self.icon_objs[self.slct['grph']].edit_window(nonedit=['content', 'visible'])
        elif self.slct['part']:
            edit_data = self.part_obj.editable_data()
            edit_win = gui_elements.EditWin(data=edit_data)

            def func_save():
                """
                func: "save" function
                :return: None
                """
                edit_win.destroy()
                self.set_data(part=True,
                              **edit_win.page.data)
                self.display()

            edit_win.command(func_save=func_save)
            edit_win.mainloop()

    def common_pop_menu(self):
        """
        method: common pop menu
        :return:
        """
        self.rt_menu = tk.Menu(self.part_obj.canvas, tearoff=0)
        self.rt_menu.add_command(label='Edit', command=self.edit_window)
        self.rt_menu.add_separator()

    def part_pop_menu(self, x, y):
        """
        method: part pop menu
        :param x: crd x
        :param y: crd y
        :return: None
        """
        self.common_pop_menu()
        ref_vol_visible = tk.IntVar(value=self.icon_objs['dft_vol'].get_data('visible'))

        def set_refvol_visible():
            """func: set the reference direction of voltage's visible"""
            if ref_vol_visible.get():
                self.set_graph_data(grph_key='dft_vol', visible=True)
            else:
                self.set_graph_data(grph_key='dft_vol', visible=False)
            self.icon_objs['dft_vol'].display()

        self.rt_menu.add_checkbutton(label='ref_vol', variable=ref_vol_visible, command=set_refvol_visible)

        ref_cur_visible = tk.IntVar(value=self.icon_objs['dft_cur'].get_data('visible'))

        def set_refcur_visible():
            """func: set the reference direction of current's visible"""
            if ref_cur_visible.get():
                self.set_graph_data(grph_key='dft_cur', visible=True)
            else:
                self.set_graph_data(grph_key='dft_cur', visible=False)
            self.icon_objs['dft_cur'].display()

        self.rt_menu.add_checkbutton(label='ref_cur', variable=ref_cur_visible, command=set_refcur_visible)
        self.rt_menu.add_separator()

        self.rt_menu.post(x + 128, y + 88)

    def text_pop_menu(self, x, y):
        """
        method: text pop menu
        :param x: crd x
        :param y: crd y
        :return:
        """
        self.common_pop_menu()
        self.rt_menu.post(x + 128, y + 88)

    def grph_pop_menu(self, x, y):
        """
        method: icon pop menu
        :param x: crd x
        :param y: crd y
        :return:
        """
        self.common_pop_menu()
        self.rt_menu.post(x + 128, y + 88)

    def pop_menu(self, x, y):
        """
        method: mouse right button pop up menu
        :return: None
        """
        if self.slct['part']:
            self.part_pop_menu(x, y)
        elif self.slct['text']:
            self.text_pop_menu(x, y)
        elif self.slct['grph']:
            self.grph_pop_menu(x, y)


class Connector:
    """
    class: Connector, consist of Wire and Text
    """
    def __init__(self,
                 source_data=None,
                 comp_objs=None,
                 canvas=None,
                 **kwargs):
        """
        method: init Connector
        :param source_data: source data of Connector
        :param comp_objs: Component objects, used for implementing the function that the Connector follows the component
        which moves, e.g., {'comp_id1': Component,..}
        :param canvas: tkinter canvas
        :parma kwargs: Keyword arguments, refer to Elecpy.Default.dft_wire_data, e.g.,
        'id': 'wire-1',
        'designator': 'w-?',
        'net_id': '1',
        'sta_comp': component's id, e.g., 'resistor-1',
        'sta_tmnl': terminal number, e.g. 1, 2,
        'end_comp': component's id, e.g., 'resistor-1',
        'end_tmnl': terminal number, e.g. 1, 2,
        'mid_crds': None or middle points' coordinate, list, i.e., [x1, y1, x2, y2, ...]， e.g., [10, 10, 20, 20]
        """
        # source data
        self.source_data = None
        # Wire, Texts
        self.wire_obj = None
        self.text_objs = {}
        # create Connector
        if source_data:
            self.create_conn_from_data(source_data=source_data,
                                       comp_objs=comp_objs,
                                       canvas=canvas)
        else:
            self.create_conn_from_default(comp_objs=comp_objs,
                                          canvas=canvas,
                                          **kwargs)

        # select status
        self.slct = {'wire': False, 'text': ''}

    def create_conn_from_data(self,
                              source_data,
                              comp_objs,
                              canvas=None):
        """
        method: create connector from data
        :param source_data: source data
        :param comp_objs: Component objects, used for implementing the function that the Connector follows the component
        which moves, e.g., {'comp_id1': Component,..}
        :param canvas: tkinter canvas
        :return: None
        """
        self.source_data = source_data
        self.wire_obj = Wire(source_data=source_data['wire_data'], comp_objs=comp_objs, canvas=canvas)
        for key in source_data['texts_data']:
            self.text_objs[key] = Text(source_data=source_data['texts_data'][key], canvas=canvas)

    def create_conn_from_default(self,
                                 comp_objs=None,
                                 canvas=None,
                                 **kwargs):
        """
        method: create connector from default
        :param comp_objs: Component objects, used for implementing the function that the Connector follows the component
        which moves, e.g., {'comp_id1': Component,..}
        :param canvas: tkinter canvas
        :parma kwargs: Keyword arguments, refer to Elecpy.Default.dft_wire_data, e.g.,
        'id': 'wire-1',
        'designator': 'w-?',
        'net_id': '1',
        'sta_comp': component's id, e.g., 'resistor-1',
        'sta_tmnl': terminal number, e.g. 1, 2,
        'end_comp': component's id, e.g., 'resistor-1',
        'end_tmnl': terminal number, e.g. 1, 2,
        'mid_crds': None or middle points' coordinate, list, i.e., [x1, y1, x2, y2, ...]， e.g., [10, 10, 20, 20]
        :return: None
        """
        self.wire_obj = Wire(comp_objs=comp_objs, canvas=canvas, **kwargs)
        self.text_objs['default'] = Text(id='default-' + self.wire_obj.get_data(key='id'),
                                         content=self.wire_obj.get_data(key='id'),
                                         visible=False)
        self.source_data = {'wire_data': self.wire_obj.get_data(),
                            'texts_data': {'default': self.text_objs['default'].get_data()}}

    def set_wire_data(self,
                      comp_objs=None,
                      wire_vol=None,
                      wire_cur=None,
                      canvas=None,
                      **kwargs):
        """
        method: Set the parameters of Wire
        :param comp_objs: Component objects, used for implementing the function that the Connector follows the component
        which moves, e.g., {'comp_id1': Component,..}
        :param wire_vol: wire voltage with unit of V, float, e.g., 10.0
        :param wire_cur: wire current with unit of A, float, e.g., 1.0
        :param canvas: tkinter canvas
        :parma kwargs: Keyword arguments, refer to Elecpy.Default.dft_wire_data, e.g.,
        'id': 'wire-1',
        'designator': 'w-?',
        'net_id': '1',
        'sta_comp': component's id, e.g., 'resistor-1',
        'sta_tmnl': terminal number, e.g. 1, 2,
        'end_comp': component's id, e.g., 'resistor-1',
        'end_tmnl': terminal number, e.g. 1, 2,
        'mid_crds': None or middle points' coordinate, list, i.e., [x1, y1, x2, y2, ...]， e.g., [10, 10, 20, 20]
        :return: None
        """
        # only when the part hasn't displayed, can the id be modified.
        if self.wire_obj.canvas is not None and 'id' in kwargs.keys():
            print('Edition of id is not permitted!!')
            kwargs.pop('id')
        self.wire_obj.set_data(comp_objs=comp_objs,
                               wire_vol=wire_vol,
                               wire_cur=wire_cur,
                               canvas=canvas,
                               **kwargs)
        # if the part id is modified, the text need to be modified consequently.
        if 'id' in kwargs.keys():
            self.text_objs['default'].set_data(id='default' + kwargs['id'],
                                               content=self.source_data['wire_data']['id'])

    def set_text_data(self,
                      text_key,
                      **kwargs):
        """
        method: set Connector's Text's part parameters, i.e., visible、content、font_family、font_size、font_weight、
        font_slant、font_underline、font_overstrike.
        :param text_key: key in self.text_objs, if default, set the selected Text, if no selected Text, do nothing.
        :param kwargs: Keyword arguments, refer to Elecpy.Default.dft_text_data, e.g.,
        'crd_x': 0,
        'crd_y': 20,
        'angle': 0,
        'color': black,
        'visible': True,
        'content': 'text',
        'font_family': 'Times',
        'font_size': '8',
        'font_weight': 'bold',
        'font_slant': 'roman',
        'font_underline': 0,
        'font_overstrike': 0
        :return:
        """
        # if text_key is default, self.slct will take charge.
        if text_key is None:
            text_key = self.slct['text']

        # judge text_key, when text_key exist and is not 'default', set it's data
        if text_key is None:
            print("No Connector's Text object is selected!")
            return
        else:
            legal_key = {}
            for key in kwargs:
                if key == 'crd_x' or key == 'crd_y' or key == 'angle' or 'color' or 'visible' or key == 'content' \
                        or key == 'font_family' or key == 'font_size' or key == 'font_weight' or key == 'font_slant'\
                        or key == 'font_underline' or key == 'font_overstrike':
                    legal_key[key] = kwargs[key]
            self.text_objs[text_key].set_data(**legal_key)

    def add_comp_tmnl(self,
                      sta_comp=None,
                      sta_tmnl=None,
                      end_comp=None,
                      end_tmnl=None):
        """
        method: Add a Component's key in self.comp_objs and its terminal number to the start terminal or end terminal of
        Wire.
        :param sta_comp: start Component's key, e.g., 'resistor-1', 'capacitor-1', etc,..
        :param sta_tmnl: terminal's number
        :param end_comp: end Component's key, e.g., 'resistor-1', 'capacitor-1', etc,..
        :param end_tmnl: terminal's number
        :return: None
        """
        self.wire_obj.add_comp_tmnl(sta_comp=sta_comp,
                                    sta_tmnl=sta_tmnl,
                                    end_comp=end_comp,
                                    end_tmnl=end_tmnl)

    def delete(self,
               text_key=None):
        """
        method: Delete Text of this Connector.
        text_key determine which Text will be deleted.
        The default Text can not be deleted.
        If text_key is default, it is self.slct which determines which Text will be deleted.
        If self.slct is empty, nothing will be done.
        :param text_key: Text's key in self.text_objs
        :return: None
        """
        # if text_key is default, self.slct will take charge.
        if text_key is None:
            text_key = self.slct['text']

        if text_key:
            if text_key != 'default':
                self.text_objs[text_key].clear()
                self.text_objs.pop(text_key)
                self.source_data['texts_data'].pop(text_key)

    def get_data(self,
                 key=None):
        """
        method: Get data of Connector. key is self.source_data's key. When key is default, return self.source_data.
        :param key: key of self.source_data.
        :return: self.source_data or self.source_data[key]
        """
        # if key is None, return self.source_data
        if key is None:
            return self.source_data
        # if key is not None, return self.source_data[key]
        else:
            if key in self.source_data.keys():
                return self.source_data[key]
            else:
                print('This data is not exist!')
                return None

    def add_text(self,
                 **kwargs):
        """
        method: Add a Text.
        :param kwargs: Keyword arguments, refer to Elecpy.Default.dft_text_data, e.g.,
        'id': 'text-1',
        'crd_x': 0,
        'crd_y': 20,
        'angle': 0,
        'visible': True,
        'content': 'text',
        'font_family': 'Times',
        'font_size': '8',
        'font_weight': 'bold',
        'font_slant': 'roman',
        'font_underline': 0,
        'font_overstrike': 0
        :return: None
        """
        # get the parameters of the Text object
        num = len(self.text_objs)
        crd_x = self.text_objs['default'].get_data('crd_x')
        crd_y = self.text_objs['default'].get_data('crd_y') + (num + 1) * 10
        if 'id' not in kwargs.keys():
            text_id = 'text' + str(num)
        else:
            text_id = kwargs['id']

        # create a Text object
        self.text_objs[text_id] = Text(id=text_id,
                                       crd_x=crd_x,
                                       crd_y=crd_y)
        # add source_data of Text to the self.source_data
        self.source_data['texts_data'][text_id] = self.text_objs[text_id].get_data()
        # display the new Text
        self.text_objs[text_id].display()

    def display(self,
                canvas=None):
        """
        method: display the Connector, including Wire and Texts
        :param canvas: tkinter canvas
        :return: None
        """
        self.wire_obj.display(canvas=canvas)
        for key in self.text_objs:
            self.text_objs[key].display(canvas=canvas)

    def move_by(self,
                bias_crd):
        """
        method:
        :param bias_crd:
        :return:
        """
        # move the Element(Text, Graph or Part) by bias_crd
        if self.slct['text']:
            self.text_objs[self.slct['text']].move_by(bias_crd)
        elif self.slct['wire']:
            self.wire_obj.move_by(bias_crd)
            for key in self.text_objs:
                self.text_objs[key].move_by(bias_crd)

    def clear(self):
        """
        method: clear the display of the Connector.
        """
        self.wire_obj.clear()
        for key in self.text_objs:
            self.text_objs[key].clear()

    def select(self,
               crd=None):
        """
        method: Judge whether the Wire is selected, or which Text is selected by crd(crd_x, crd_y).
        When any Element(Wire or Text) in Connector is selected, return True, otherwise, return False.
        self.slct will indicate whether the Part is selected, or which Text or Graph is selected.
        e.g., self.slct = {'wire': True, 'text': ''} means the Wire is selected.
        self.slct = {'wire': False, 'text': 'Default',} means the self.text_objs['Default'] is selected.
        etc..
        :param crd: coordinate of the point
        :return: selected：True, not selected: False
        """
        # judge if any Text is selected
        self.slct['text'] = ''
        for key in self.text_objs:
            if self.text_objs[key].select(crd):
                self.slct['text'] = key
                return True
        # if no Text is selected, judge if Part is selected
        self.slct['wire'] = self.wire_obj.select(crd)
        return self.slct['wire']

    def enclosed_select(self, x0, y0, x1, y1):
        """
        method:
        :param x0:
        :param y0:
        :param x1:
        :param y1:
        :return:
        """
        self.slct['wire'] = self.wire_obj.enclosed_select(x0, y0, x1, y1)
        return self.slct['wire']

    def move_to(self,
                to_crd=None):
        """
        method: move Text of Connector to to_crd
        :param to_crd: destination location coordinate
        """
        # capture the destination location coordinate
        if self.slct['wire']:
            to_crd = tools.point_capture(to_crd)
        # move the Text selected to to_crd
        if self.slct['text']:
            self.text_objs[self.slct['text']].move_to(to_crd)

    def tmnl_select(self,
                    crd):
        """
        method: judge if the terminal is selected by the point with coordinate of crd, if selected, return the terminal
        number, if not selected, return False
        :param crd: coordinate of the point, (crd_x, crd_y)
        :return: selected: terminal number, e.g., 1, 2, not selected: False
        """
        return self.wire_obj.tmnl_select(crd)

    def get_comp_tmnl(self):
        """
        method: get component id and terminal number connecting to each terminal of the wire
        :return: ((sta_comp_id, sta_comp_tmnl), (end_comp_id, end_comp_tmnl))
        """
        return self.wire_obj.get_comp_tmnl()

    def get_sta_comp(self):
        """
        method: get start component id
        :return: sta_comp_id, e.g., 'capacitor-2'
        """
        return self.get_comp_tmnl()[0][0]

    def get_sta_tmnl(self):
        """
        method: get start component's terminal number
        :return: sta_comp_tmnl, e.g., 1, 2
        """
        return self.get_comp_tmnl()[0][1]

    def get_end_comp(self):
        """
        method: get start component id
        :return: end_comp_id, e.g., 'resistor-1'
        """
        return self.get_comp_tmnl()[1][0]

    def get_end_tmnl(self):
        """
        method: get end component's terminal number
        :return: end_comp_tmnl, e.g., 1, 2
        """
        return self.get_comp_tmnl()[0][1]

    def get_mid_pcrds(self):
        """
        method: get middle points' crd, list, e.g., [x1, y1, x2, y2, ..]
        :return: e.g., [], [x1, y1, x2, y2, ..], etc,..
        """
        return self.wire_obj.get_mid_pcrds()


class Platform:
    """
    class: Platform for electric system, consist of Components, Connectors, Texts and Icons
    """
    def __init__(self,
                 source_data=None,
                 **kwargs):
        """
        method: init a Circuit
        :param source_data: circuit's source data
        :param kwargs: Keyword arguments, refer to Default.dft_cir_data, e.g.,
        cir_name: circuit's name, e.g., 'RLC circuit'
        """
        # source data
        self.source_data = None
        # calculation data
        self.calc_data = None
        # tkinter canvas
        self.canvas = None
        # component objects
        self.comp_objs = {}
        # connector objects
        self.conn_objs = {}
        # text objects
        self.text_objs = {}
        # icon objects
        self.icon_objs = {}
        # data reading from file, used in method self.open(), self.save() and self.close()
        self.file_data = None

        # File object, used for reading and writing of the .elc and .cmp file
        self.file_obj = file.File()

        # create circuit's Elements(including Components, Connectors, Texts and Graphs)
        if source_data:
            self.create_elc_from_data(source_data)
        else:
            self.create_elc_from_default(**kwargs)

    def create_elc_from_data(self,
                             source_data):
        """
        method: create elc from source data
        :param source_data: source data
        :return: None
        """
        # passing the parameters
        self.source_data = source_data
        # copy the calc_data in self.cource_data
        self.calc_data = self.source_data['calc_data']
        # create Elements in circuit
        for key in source_data['comps_data']:
            self.comp_objs[key] = Component(comp_nm=key.split('-')[0],
                                            source_data=source_data['comps_data'][key])
        for key in source_data['conns_data']:
            self.conn_objs[key] = Connector(source_data=source_data['conns_data'][key],
                                            comp_objs=self.comp_objs)
        for key in source_data['texts_data']:
            self.text_objs[key] = Text(source_data=source_data['texts_data'][key])
        for key in source_data['grphs_data']:
            self.text_objs[key] = Icon(icon_nm=key.split('-')[0],
                                       source_data=source_data['grphs_data'][key])

    def create_elc_from_default(self,
                                **kwargs):
        """
        method: create electric from default
        :param kwargs: Keyword arguments, refer to Default.dft_cir_data, e.g.,
        cir_name: circuit's name, e.g., 'RLC circuit'
        :return: None
        """
        self.source_data = copy.deepcopy(default.dft_elc_data)
        # copy the calc_data in self.cource_data
        self.calc_data = self.source_data['calc_data']
        # pass the kwargs, e.g., cir_name
        for key in kwargs:
            if kwargs[key] is not None:
                self.source_data[key] = kwargs[key]

    def display(self):
        """
        method: display the Circuit
        :return:
        """
        if self.canvas:
            for key in self.comp_objs:
                self.comp_objs[key].display(self.canvas)
            for key in self.conn_objs:
                self.conn_objs[key].display(self.canvas)
            for key in self.text_objs:
                self.text_objs[key].display(self.canvas)
            for key in self.icon_objs:
                self.icon_objs[key].display(self.canvas)
        else:
            print('The canvas is needed!')

    def add_component(self,
                      comp_nm,
                      func=None,
                      **kwargs):
        """
        method: add a Compnent
        :param comp_nm: Component's name, e.g.,
        'resistor', 'capacitor', 'resistor', 'capacitor', 'inductor', 'diode', 'voltage_ac', 'voltage_dc', 'current_ac',
        'current_dc', 'ground', 'gap', 'vcvs', 'vccs', 'ccvs', 'cccs'
        :param func: function to be called after the Component is added.
        :param kwargs: Keyword arguments, refer to Elecpy.Default.dft_comps_data, e.g.,
        'designator': 'R-?',
        'value': 10.0,
        'node1': None,
        'node2': None,
        'vol_dir': 1,
        'cur_dir': 1,
        'crd_x': 60,
        'crd_y': 60,
        'angle': 0
        :return:
        """
        # create a new Component
        comp_obj = Component(comp_nm=comp_nm, **kwargs)
        # edit the component
        comp_id = self.gen_comp_id(comp_nm)
        comp_obj.set_data(part=True,
                          id=comp_id)
        self.comp_objs[comp_id] = comp_obj
        self.source_data['comps_data'][comp_id] = comp_obj.get_data()
        # call the function func()
        if func is not None:
            func()

    def add_connector(self,
                      sta_comp,
                      sta_tmnl,
                      end_comp,
                      end_tmnl,
                      func=None,
                      mid_crds=None):
        """
        method: add Connector to circuit
        :param sta_comp: start component id
        :param sta_tmnl: start component's terminal number
        :param end_comp: end component id
        :param end_tmnl: end component's terminal number
        :param func: function to be called after the Component is added.
        :param mid_crds: middle points' coordinate list, e.g., [100, 200, 200, 300, ..]
        :return: None
        """
        sta_comp = self.get_id_from_designator(designator=sta_comp)
        end_comp = self.get_id_from_designator(designator=end_comp)
        conn_id = self.gen_wire_id()
        net_id = self.gen_net_id(sta_comp=sta_comp,
                                 sta_tmnl=sta_tmnl,
                                 end_comp=end_comp,
                                 end_tmnl=end_tmnl)
        if net_id is not False:
            # create a conn_obj
            conn_obj = Connector(comp_objs=self.comp_objs,
                                 id=conn_id,
                                 net_id=net_id,
                                 sta_comp=sta_comp,
                                 sta_tmnl=sta_tmnl,
                                 end_comp=end_comp,
                                 end_tmnl=end_tmnl,
                                 mid_crds=mid_crds)

            self.conn_objs[conn_id] = conn_obj
            self.source_data['conns_data'][conn_id] = conn_obj.get_data()
            # call the function func()
            if func is not None:
                func()
        else:
            print('The two terminal have different nets!')

    def get_id_from_designator(self,
                               designator):
        """
        method: get the id of a Component from it's designator, if gives id to designator, return id
        :return: id
        """
        if designator in self.get_comp_designator_lst():
            for key in self.comp_objs:
                if designator == self.comp_objs[key].get_data('part_data')['designator']:
                    return self.comp_objs[key].get_data('part_data')['id']
        elif designator.split('-')[0] == 'G':
            return designator.replace('G', 'ground')
        elif designator in self.get_comp_id_lst():
            return designator

    def select(self, crd):
        """
        method: judge if any Component, Connector, Text or Graph is selected by crd
        :param crd: coordinate, (crd_x, crd_y)
        :return: True: one Element is selected. False: No Element is selected.
        """
        for key in self.comp_objs:
            if self.comp_objs[key].select(crd):
                return True
        for key in self.conn_objs:
            if self.conn_objs[key].select(crd):
                return True
        for key in self.text_objs:
            if self.text_objs[key].select(crd):
                return True
        for key in self.icon_objs:
            if self.icon_objs[key].select(crd):
                return True
        return False

    def enclosed_select(self, x0, y0, x1, y1):
        """
        method: enclosed select
        :return: id list of str, [id1, id2,..]
        """
        for key in self.comp_objs:
            self.comp_objs[key].enclosed_select(x0, y0, x1, y1)
        for key in self.conn_objs:
            self.conn_objs[key].enclosed_select(x0, y0, x1, y1)

    def move_to(self, to_crd):
        """
        method: move the selected Component, Text or Graph to to_crd
        :param to_crd: destination location coordinate, (crd_x, crd_y)
        :return: None
        """
        for key in self.comp_objs:
            self.comp_objs[key].move_to(to_crd)
        for key in self.conn_objs:
            self.conn_objs[key].move_to(to_crd)
        for key in self.text_objs:
            self.text_objs[key].move_to(to_crd)
        for key in self.icon_objs:
            self.icon_objs[key].move_to(to_crd)

    def move_by(self, bias_crd):
        """
        method: move all the selected Component, Connector, Text or Icon by crd_bias
        :param bias_crd:
        :return:
        """
        for key in self.comp_objs:
            self.comp_objs[key].move_by(bias_crd)
        for key in self.conn_objs:
            self.conn_objs[key].move_by(bias_crd)
        for key in self.text_objs:
            self.text_objs[key].move_by(bias_crd)
        for key in self.icon_objs:
            self.icon_objs[key].move_by(bias_crd)

    def rotate(self):
        """
        method: clockwise rotate a selected Component or Graph 90 degree
        :return:
        """
        for key in self.comp_objs:
            self.comp_objs[key].rotate()
        for key in self.icon_objs:
            self.icon_objs[key].rotate()

    def delete(self):
        """
        method: delete the selected Component or Connectorin the Circuit
        :return: None
        """
        self.__del_component()
        self.__del_connector()

    def __del_component(self):
        """
        method: delete the selected Component or its Text or Graph
        :return: None
        """
        for key in self.comp_objs:
            # if the component itself is selected, judge if it is connected to other component.
            # if the component is connected to other component, print a hint that this component can not be deleted.
            # if the component is independent, delete this component
            if self.comp_objs[key].slct['part']:
                if key.split('-')[0] == 'ground':
                    if self.comp_objs[key].get_data('part_data')['node1'] is not None:
                        messagebox.showinfo(title='information',
                                            message='The compnent has connections, '
                                                    'delete all the connections before deleting!')
                    else:
                        self.comp_objs[key].clear()
                        self.comp_objs.pop(key)
                        self.source_data['comps_data'].pop(key)
                        return
                else:
                    if self.comp_objs[key].get_data('part_data')['node1'] is not None or \
                            self.comp_objs[key].get_data('part_data')['node2'] is not None:
                        messagebox.showinfo(title='information',
                                            message='The compnent has connections, '
                                                    'delete all the connections before deleting!')
                    else:
                        self.comp_objs[key].clear()
                        self.comp_objs.pop(key)
                        self.source_data['comps_data'].pop(key)
                        return

    def __del_connector(self):
        """
        method: delete the selected Connector, 2 missions need to be accomplished.
        1. delete the Connector in self.conn_objs.
        2. judge the Connector's start Component'terminal and end Component's terminal, if the terminal's Connector
        number is zero, the self.source_data['comps_data']['node1']=None, or self.source_data['comps_data']['node2']=
        None.
        :return: None
        """
        for key in self.conn_objs:
            # delete the connector, modified start Component and end Component's node's value.
            if self.conn_objs[key].slct['wire']:
                # find component id and terminal number of the start Compnent and end Component of the connector
                wire_data = self.conn_objs[key].get_data('wire_data')
                comp1_id = wire_data['sta_comp']
                comp1_tmnl = wire_data['sta_tmnl']
                comp2_id = wire_data['end_comp']
                comp2_tmnl = wire_data['end_tmnl']
                # calculate connector number of the Component(comp_id)'s terminal(comp_tmnl)
                if self.count_wire_num(comp1_id, comp1_tmnl) == 1:
                    # if comp1_id.split('-')[0] != 'ground':
                    comp_data = {('node' + comp1_tmnl): None}
                    self.comp_objs[comp1_id].set_data(part=True,
                                                      **comp_data)
                if self.count_wire_num(comp2_id, comp2_tmnl) == 1:
                    # if comp2_id.split('-')[0] != 'ground':
                    comp_data = {('node' + comp2_tmnl): None}
                    self.comp_objs[comp2_id].set_data(part=True,
                                                      **comp_data)
                # delete the connector
                self.conn_objs[key].clear()
                self.conn_objs.pop(key)
                self.source_data['conns_data'].pop(key)
                return
            else:
                self.conn_objs[key].delete()

    def clear(self):
        """
        method: clear the display of circuit, including all Component, Connector, Text and Graph
        :return: None
        """
        for key in self.comp_objs:
            self.comp_objs[key].clear()
        for key in self.conn_objs:
            self.conn_objs[key].clear()
        for key in self.text_objs:
            self.text_objs[key].clear()
        for key in self.icon_objs:
            self.icon_objs[key].clear()

    def count_wire_num(self,
                       comp_id=None,
                       tmnl=None):
        """
        method: count Component(id=comp_id)'s terminal(number=1, 2)'s wire number
        :param comp_id: Component's id, 'resistor-1'
        :param tmnl: terminal number, e.g., 1, 2
        :return: wire number
        """
        num = 0
        for key in self.conn_objs:
            if self.conn_objs[key].get_comp_tmnl()[0][0] == comp_id and \
                    self.conn_objs[key].get_comp_tmnl()[0][1] == tmnl:
                num += 1
            if self.conn_objs[key].get_comp_tmnl()[1][0] == comp_id and \
                    self.conn_objs[key].get_comp_tmnl()[1][1] == tmnl:
                num += 1
        return num

    def get_net_comp_tmnl(self):
        """
        method: get net's comp_id and terminal list
        :return: e.g., {net1:[(comp1,tmnl1), (comp2, tmnl2), ..], net2:[]}
        """
        net_nodes = {}
        for key in self.comp_objs:
            id = self.comp_objs[key].get_data('part_data')['id']
            if id.split('-')[0] == 'ground':
                continue
            node1 = self.comp_objs[key].get_data('part_data')['node1']
            node2 = self.comp_objs[key].get_data('part_data')['node2']
            if node1 is not None and node1 != 0:
                if node1 not in net_nodes.keys():
                    net_nodes[node1] = [(id, 1)]
                else:
                    net_nodes[node1].append((id, 1))
            if node2 is not None and node2 != 0:
                if node2 not in net_nodes.keys():
                    net_nodes[node2] = [(id, 2)]
                else:
                    net_nodes[node2].append((id, 2))
        return net_nodes

    def get_net_conn(self):
        """
        method: get net's connector list, i.e., {net1: [conn1, conn2, ...], net2: [conn1, conn2, ...]}
        :return: {net1: [conn1, conn2, ...], net2: [conn1, conn2, ...]}
        """
        net_conn = {}
        for key in self.conn_objs:
            id = self.conn_objs[key].get_data('wire_data')['id']
            net_id = self.conn_objs[key].get_data('wire_data')['net_id']
            if net_id is not None and net_id != 0:
                if net_id not in net_conn.keys():
                    net_conn[net_id] = [id]
                else:
                    net_conn[net_id].append(id)
        return net_conn

    def refresh_net_id(self):
        """
        method: refresh net id
        :return: None
        """
        # refresh the component's net id
        net_nodes = self.get_net_comp_tmnl()
        for idx, key in enumerate(net_nodes):
            for comp, tmnl in net_nodes[key]:
                data = {'node' + str(tmnl): idx + 1}
                self.comp_objs[comp].set_data(part=True, **data)

        # refresh the connector's net id
        net_conns = self.get_net_conn()
        for idx, key in enumerate(net_nodes):
            for conn in net_conns[key]:
                data = {'net_id': idx + 1}
                self.conn_objs[conn].set_wire_data(**data)

    def compile(self):
        """
        method: compile circuit, including judge the connection is complete, net id is continuous, return True when
        compile is completed. when the compile failed, messagebox will be shown.
        :return: True: compile completed，False: compile failed
        """
        # judge the connection is complete
        if not self.judge_connect_complete():
            messagebox.showwarning(title='warning', message='Check the Connection')
            return False
        # judge if net_id is continuous, refresh net_id
        if not self.judge_net_id():
            self.refresh_net_id()
        # judge Component's designator,
        if not self.judge_comps_designator():
            messagebox.showwarning(title='warning', message='Check the designator of compnent!!')
            return False
        # judge ground
        if not self.judge_ground():
            messagebox.showwarning(title='warning', message='Ground is missed!!')
            return False
        return True

    def get_netlist(self):
        """
        method: get the "netlist"
        :return: netlist, e.g.,
        [{'designator': 'Uac-1', 'amp': 100, 'freq': 50, 'phase': 0.0, 'node1': 1, 'node2': 0, 'vol_dir': 1, 'cur_dir': 1},
         {'designator': 'R-1', 'value': 10.0, 'node1': 1, 'node2': 2, 'vol_dir': 1, 'cur_dir': 1},
         {'designator': 'L-1', 'value': 1e-06, 'Il': 0, 'node1': 2, 'node2': 3, 'vol_dir': 1, 'cur_dir': 1},
         {'designator': 'C-1', 'value': 1e-06, 'Uc': 0, 'node1': 3, 'node2': 0, 'vol_dir': 1, 'cur_dir': 1}
         ]
        """
        if not self.compile():
            return False
        # get netlist
        netlist = []
        for key in self.comp_objs:
            if key.split('-')[0] == 'ground':
                continue
            comp_data = copy.deepcopy(self.comp_objs[key].get_data('part_data'))
            remove_key = ['id', 'crd_x', 'crd_y', 'angle']
            for key in remove_key:
                comp_data.pop(key)
            netlist.append(comp_data)
        return netlist

    def judge_comp_designator(self,
                              designator):
        """
        method: judge if designator is normal
        :param designator: Component's designator
        :return: True: normal, False:
        """
        designator_list = self.get_comp_designator_lst()
        if designator.count('-') != 1:
            return False
        if not str.isdecimal(designator.split('-')[1]):
            return False
        # judge if duplicate of name
        for designator in designator_list:
            if designator_list.count(designator) > 1:
                return False
        return True

    def judge_comps_designator(self):
        """
        method: judge if all the designators in the circuit is legal
        :return: True: legal， False: illegal
        """
        designator_list = self.get_comp_designator_lst()
        # judge if legal
        for designator in designator_list:
            if not self.judge_comp_designator(designator):
                return False
        return True

    def judge_ground(self):
        """
        method: judge if the ground is missed
        :return: True: not missed False: missed
        """
        for designator in self.comp_objs.keys():
            if 'ground' in designator:
                return True
        return False

    def judge_connect_complete(self):
        """
        method: judge if the connection is complete, i.e., no component is isolated.
        :return: True: complete, False: not complete
        """
        for key in self.comp_objs:
            if self.comp_objs[key].get_data('part_data')['node1'] is None:
                print(self.comp_objs[key].get_data('part_data')['node1'])
                return False
            if key.split('-')[0] != 'ground':
                if self.comp_objs[key].get_data('part_data')['node2'] is None:
                    print(self.comp_objs[key].get_data('part_data')['node2'])
                    return False
        return True

    def judge_net_id(self):
        """
        method: judge if the net ids of the circuit is continuous
        :return: True: continuous， False: not continuous
        """
        net_id_list = self.get_net_id_lst()
        for idx, data in enumerate(net_id_list):
            if idx + 1 not in net_id_list:
                return False
        return True

    def open(self,
             path,
             file):
        """
        method: open a elecpy file(.elc file)
        :param path: path, e.g., 'E:/'
        :param file: file name, e.g., 'xx.elc'
        :return: None
        """
        # open file in direction of path and get the source data of circuit
        source_data = self.file_obj.open_elcfile(path, file)
        # get the data in file, used to compare with the source data to judge if the data was modified.
        self.file_data = copy.deepcopy(source_data)
        # create Platform from source data getting from .elc file
        self.create_elc_from_data(source_data)

    def save(self,
             filepath=None):
        """
        method: save self.source_data into file following rules as below:
        If filepath is not default, save self.source_data into filepath.
        If filepath is default and self.source_data is getting from file, save self.source_data into that file.
        If filepath is default and self.source_data is not getting from file, do nothing.
        :param filepath: full path file, e.g., 'E:/../xxx.elc'
        :return: None
        """
        self.calc_data['time'] = None
        if self.calc_data['calc_method'] == 'Dynamic':
            for key in ['u_comps', 'i_comps', 'u_nodes', 'time']:
                self.calc_data[key] = None
        self.file_data = copy.deepcopy(self.source_data)
        self.file_obj.save_elcfile(elc_data=self.source_data,
                                   filepath=filepath)

    def close(self):
        """
        method: close the file
        :return: None
        """
        self.clear()
        self.file_obj.source_elcfilepath = None
        self.comp_objs = {}
        self.conn_objs = {}
        self.text_objs = {}
        self.icon_objs = {}
        self.source_data = copy.deepcopy(default.dft_elc_data)
        self.calc_data = self.source_data['calc_data']
        self.file_data = None

    def get_comp_id_lst(self,
                        comp_nm=None):
        """
        method: get one kind of Component's comp_id list or all Components' comp_id list when comp_nm is default
        :param comp_nm: component's name, e.g., 'resistor', 'capacitor', etc..
        :return: e.g., ['resistor-1', 'capacitor-1', ..]
        """
        comp_id_lst = []
        for idx, key in enumerate(self.comp_objs):
            if comp_nm is None:
                comp_id_lst.append(self.comp_objs[key].get_data('part_data')['id'])
            elif comp_nm == self.comp_objs[key].get_data('part_data')['id'].split('-')[0]:
                comp_id_lst.append(self.comp_objs[key].get_data('part_data')['id'])
        return comp_id_lst

    def gen_comp_id(self,
                    comp_nm):
        """
        method: generate comp_id for a new Component
        :param comp_nm: component name
        :return: e.g., 'resistor-1', 'capacitor-2', ..
        """
        comp_id_lst = self.get_comp_id_lst(comp_nm=comp_nm)
        i = 1
        while True:
            if comp_nm + '-' + str(i) not in comp_id_lst:
                break
            i += 1
        return comp_nm + '-' + str(i)

    def get_comp_designator_lst(self,
                                comp_nm=None):
        """
        method: get Component whose name is comp_nm or all Components' designator list(not include 'ground')
        :param comp_nm: component name
        :return: e.g., ['R-1', 'C-1', ..]
        """
        # get all the Component's designator list except ground
        comp_designator_lst = []
        for key in self.comp_objs:
            if key.split('-')[0] != 'ground':
                if comp_nm is not None:
                    if comp_nm == self.comp_objs[key].get_data('part_data')['id'].split('-')[0]:
                        comp_designator_lst.append(self.comp_objs[key].get_data('part_data')['designator'])
                else:
                    comp_designator_lst.append(self.comp_objs[key].get_data('part_data')['designator'])
        return comp_designator_lst

    def gen_comp_designator(self,
                            comp_nm):
        """
        method: generate designator for a new Component whose kind is comp_nm
        :param comp_nm: component name
        :return: e.g., 'R-1', 'C-1', etc..
        """
        comp_dsg_lst = self.get_comp_designator_lst(comp_nm=comp_nm)
        i = 1
        while True:
            if default.nm2designator[comp_nm] + '-' + str(i) not in comp_dsg_lst:
                break
            i += 1
        return default.nm2designator[comp_nm] + '-' + str(i)

    def give_comps_designator(self):
        """
        method: give all Components's designator in bulk
        :return: None
        """
        for key in self.comp_objs:
            id = self.comp_objs[key].get_data('part_data')['id']
            designator = self.comp_objs[key].get_data('part_data')['designator']
            if not self.judge_comp_designator(designator):
                self.comp_objs[key].set_data(part=True,
                                             designator=self.gen_comp_designator(comp_nm=id.split('-')[0]))
        self.display()

    def get_wire_id_lst(self):
        """
        method: get Connector id list
        :return: e.g., ['wire-1', 'wire-2', etc..]
        """
        wire_id_lst = []
        for key in self.conn_objs:
            wire_id_lst.append(self.conn_objs[key].get_data('wire_data')['id'])
        return wire_id_lst

    def gen_wire_id(self):
        """
        method: generate a id for new Connector(or Wire)
        """
        wire_id_lst = self.get_wire_id_lst()
        i = 1
        while True:
            if 'wire-' + str(i) not in wire_id_lst:
                break
            i += 1
        return 'wire-' + str(i)

    def gen_net_id(self,
                   sta_comp=None,
                   sta_tmnl=None,
                   end_comp=None,
                   end_tmnl=None):
        """
        method: generate a net id for a new connection, used for creating a new Connector(or Wire)
        :param sta_comp: start component id
        :param sta_tmnl: start component's terminal number
        :param end_comp: end component id
        :param end_tmnl: end component's terminal number
        :return: None
        """
        # get the existed net id
        if sta_comp.split('-')[0] == 'ground':
            sta_net = 0
        else:
            sta_net = self.comp_objs[sta_comp].get_tmnl_net(sta_tmnl)
        if end_comp.split('-')[0] == 'ground':
            end_net = 0
        else:
            end_net = self.comp_objs[end_comp].get_tmnl_net(end_tmnl)
        # only start terminal has net
        if sta_net is not None and end_net is None:
            return sta_net
        # only end terminal has net
        elif end_net is not None and sta_net is None:
            return end_net
        # start terminal and end terminal both have nets
        elif sta_net is not None and end_net is not None:
            if sta_net == end_net:
                return sta_net
            else:
                return False
        # start and end terminal both have no nets
        else:
            net_id_lst = self.get_net_id_lst()
            i = 1
            while True:
                if i not in net_id_lst:
                    break
                i += 1
            return i

    def change_net_id(self,
                      old_net_id,
                      new_net_id):
        """
        method: change id of the net, whose id is old_net_id, to new_net_id
        :param old_net_id: old net id
        :param new_net_id: nwe net id
        :return: None
        """
        if old_net_id not in self.get_net_id_lst():
            print('old_net_id is not exist!')
            return None
        if new_net_id in self.get_net_id_lst():
            print('new_net_id is already exist!')
            return None
        # change all the Component terminal's net id
        for key in self.comp_objs:
            if self.comp_objs[key].get_data(key='part_data')['node1'] == old_net_id:
                self.comp_objs[key].set_data(part=True,
                                             node1=new_net_id)
            if self.comp_objs[key].get_data(key='part_data')['node2'] == old_net_id:
                self.comp_objs[key].set_data(part=True,
                                             node2=new_net_id)
        # change all the Connector(i.e., Wire)'s net id
        for key in self.conn_objs:
            if self.conn_objs[key].get_data(key='wire_data')['net_id'] == old_net_id:
                self.conn_objs[key].set_wire_data(net_id=new_net_id)

    def get_net_id_lst(self):
        """
        method: get net id list in the circuit, not including net 0, i.e., ground's net
        :return: net id list, e.g., [1, 2, 3, ...]
        """
        net_id_lst = []
        for key in self.comp_objs:
            net_id1 = self.comp_objs[key].get_data('part_data')['node1']
            if net_id1 not in net_id_lst and net_id1 is not None and net_id1 != 0 and net_id1 != 'None':
                net_id_lst.append(net_id1)
            if key.split('-')[0] != 'ground':
                net_id2 = self.comp_objs[key].get_data('part_data')['node2']
                if net_id2 not in net_id_lst and net_id2 is not None and net_id2 != 0 and net_id2 != 'None':
                    net_id_lst.append(net_id2)
        net_id_lst.sort()
        return net_id_lst

    def get_calc_config(self):
        """
        method: get calculation config
        :return:
        """
        calc_config = copy.deepcopy(self.calc_data)
        for key in ['u_comps', 'i_comps', 'u_nodes', 'time']:
            calc_config.pop(key)
        return calc_config


class PlatformGUI(Platform):
    """
    class: Platform's GUI
    """
    def __init__(self):
        """
        method: init Circuit GUI
        """
        super().__init__()

        # root window for the CircuitGUI platform and its width and height
        self.root_win = None
        self.win_width = None
        self.win_height = None
        # areas on the root window
        self.frame_title = None
        self.frame_tools = None
        self.frame_work = None
        # Scroll Canvas
        self.scr_can = None
        # select flag
        self.slct_rectangle = None
        self.slct_flag = False
        # operation bar
        self.oper_bar = None
        # tk.Label, display the .elc file's path
        self.filepath_diplay = None
        # tool bar
        self.tool_bar = None
        # mouse right button's pop up menu
        self.rt_menu = None

        # start up when the class make a instance
        self.start_up()

    def build_root_win(self,
                       geometry=None):
        """
        method: build a root window for circuit GUI
        :param geometry: e.g., '1920x1200'
        :return: root window
        """
        self.root_win = tk.Tk()
        self.root_win.title('Elecpy->Platform')
        # cancel the affect of matplotlib's plot
        FigureCanvasTkAgg(pyplot.figure(), master=self.root_win)
        if geometry is None:
            self.root_win.state('zoomed')
            self.root_win.update()
            self.win_width = self.root_win.winfo_width()
            self.win_height = self.root_win.winfo_height()
            geometry = str(self.win_width) + 'x' + str(self.win_height)
        else:
            self.win_width = int(geometry.split('x')[0])
            self.win_height = int(geometry.split('x')[1])
        self.root_win.geometry(geometry)

        # title area
        self.frame_title = tk.LabelFrame(self.root_win, bg='#F0F0F0', text=None, font=('仿宋', 12),
                                         height=32,
                                         width=self.win_width)
        self.frame_title.grid(row=0, column=0, columnspan=2)
        self.frame_title.grid_propagate(0)

        # tools area
        self.frame_tools = tk.LabelFrame(self.root_win, bg='#F0F0F0', text='Tools', font=('仿宋', 12),
                                         height=self.win_height - 32,
                                         width=120)
        self.frame_tools.grid(row=1, column=0)
        self.frame_tools.grid_propagate(0)

        # work area
        self.frame_work = tk.LabelFrame(self.root_win, bg='#F0F0F0', text='Platform', font=('仿宋', 12),
                                        height=self.win_height - 32,
                                        width=self.win_width - 120)
        self.frame_work.grid(row=1, column=1)
        self.frame_work.grid_propagate(0)

        return self.root_win

    def mainloop(self):
        """
        method: mainloop the root window, like method .mainloop() in tkinter.
        :return: None
        """
        self.root_win.mainloop()

    def build_oper_bar(self,
                       master):
        """
        method: build the operation bar, containing buttons such as 'New', 'Open', etc..
        :param master: the tkinter widget, tkinter.Frame,
        :return: operation bar, ButtonsArea
        """
        self.oper_bar = gui_elements.ButtonsPage(master=master,
                                                 btn_lst=['New', 'Open', 'Template', 'Refresh', 'Save', 'SaveAs', 'Close',
                                                          'Designator', 'Compile', 'Netlist', 'Run', 'Graph'],
                                                 wdg_width=800,
                                                 btn_width=[4, 5, 8, 7, 5, 6, 5, 10, 7, 7, 5, 7],
                                                 num_per_row=20)
        self.filepath_diplay = ttk.Label(self.frame_title)
        self.filepath_diplay.grid(row=0, column=1)
        self.filepath_diplay.grid_propagate(0)
        self.oper_bar.disable(btn_lst=['Refresh', 'Save', 'SaveAs', 'Close', 'Designator', 'Compile', 'Netlist', 'Run',
                                       'Graph'])
        self.oper_bar.command(btn_nm='New',
                              cal_func=self.create_new_elc_canvas)
        self.oper_bar.command(btn_nm='Open',
                              cal_func=self.ask_open_elc)
        self.oper_bar.command(btn_nm='Template',
                              cal_func=self.config_template)
        self.oper_bar.command(btn_nm='Refresh',
                              cal_func=self.state_normal)
        self.oper_bar.command(btn_nm='Save',
                              cal_func=self.ask_save_elc)
        self.oper_bar.command(btn_nm='SaveAs',
                              cal_func=self.ask_save_as_elc)
        self.oper_bar.command(btn_nm='Close',
                              cal_func=self.close)
        self.oper_bar.command(btn_nm='Designator',
                              cal_func=self.designator)
        self.oper_bar.command(btn_nm='Compile',
                              cal_func=self.compile_check)
        self.oper_bar.command(btn_nm='Netlist',
                              cal_func=self.disp_netlist)
        self.oper_bar.command(btn_nm='Run',
                              cal_func=self.run_cir)
        self.oper_bar.command(btn_nm='Graph',
                              cal_func=self.config_graph)

        return self.oper_bar

    def create_new_elc_canvas(self):
        """
        method: create a new circuit's canvas
        :return: None
        """
        # close the circuit if there is a previous circuit opened
        self.close()
        # copy value of self.source_data
        self.file_data = copy.deepcopy(self.source_data)
        self.scr_can = gui_elements.ScrollCanvas(self.frame_work, grid=20)
        self.canvas = self.scr_can.canvas
        self.slct_rectangle = SelectRectangle(canvas=self.canvas)
        self.state_normal()
        self.tool_bar.enable()
        self.oper_bar.enable(['Refresh', 'Save', 'SaveAs', 'Close', 'Designator', 'Compile', 'Netlist', 'Run'])

    def ask_open_elc(self):
        """
        method: pop a file dialogue. find the file to be opened.
        :return: None
        """
        pathfile = filedialog.askopenfilename(defaultextension='.elc',
                                              filetypes=[('.elc', '*.elc'), ('.cmp', '*.cmp')])
        if pathfile:
            self.create_new_elc_canvas()
            self.open(path=os.path.dirname(pathfile),
                      file=os.path.basename(pathfile))
            self.display()
            self.state_normal()
            self.filepath_diplay.config(text=self.file_obj.source_elcfilepath)
            if self.judge_calc_data():
                self.oper_bar.enable(['Graph'])

    def ask_save_elc(self):
        """
        method: save the source data to the file from which is it. if the source data is not from a file, pop up a file
        dialog and define a path and file.
        :return: None
        """
        if self.scr_can:
            if self.file_obj.source_elcfilepath and self.file_obj.source_elcfilepath != 'Template Circuit':
                self.save()
            else:
                pathfile = filedialog.asksaveasfilename(defaultextension='.elc',
                                                        filetypes=[('.elc', '*.elc'), ('.cmp', '*.comp')])
                if pathfile:
                    self.save(filepath=pathfile)
                    self.file_obj.source_elcfilepath = pathfile
                    self.filepath_diplay.config(text=self.file_obj.source_elcfilepath)
        else:
            messagebox.showerror(title='warning!', message='The circuit is not exist!')
        self.state_normal()

    def ask_save_as_elc(self):
        """
        method: a file dialog box pops up. find a path and define a filename to save source data in.
        :return: None
        """
        if self.scr_can:
            pathfile = filedialog.asksaveasfilename(defaultextension='.elc',
                                                    filetypes=[('.elc', '*.elc'), ('.cmp', '*.comp')])
            if pathfile:
                self.save(filepath=pathfile)
                self.file_obj.source_elcfilepath = pathfile
                self.filepath_diplay.config(text=self.file_obj.source_elcfilepath)
        else:
            messagebox.showerror(title='warning!', message='The circuit is not exist!')
        self.state_normal()

    def close(self):
        """
        method: close the current circuit
        :return: None
        """
        answer = False
        if self.file_data != self.source_data and self.file_data is not None and \
                self.file_obj.source_elcfilepath != 'Template Circuit':
            answer = messagebox.askyesnocancel(title='warning',
                                               message='The file has been changed, do you want to save?')
        if answer is True:
            self.ask_save_elc()
        elif answer is None:
            # self.state_normal()
            return
        super().close()
        if self.tool_bar:
            self.tool_bar.disable()
        if self.oper_bar:
            self.oper_bar.disable(['Refresh', 'Save', 'SaveAs', 'Close', 'Designator', 'Compile', 'Netlist', 'Run',
                                   'Graph'])
        if self.filepath_diplay:
            self.filepath_diplay.config(text='')
        if self.scr_can:
            self.scr_can.destroy()

    def designator(self):
        """
        method: refresh the designator
        :return: None
        """
        super().give_comps_designator()
        self.state_normal()

    def compile_check(self):
        """
        method: check the compile
        :return:
        """
        if super().compile():
            messagebox.showinfo(title='Information', message='Compile finished!!')
        self.state_normal()

    def disp_netlist(self):
        """
        method: display netlist
        :return: None
        """
        netlist = super().get_netlist()
        if netlist:
            page = gui_elements.NormalWin(title='Netlist', width=700, height=500)
            for idx, comp in enumerate(netlist):
                label = ttk.Label(page.frame, text=str(comp), justify=tk.LEFT)
                label.grid(row=idx, column=0)
            self.state_normal()

    def run_cir(self):
        """
        method: run the circuit, i.e., calculate the circuit.
        :return: None
        """
        netlist = self.get_netlist()
        if netlist:
            calculation.CalculationGUI(netlist=netlist,
                                       cir_calc_data=self.calc_data)
        self.oper_bar.enable(['Graph'])
        self.state_normal()

    def judge_calc_data(self):
        """
        method: judge if the calc_data is exist.
        :return: True or False
        """
        for key in ['u_comps', 'i_comps', 'u_nodes']:
            if self.calc_data[key] is None:
                return False
        return True

    def refresh_calc_data(self):
        """
        method:
        :return:
        """
        if self.calc_data['calc_method'] == 'Numerical':
            for key in self.get_calc_config():
                self.source_data['calc_data'][key] = self.calc_data[key]
            # print(self.source_data['calc_data'])
        elif self.calc_data['calc_method'] == 'SinSteady':
            self.source_data['calc_data'] = self.calc_data
        elif self.calc_data['calc_method'] == 'Decimal':
            self.source_data['calc_data'] = self.calc_data

    def build_tool_bar(self,
                       master):
        """
        method: build the tools bar
        :param master: tkinter widget
        :return: None
        """
        self.tool_bar = gui_elements.ButtonsPage(master=master,
                                                 btn_lst=['Res', 'Cap', 'Ind', 'Dio', 'Udc', 'Uac', 'Idc', 'Iac',
                                                          'GND', 'Wire', 'Del'],
                                                 wdg_width=500,
                                                 btn_width=[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                                                 num_per_row=2)
        self.tool_bar.disable()
        self.tool_bar.command(btn_nm='Res',
                              cal_func=lambda x='resistor': self.state_place_comp(comp_nm=x))
        self.tool_bar.command(btn_nm='Cap',
                              cal_func=lambda x='capacitor': self.state_place_comp(comp_nm=x))
        self.tool_bar.command(btn_nm='Ind',
                              cal_func=lambda x='inductor': self.state_place_comp(comp_nm=x))
        self.tool_bar.command(btn_nm='Dio',
                              cal_func=lambda x='diode': self.state_place_comp(comp_nm=x))
        self.tool_bar.command(btn_nm='Udc',
                              cal_func=lambda x='voltage_dc': self.state_place_comp(comp_nm=x))
        self.tool_bar.command(btn_nm='Uac',
                              cal_func=lambda x='voltage_ac': self.state_place_comp(comp_nm=x))
        self.tool_bar.command(btn_nm='Idc',
                              cal_func=lambda x='current_dc': self.state_place_comp(comp_nm=x))
        self.tool_bar.command(btn_nm='Iac',
                              cal_func=lambda x='current_ac': self.state_place_comp(comp_nm=x))
        self.tool_bar.command(btn_nm='GND',
                              cal_func=lambda x='ground': self.state_place_comp(comp_nm=x))
        self.tool_bar.command(btn_nm='Wire', cal_func=self.state_draw_conn)
        self.tool_bar.command(btn_nm='Del', cal_func=self.delete)

    def delete(self):
        """
        method: delete
        :return:
        """
        super().delete()
        self.state_normal()

    def state_normal(self):
        """
        method: normal state
        :return: None
        """
        # mouse's left button
        def button_1(event):
            event_x = int(self.canvas.canvasx(event.x))
            event_y = int(self.canvas.canvasy(event.y))
            self.slct_rectangle.delete()
            self.canvas.config(cursor='arrow')
            if self.select(crd=(event_x, event_y)):
                self.slct_flag = True
            else:
                self.slct_flag = False
                self.slct_rectangle.mark_start(event_x, event_y)
            self.display()

        # drag and move
        def b1_motion(event):
            event_x = int(self.canvas.canvasx(event.x))
            event_y = int(self.canvas.canvasy(event.y))
            if self.slct_flag:
                self.move_to(to_crd=(event_x, event_y))
            self.display()

        def ctrl_b1_motion(event):
            event_x = int(self.canvas.canvasx(event.x))
            event_y = int(self.canvas.canvasy(event.y))
            if not self.slct_flag:
                self.slct_rectangle.draw(event_x, event_y)
                self.enclosed_select(x0=self.slct_rectangle.slct_from[0], y0=self.slct_rectangle.slct_from[1],
                                     x1=event_x, y1=event_y)
            self.display()

        def ctrl_direct_key(event):
            if self.slct_rectangle.exist:
                if event.keysym == 'Down':
                    self.move_by((0, 20))
                    self.slct_rectangle.move_by((0, 20))
                elif event.keysym == 'Up':
                    self.move_by((0, -20))
                    self.slct_rectangle.move_by((0, -20))
                elif event.keysym == 'Left':
                    self.move_by((-20, 0))
                    self.slct_rectangle.move_by((-20, 0))
                elif event.keysym == 'Right':
                    self.move_by((20, 0))
                    self.slct_rectangle.move_by((20, 0))

        # mouse's right button
        def button_3(event):
            event_x = int(self.canvas.canvasx(event.x))
            event_y = int(self.canvas.canvasy(event.y))
            self.pop_rt_menu(event_x, event_y)

        # delete key
        def delete(event):
            self.delete()

        # space key
        def space(event):
            self.rotate()
            self.display()

        def direct_key(event):
            self.change_ref_dir()

        def control_w(event):
            self.state_draw_conn()

        def control_s(event):
            self.ask_save_elc()

        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", button_1)
        self.canvas.bind("<Button-3>", button_3)
        self.canvas.bind("<B1-Motion>", b1_motion)
        self.canvas.bind("<Control-B1-Motion>", ctrl_b1_motion)
        self.canvas.bind("<Control-Up>", ctrl_direct_key)
        self.canvas.bind("<Control-Down>", ctrl_direct_key)
        self.canvas.bind("<Control-Left>", ctrl_direct_key)
        self.canvas.bind("<Control-Right>", ctrl_direct_key)
        self.canvas.bind("<Delete>", delete)
        self.canvas.bind("<space>", space)
        self.canvas.bind("<Up>", direct_key)
        self.canvas.bind("<Down>", direct_key)
        self.canvas.bind("<Left>", direct_key)
        self.canvas.bind("<Right>", direct_key)
        self.canvas.bind("<Control-w>", control_w)
        self.canvas.bind("<Control-s>", control_s)
        # self.canvas.bind("<Control-MouseWheel>", self.zoomer)

    def add_component(self,
                      comp_nm,
                      func=None,
                      **kwargs):
        """
        method: add Component
        :param comp_nm: component name, e.g., 'resistor', 'capacitor', ..
        :param func: function after the adding
        :param kwargs: Keyword arguments
        :return: None
        """
        # create a Component
        comp_obj = Component(comp_nm=comp_nm,
                             id=self.gen_comp_id(comp_nm))
        comp_obj.display(self.canvas)
        comp_obj.move_to(to_crd=(0, 0))
        comp_obj.slct['part'] = True

        def motion(event):
            # conver crd to canvas crd
            event_x = int(self.canvas.canvasx(event.x))
            event_y = int(self.canvas.canvasy(event.y))
            comp_obj.move_to(to_crd=(event_x, event_y))

        def button_1(event):
            # put the new Component to the component dict
            self.comp_objs[comp_obj.get_data('part_data')['id']] = comp_obj
            self.source_data['comps_data'][comp_obj.get_data('part_data')['id']] = comp_obj.get_data()
            comp_obj.slct['part'] = False
            quit_method()
            func()

        def button_3(event):
            comp_obj.clear()
            quit_method()
            func()

        def space(event):
            comp_obj.rotate()

        def quit_method():
            """
            func: quit this method, unbind some event
            """
            self.canvas.unbind("<Motion>")
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<Button-3>")
            self.canvas.unbind("<Escape>")
            self.canvas.unbind("<space>")

        self.canvas.focus_set()
        self.canvas.bind("<Motion>", motion)
        self.canvas.bind("<Button-1>", button_1)
        self.canvas.bind("<Button-3>", button_3)
        self.canvas.bind("<Escape>", button_3)
        self.canvas.bind("<space>", space)

    def draw_connector(self,
                       func):
        """
        method: draw connector
        :param func: function to be called after the connector was added.
        :return: None
        """
        conn_obj = Connector(comp_objs=self.comp_objs)
        # temporary points' crd
        sta_crd = None
        mid_points = []
        end_crd = None
        # left crd
        left_crd = None
        # temporary line width
        tmp_w = 2

        self.canvas.config(cursor='crosshair')

        def button_1(event):
            nonlocal sta_crd, mid_points, end_crd, left_crd, tmp_w
            event_x = int(self.canvas.canvasx(event.x))
            event_y = int(self.canvas.canvasy(event.y))
            comp_id_tmnl = conn_obj.tmnl_select((event_x, event_y))
            # start point
            if comp_id_tmnl and conn_obj.get_sta_comp() is None:
                conn_obj.set_wire_data(sta_comp=comp_id_tmnl[0],
                                       sta_tmnl=comp_id_tmnl[1])

                # get the start crd and left crd
                sta_crd = tools.point_capture(crd=(event_x, event_y))
                left_crd = sta_crd
            # end point
            elif comp_id_tmnl and conn_obj.get_end_comp() is None:
                conn_obj.set_wire_data(end_comp=comp_id_tmnl[0],
                                       end_tmnl=comp_id_tmnl[1])
                # get the end crd
                end_crd = tools.point_capture(crd=(event_x, event_y))

            # middle point
            elif comp_id_tmnl is None and conn_obj.get_sta_comp() is not None and conn_obj.get_end_comp() is not None:
                crd = tools.point_capture(crd=(event_x, event_y))
                if crd:
                    mid_points.append(crd[0])
                    mid_points.append(crd[1])
                    conn_obj.set_wire_data(mid_crds=mid_points)
                    self.canvas.create_line(left_crd[0], left_crd[1], crd[0], crd[1], width=tmp_w, tags='temp1')
                    left_crd = crd

        def motion(event):
            event_x = int(self.canvas.canvasx(event.x))
            event_y = int(self.canvas.canvasy(event.y))
            nonlocal left_crd, end_crd
            # if has start comp and dosen't have end comp
            if conn_obj.get_sta_comp() and conn_obj.get_end_comp() is None:
                crd = tools.point_capture(crd=(event_x, event_y))
                if crd:
                    self.canvas.delete('temp')
                    self.canvas.create_line(left_crd[0], left_crd[1], crd[0], crd[1], width=tmp_w, tags='temp')
            # if has both start comp adn end comp
            elif conn_obj.get_sta_comp() and conn_obj.get_end_comp():
                crd = tools.point_capture(crd=(event_x, event_y))
                if crd:
                    self.canvas.delete('temp')
                    self.canvas.create_line(left_crd[0], left_crd[1], crd[0], crd[1], width=tmp_w, tags='temp')
                    self.canvas.create_line(end_crd[0], end_crd[1], crd[0], crd[1], width=tmp_w, tags='temp')

        def button_3(event):
            self.canvas.config(cursor='arrow')
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<Motion>")
            self.canvas.unbind("<Button-3>")
            nonlocal mid_points
            # if click right button before finishing the end terminal of the wire, delete all
            if conn_obj.get_end_comp() is None:
                self.canvas.delete('temp')
            # if the start terminal and the end terminal are both finished
            elif conn_obj.get_sta_comp() and conn_obj.get_end_comp():
                # get the new id
                comp_tmnl = conn_obj.get_comp_tmnl()
                net_id = self.gen_net_id(sta_comp=comp_tmnl[0][0],
                                         sta_tmnl=comp_tmnl[0][1],
                                         end_comp=comp_tmnl[1][0],
                                         end_tmnl=comp_tmnl[1][1])
                if net_id is False:
                    messagebox.showwarning(title='warning', message='Can not connect the two terminals!\n'
                                                                    'They have different net id!')
                    self.canvas.delete('temp1')
                    self.canvas.delete('temp')
                    self.state_normal()
                    return

                data = {'node' + str(comp_tmnl[0][1]): net_id}
                self.comp_objs[comp_tmnl[0][0]].set_data(part=True, **data)
                data = {'node' + str(comp_tmnl[1][1]): net_id}
                self.comp_objs[comp_tmnl[1][0]].set_data(part=True, **data)
                # delete all the temp wires
                self.canvas.delete('temp1')
                self.canvas.delete('temp')

                # place the text of the wire
                sta_x, sta_y = conn_obj.wire_obj.get_sta_tmnl_crd()
                conn_obj.set_text_data(text_key='default',
                                       content=conn_obj.wire_obj.get_data('id'),
                                       visible=False,
                                       crd_x=sta_x + 20,
                                       crd_y=sta_y + 20)
                # set the wire's id
                conn_id = self.gen_wire_id()
                conn_obj.set_wire_data(id=conn_id,
                                       designator=conn_id,
                                       net_id=net_id)
                # add the Connector to self.conn_objs中
                self.conn_objs[conn_id] = conn_obj
                # add the source data of the new Connector into self.cource_data
                self.source_data['conns_data'][conn_id] = conn_obj.get_data()
                # display
                conn_obj.display(canvas=self.canvas)
            # execute func
            func()

        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", button_1)
        self.canvas.bind("<Motion>", motion)
        self.canvas.bind("<Button-3>", button_3)

    def blank_pop_rt_menu(self, x, y):
        """
        method: mouse right click pop up menu
        :return:
        """
        self.rt_menu = tk.Menu(self.canvas, tearoff=0)

        ref_vol_visible = tk.IntVar(value=self.source_data['elec_config']['ref_vol_visible'])

        def set_refvol_visible():
            """func: set the referenc direction of voltage's visible"""
            if ref_vol_visible.get():
                self.source_data['elec_config']['ref_vol_visible'] = True
            else:
                self.source_data['elec_config']['ref_vol_visible'] = False
            for key in self.comp_objs:
                self.comp_objs[key].set_data(grph_key='dft_vol',
                                             visible=self.source_data['elec_config']['ref_vol_visible'])
            self.display()

        self.rt_menu.add_checkbutton(label='ref_vol', variable=ref_vol_visible, command=set_refvol_visible)

        ref_cur_visible = tk.IntVar(value=self.source_data['elec_config']['ref_cur_visible'])

        def set_refcur_visible():
            """func: set the referenc direction of current's visible"""
            if ref_cur_visible.get():
                self.source_data['elec_config']['ref_cur_visible'] = True
            else:
                self.source_data['elec_config']['ref_cur_visible'] = False
            for key in self.comp_objs:
                self.comp_objs[key].set_data(grph_key='dft_cur',
                                             visible=self.source_data['elec_config']['ref_cur_visible'])
            self.display()

        self.rt_menu.add_checkbutton(label='ref_cur', variable=ref_cur_visible, command=set_refcur_visible)

        self.rt_menu.post(x + 128, y + 88)

    def pop_rt_menu(self, x, y):
        """
        method:
        :param x:
        :param y:
        :return:
        """
        for key in self.comp_objs:
            self.comp_objs[key].pop_menu(x, y)
        if not self.select(crd=(x, y)):
            self.blank_pop_rt_menu(x, y)

    def state_draw_conn(self):
        """
        method: state of drawing connectors
        :return:
        """
        self.draw_connector(self.state_normal)

    def state_place_comp(self,
                         comp_nm):
        """
        method: state of placing components
        :param comp_nm: component name
        :return:
        """
        self.add_component(comp_nm=comp_nm,
                           func=self.state_normal)

    def change_ref_dir(self):
        """
        method: change the reference direction
        :return:
        """
        for key in self.comp_objs:
            self.comp_objs[key].reverse_ref_dir()

    def config_graph(self):
        """
        method: config graph display
        :return: None
        """
        if not self.judge_calc_data():
            messagebox.showwarning(title='data missed',
                                   message='The calculation data is none!\nPlease "Run" the circuit again to get data!')
            return
        if self.calc_data['calc_method'] == 'Dynamic':
            grph.GraphGUI(data_ucomps=self.calc_data['u_comps'],
                          data_icomps=self.calc_data['i_comps'],
                          data_unodes=self.calc_data['u_nodes'],
                          data_time=self.calc_data['time'])
        elif self.calc_data['calc_method'] == 'SinSteady':
            grph.GraphGUI(data_ucomps=self.calc_data['u_comps'],
                          data_icomps=self.calc_data['i_comps'],
                          data_unodes=self.calc_data['u_nodes'])
        elif self.calc_data['calc_method'] == 'DCSteady':
            grph.GraphGUI(data_ucomps=self.calc_data['u_comps'],
                          data_icomps=self.calc_data['i_comps'],
                          data_unodes=self.calc_data['u_nodes'])

    def config_template(self):
        """
        method: config the template electric platforms
        :return: None
        """
        page = gui_elements.NormalWin(title='Templates of electric system', width=500, height=600)
        classic_cir_list = gui_elements.ListboxPage(master=page.frame,
                                                    height=200,
                                                    label='Classic Circuits',
                                                    list_data=list(templates.classic_circuits_data.keys()),
                                                    nrows=8)
        """dc_active = gui_elements.ListboxPage(master=page.frame,
                                             height=200,
                                             row=1,
                                             label='DC Active',
                                             list_data=list(templates.classic_circuit.keys()),
                                             nrows=8)
        passive = gui_elements.ListboxPage(master=page.frame,
                                           height=200,
                                           row=2,
                                           label='Passive',
                                           list_data=list(templates.classic_circuit.keys()),
                                           nrows=8)"""

        def func(label, item):
            """callback function"""
            if item in templates.classic_circuits_data.keys():
                if templates.classic_circuits_data[item] == {}:
                    print('data is empty')
                    return
            else:
                return

            self.create_new_elc_canvas()
            self.create_elc_from_data(templates.classic_circuits_data[item])
            self.display()
            self.file_obj.source_elcfilepath = 'Template Circuit'
            self.filepath_diplay.config(text=self.file_obj.source_elcfilepath + '->' + str(item))
            if self.judge_calc_data():
                self.oper_bar.enable(['Graph'])

        classic_cir_list.command(cal_func=func)

    def start_up(self):
        """
        method: start up the circuit GUI platform
        :return: None
        """
        self.build_root_win()
        self.build_oper_bar(self.frame_title)

        self.build_tool_bar(self.frame_tools)

        self.mainloop()


if __name__ == "__main__":
    cir = PlatformGUI()
    cir.start_up()
