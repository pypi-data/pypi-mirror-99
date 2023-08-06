"""
This module include all kind of GUI Elements, such as MainPage, ScrollCanvas, Content, ButtonArea, etc.., consist of
tkinter's widgets.
"""
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import *
import tkinter.filedialog as fdlg
import tkinter.messagebox as msg
from math import *
import pandas as pd


class MainWin:
    """
    class: Main window for a GUI application, including 5 areas: title area, projection area, work area, informationn
    area and status area. every area is a tk.Frame.
    """
    def __init__(self,
                 win_title='Elecpy GUI by Aiqy',
                 page_title=None,
                 geometry=None):
        """
        method: create a main window
        :param win_title: window title
        :param page_title: page title
        :param geometry: window geometry, '1200x900'
        """
        self.root_win = tk.Tk()
        self.root_win.title(win_title)
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

        # frame of title
        self.frame_title = tk.LabelFrame(self.root_win, bg='#F0F0F0', text=None, font=('仿宋', 12),
                                         height=self.win_height / 20,
                                         width=self.win_width)
        self.frame_title.grid(row=0, column=0, columnspan=3)
        self.frame_title.grid_propagate(0)

        # frame of project
        self.frame_prj = tk.LabelFrame(self.root_win, bg='#F0F0F0', text=None, font=('仿宋', 12),
                                       height=self.win_height * 17 / 20,
                                       width=self.win_width / 10)
        self.frame_prj.grid(row=1, column=0)
        self.frame_prj.grid_propagate(0)

        # frame of work
        self.frame_wrk = tk.LabelFrame(self.root_win, bg='#F0F0F0', text=None, font=('仿宋', 12),
                                       height=self.win_height * 17 / 20,
                                       width=self.win_width * 7 / 10)
        self.frame_wrk.grid(row=1, column=1)
        self.frame_wrk.grid_propagate(0)

        # frame of detail
        self.frame_dtl = tk.LabelFrame(self.root_win, bg='#F0F0F0', text=None, font=('仿宋', 12),
                                       height=self.win_height * 17 / 20,
                                       width=self.win_width / 5)
        self.frame_dtl.grid(row=1, column=2)
        self.frame_dtl.grid_propagate(0)

        # frame of status
        self.frame_status = tk.LabelFrame(self.root_win, bg='#F0F0F0', text=None, font=('仿宋', 12),
                                          height=self.win_height / 10,
                                          width=self.win_width)
        self.frame_status.grid(row=2, column=0, columnspan=3)
        self.frame_status.grid_propagate(0)

        # display page_title on the frame of title
        if page_title is not None:
            self.title = tk.Label(self.frame_title, text=page_title, anchor='center', font=('微软雅黑', 35),
                                  height=1, width=46, bg='#F0F0F0', fg='green')
            self.title.grid(row=0, column=0)

    def mainloop(self):
        """
        method: tkinter 's .mainloop() method
        :return: None
        """
        self.root_win.mainloop()

    def destroy(self):
        """
        method: tkinter's destroy() method
        :return: None
        """
        self.root_win.destroy()


class CompWin:
    """
    class: create a window for displaying the component
    """
    def __init__(self,
                 width=None,
                 height=None):
        """
        method: create a window for displaying the component with width and height
        if width and height is not given, the window is full of screen.
        :param width: width of window
        :param height: height of window
        :return: None
        """
        self.root_win = tk.Tk()
        self.root_win.title('Component')
        if width and height:
            geometry = str(width) + 'x' + str(height)
        else:
            self.root_win.state('zoomed')
            self.root_win.update()
            width = self.root_win.winfo_width()
            height = self.root_win.winfo_height()
            geometry = str(width) + 'x' + str(height)
        self.root_win.geometry(geometry)
        self.frame = tk.LabelFrame(self.root_win, bg='#F0F0F0', text=None, font=('仿宋', 12), height=height, width=width)
        self.frame.grid(row=0, column=0, columnspan=3)
        self.frame.grid_propagate(0)

    def mainloop(self):
        """
        method: tkinter's .mainloop() method
        :return: None
        """
        self.root_win.mainloop()

    def destroy(self):
        """
        method: tkinter's .destroy() method
        :return: None
        """
        self.root_win.destroy()


class NormalWin:
    """
    class: create a normal window to supply a container for placing the other widgets or Pages
    """
    def __init__(self,
                 title='Normal',
                 width=None,
                 height=None):
        """
        method: create a window for displaying the component with width and height
        if width and height is not given, the window is full of screen.
        :param title: title
        :param width: width
        :param height: height
        """
        self.root_win = tk.Toplevel()
        self.root_win.title(title)

        if width is None and height is None:
            self.root_win.state('zoomed')
            self.root_win.update()
            width = self.root_win.winfo_width()
            height = self.root_win.winfo_height()
        elif width is None:
            width = 200
        elif height is None:
            height = 200

        self.root_win.geometry(str(width) + 'x' + str(height))
        self.frame = tk.LabelFrame(self.root_win, bg='#F0F0F0', text=None, font=('仿宋', 12), height=height, width=width)
        self.frame.grid(row=0, column=0, columnspan=3)
        self.frame.grid_propagate(0)

    def mainloop(self):
        """
        method: tkinter's .mainloop() method
        :return: None
        """
        self.root_win.mainloop()

    def destroy(self):
        """
        method: tkinter's .destroy() method
        :return: None
        """
        self.root_win.destroy()


class EditWin:
    """
    class: Edit Window
    """
    def __init__(self,
                 data,
                 func_save=None):
        """
        method: a window for editing parameters
        :param data:
        :param func_save:
        """
        self.data = None
        self.win = NormalWin(title='Edit',
                             width=300,
                             height=500)
        self.page = EditPage(self.win.frame,
                             data=data,
                             func_save=func_save)

    def command(self,
                func_save):
        """
        method: command
        :param func_save: the function to be called when the save button is pressed.
        :return: None
        """
        self.page.command(func_save=func_save)

    def mainloop(self):
        """
        method: tkinter's mainloop
        :return: None
        """
        self.win.mainloop()

    def destroy(self):
        """
        method: tkinter's destroy
        :return: None
        """
        self.win.destroy()


class AnimationControlPage:
    """
    class: create a page for control of animation
    """
    def __init__(self,
                 master=None,
                 row=0,
                 column=0):
        """
        method: create the page
        :param master: tkinter widget for placing this area
        :param row: row in .grid()
        :param column: column in .grid()
        """
        # master
        self.master = master

        # create the base frame
        self.bframe = tk.Frame(master=master, width=800, height=100)
        self.bframe.grid(row=row, column=column)
        self.bframe.grid_propagate(0)
        # speed down button
        self.spd_dw_butt = None
        # speed indicator
        self.spd_disp = None
        # speed var, tk.StringVar
        self.spd_var = None
        # speed up button
        self.spd_up_butt = None
        # start button
        self.sta_butt = None
        # suspend button
        self.ssp_butt = None
        # stop button
        self.stp_butt = None
        # position scale
        self.position_scal = None
        self.position_var = None
        # radio buttons for mode
        self.mode_frame = None
        self.mode_var = None
        self.expand = None
        self.shift = None
        self.fixed = None
        # radio buttons for drive
        self.drive_mode_frame = None
        self.drive_mode_var = None
        self.auto = None
        self.manual = None

    def build_spd_adj_butt(self,
                           row=0,
                           column=0,
                           func=None):
        """
        method: build speed adjust button
        :param row:
        :param column:
        :param func:
        :return:
        """
        def spd_dwn_butt_func():
            """speed down button function"""
            temp = int(self.spd_var.get().replace('x', ''))
            if temp >= 2:
                self.spd_var.set(value='x' + str(int(temp / 2)))
            if func is not None:
                func(self.spd_var.get())

        def spd_up_butt_func():
            """speed up button function"""
            temp = int(self.spd_var.get().replace('x', ''))
            if temp < 1024:
                self.spd_var.set(value='x' + str(temp * 2))
            if func is not None:
                func(self.spd_var.get())

        frame = ttk.LabelFrame(master=self.bframe, width=80, height=10, text='Speed Adjust')
        frame.grid(row=row, column=column)
        # speed down button
        self.spd_dw_butt = ttk.Button(frame, width=4, text='-', command=spd_dwn_butt_func)
        self.spd_dw_butt.grid(row=0, column=0)
        # speed indicator
        self.spd_var = tk.StringVar(value='x1')
        self.spd_disp = ttk.Label(frame, width=6, textvariable=self.spd_var, anchor=tk.W)
        self.spd_disp.grid(row=0, column=1)
        # speed up button
        self.spd_up_butt = ttk.Button(frame, width=4, text='+', command=spd_up_butt_func)
        self.spd_up_butt.grid(row=0, column=2)

    def build_control_butt(self,
                           row=0,
                           column=0,
                           start_func=None,
                           suspend_func=None,
                           stop_func=None):
        """
        method:
        :param row:
        :param column:
        :param start_func:
        :return:
        """
        def start_butt_func():
            """start button function"""
            if start_func is not None:
                start_func()

        def suspend_butt_func():
            """suspend button function"""
            if suspend_func is not None:
                suspend_func()

        def stop_butt_func():
            """stop button function"""
            if stop_func is not None:
                stop_func()

        frame = ttk.LabelFrame(master=self.bframe, width=80, height=10, text='Operation Control')
        frame.grid(row=row, column=column)

        # start button
        self.sta_butt = ttk.Button(frame, width=4, text='>', command=start_butt_func)
        self.sta_butt.grid(row=0, column=0)

        self.ssp_butt = ttk.Button(frame, width=4, text='||', command=suspend_butt_func)
        self.ssp_butt.grid(row=0, column=1)

        self.stp_butt = ttk.Button(frame, width=4, text='●', command=stop_butt_func)
        self.stp_butt.grid(row=0, column=2)

    def build_position_scale(self,
                             row=0,
                             column=0,
                             from_=0,
                             to=10,
                             func=None):
        """

        :param row:
        :param column:
        :param from_:
        :param to:
        :param func:
        :return:
        """
        def position_scale_func(scale_value):
            """position scale function"""
            if func is not None:
                func(scale_value)

        frame = ttk.LabelFrame(master=self.bframe, width=80, height=10, text='Position Control')
        frame.grid(row=row, column=column)
        self.position_var = tk.DoubleVar(value=0.0)
        self.position_scal = ttk.Scale(frame, from_=from_, to=to, length=200, command=position_scale_func,
                                       variable=self.position_var)
        self.position_scal.grid(row=0, column=0)

    def build_axis_mode_radiobutts(self,
                                   row=0,
                                   column=0,
                                   func=None):
        """
        method:
        :param row:
        :param column:
        :param func:
        :return:
        """
        def mode_func():
            """position scale function"""
            if func is not None:
                func(self.mode_var.get())

        frame = ttk.LabelFrame(master=self.bframe, width=80, height=12, text='t-Axis MODE:')
        frame.grid(row=row, column=column)
        # mode radio button
        self.mode_var = tk.StringVar(value='expand')
        self.expand = ttk.Radiobutton(master=frame, width=6, text='expand',
                                      value='expand', variable=self.mode_var,
                                      command=mode_func)
        self.expand.grid(row=0, column=0)
        self.shift = ttk.Radiobutton(master=frame, width=4, text='shift',
                                     value='shift', variable=self.mode_var,
                                     command=mode_func)
        self.shift.grid(row=0, column=1)
        self.fixed = ttk.Radiobutton(master=frame, width=4, text='fixed',
                                     value='fixed', variable=self.mode_var,
                                     command=mode_func)
        self.fixed.grid(row=0, column=2)

    def build_drive_mode_radiobutts(self,
                                    row=0,
                                    column=0,
                                    func=None):
        """
        method:
        :param row:
        :param column:
        :param func:
        :return:
        """
        def drive_func():
            """drive style function"""
            if func is not None:
                func(self.drive_mode_var.get())

        frame = ttk.LabelFrame(master=self.bframe, width=80, height=10, text='Drive MODE')
        frame.grid(row=row, column=column)
        # mode radio button
        self.drive_mode_var = tk.StringVar(value='auto')
        self.expand = ttk.Radiobutton(master=frame, width=4, text='auto',
                                      value='auto', variable=self.drive_mode_var,
                                      command=drive_func)
        self.expand.grid(row=0, column=0)
        self.shift = ttk.Radiobutton(master=frame, width=6, text='manual',
                                     value='manual', variable=self.drive_mode_var,
                                     command=drive_func)
        self.shift.grid(row=0, column=1)

    def mainloop(self):
        """
        method: mainloop
        :return:
        """
        self.master.mainloop()


class PhasorAnimationControlPage(AnimationControlPage):
    """
    class: create a page for control of phasor animation
    """
    def __init__(self,
                 master=None,
                 row=0,
                 column=0,
                 from_=0,
                 to=10,
                 speed_adj_func=None,
                 start_func=None,
                 suspend_func=None,
                 stop_func=None,
                 position_func=None,
                 axis_mode_func=None,
                 drive_mode_func=None):
        """
        method: create the page
        :param master: tkinter widget for placing this area
        :param row: row in .grid()
        :param from_: from in ttk.Scale
        :param to: to in ttk.Scale
        :param column: column in .grid()
        :param speed_adj_func: speed down button callback function
        :param start_func: start button callback function
        :param suspend_func: suspend button callback function
        :param stop_func: stop button callback function
        :param position_func: position function
        :param axis_mode_func: axis mode function
        :param drive_mode_func: drive mode function
        """
        super().__init__(master=master,
                         row=row,
                         column=column)

        self.build_widgets(from_=from_,
                           to=to,
                           speed_adjust_func=speed_adj_func,
                           start_func=start_func,
                           suspend_func=suspend_func,
                           stop_func=stop_func,
                           position_func=position_func,
                           axis_mode_func=axis_mode_func,
                           drive_mode_func=drive_mode_func)

    def build_widgets(self,
                      from_=0,
                      to=10,
                      speed_adjust_func=None,
                      start_func=None,
                      suspend_func=None,
                      stop_func=None,
                      position_func=None,
                      axis_mode_func=None,
                      drive_mode_func=None):
        """
        method: build widgets
        :param from_: from in ttk.Scale
        :param to: to in ttk.Scale
        :param speed_adjust_func: speed down and up button callback function
        :param start_func: start button callback function
        :param suspend_func: suspend button callback function
        :param stop_func: stop button callback function
        :param position_func: position function
        :param axis_mode_func: mode function
        :param drive_mode_func: drive mode function
        :return: None
        """
        # speed down button
        self.build_spd_adj_butt(func=speed_adjust_func, column=0)
        # control button, start, stop, suspend
        self.build_control_butt(column=1, start_func=start_func, suspend_func=suspend_func, stop_func=stop_func)
        # position button
        self.build_position_scale(column=2, func=position_func, from_=from_, to=to)
        # mode button
        self.build_axis_mode_radiobutts(column=3, func=axis_mode_func)
        # drive mode buttons
        self.build_drive_mode_radiobutts(column=4, func=drive_mode_func)


class PlotAnimationControlPage(AnimationControlPage):
    """
    class: create a page for control of plotting animation
    """
    def __init__(self,
                 master=None,
                 row=0,
                 column=0,
                 from_=0,
                 to=10,
                 speed_adj_func=None,
                 start_func=None,
                 suspend_func=None,
                 stop_func=None,
                 position_func=None,
                 axis_mode_func=None,
                 drive_mode_func=None):
        """
        method: create the page
        :param master: tkinter widget for placing this area
        :param row: row in .grid()
        :param from_: from in ttk.Scale
        :param to: to in ttk.Scale
        :param column: column in .grid()
        :param speed_adj_func: speed down button callback function
        :param start_func: start button callback function
        :param suspend_func: suspend button callback function
        :param stop_func: stop button callback function
        :param position_func: position function
        :param axis_mode_func: axis mode function
        :param drive_mode_func: drive mode function
        """
        super().__init__(master=master,
                         row=row,
                         column=column)

        self.build_widgets(from_=from_,
                           to=to,
                           speed_adjust_func=speed_adj_func,
                           start_func=start_func,
                           suspend_func=suspend_func,
                           stop_func=stop_func,
                           position_func=position_func,
                           axis_mode_func=axis_mode_func,
                           drive_mode_func=drive_mode_func)

    def build_widgets(self,
                      from_=0,
                      to=10,
                      speed_adjust_func=None,
                      start_func=None,
                      suspend_func=None,
                      stop_func=None,
                      position_func=None,
                      axis_mode_func=None,
                      drive_mode_func=None):
        """
        method: build widgets
        :param from_: from in ttk.Scale
        :param to: to in ttk.Scale
        :param speed_adjust_func: speed down and up button callback function
        :param start_func: start button callback function
        :param suspend_func: suspend button callback function
        :param stop_func: stop button callback function
        :param position_func: position function
        :param axis_mode_func: mode function
        :param drive_mode_func: drive mode function
        :return: None
        """
        # speed down button
        self.build_spd_adj_butt(func=speed_adjust_func, column=0)
        # control button, start, stop, suspend
        self.build_control_butt(column=1, start_func=start_func, suspend_func=suspend_func, stop_func=stop_func)
        # position button
        self.build_position_scale(column=2, func=position_func, from_=from_, to=to)
        # mode button
        self.build_axis_mode_radiobutts(column=3, func=axis_mode_func)
        # drive mode buttons
        self.build_drive_mode_radiobutts(column=4, func=drive_mode_func)


class ButtonsPage:
    """
    class: create a page containing certain amount of buttons
    """
    def __init__(self,
                 master=None,
                 row=0,
                 column=0,
                 wdg_width=None,
                 wdg_height=None,
                 btn_lst=None,
                 btn_width=None,
                 num_per_row=3):
        """
        method: create the button area
        :param master: tkinter widget for placing this area
        :param row: row in .grid()
        :param column: column in .grid()
        :param wdg_width: widget's width, when it's default, equals to master's width
        :param wdg_height: widget's height, when it's default, equals to master's height
        :param btn_lst: button list of str, ['butt1', 'butt2',..]
        :param btn_width: button width, list of int, [3, 3,..]
        :param num_per_row: number of buttons in every row
        """
        # master
        self.master = master

        # get width and height of master
        self.master.update()
        master_width = self.master.winfo_width()
        master_height = self.master.winfo_height()

        # get width and height of base frame
        if wdg_width is None or wdg_width > master_width:
            wdg_width = master_width - 5
        if wdg_height is None or wdg_height > master_height:
            wdg_height = master_height - 5

        # create the base frame
        self.bframe = ttk.Frame(master=master, height=wdg_height, width=wdg_width)
        self.bframe.grid(row=row, column=column)
        self.bframe.grid_propagate(0)

        # button name list and object list
        if btn_lst is None:
            self.btn_lst = ['BUTTON']
        else:
            self.btn_lst = btn_lst
        self.btn_obj = {}

        # start
        for idx, btn in enumerate(btn_lst):
            if btn_width is None:
                width = len(btn)+1
            else:
                width = btn_width[idx]
            btn_obj = ttk.Button(master=self.bframe, text=btn, width=width)
            btn_obj.grid(row=int(idx/num_per_row), column=int(idx) % num_per_row)
            self.btn_obj[btn] = btn_obj

    def command(self,
                btn_nm='BUTTON',
                cal_func=None):
        """
        method: set the call back function
        :param btn_nm: button name, str
        :param cal_func: call function
        :return: None
        """
        if btn_nm in self.btn_lst:
            self.btn_obj[btn_nm].config(command=cal_func)

    def disable(self,
                btn_lst=None):
        """
        method: disable some buttons
        :param btn_lst: button list, ['butt1', 'butt3',..]
        :return: None
        """
        if btn_lst is None:
            btn_lst = self.btn_lst
        for btn_nm in btn_lst:
            self.btn_obj[btn_nm].config(state=tk.DISABLED)

    def enable(self,
               btn_lst=None):
        """
        method: enable some buttons
        :param btn_lst: button list, ['butt1', 'butt3',..]
        :return: None
        """
        if btn_lst is None:
            btn_lst = self.btn_lst
        for btn_nm in btn_lst:
            self.btn_obj[btn_nm].config(state=tk.NORMAL)

    def destroy(self):
        """
        method: destroy itself
        """
        self.bframe.destroy()


class CheckbuttonPage:
    """
    class: a Page to display several checkbuttons
    """
    def __init__(self,
                 master=None,
                 width=None,
                 height=None,
                 row=0,
                 column=0,
                 label=None,
                 list_data=None,
                 confirm_func=None,
                 cancel_func=None):
        """
        method: init the checkbutton
        :param master: master widget for placing this page
        :param width: width of the page
        :param height: height of the page
        :param row: row in .grid()
        :param column: column in .grid()
        :param label: Page's label
        :param list_data: data to be list on the page, list, e.g., {'xx': 1, 'yy': 0,..}
        :param confirm_func: confirm button function
        :param cancel_func: cancel button function
        """
        # get the master's width and height
        master.update()
        master_width = master.winfo_width()
        master_height = master.winfo_height()

        # get the Listbox's width and height
        if width is not None:
            self.width = width
        else:
            self.width = master_width - 5
        if height is not None:
            self.height = height
        else:
            self.height = master_height

        # base frame
        self.bframe = ttk.LabelFrame(master=master, width=self.width, height=self.height, text=label)
        self.bframe.grid(row=row, column=column)
        self.bframe.grid_propagate(0)

        # frame for content
        self.frame_content = ttk.Frame(master=self.bframe, width=self.width, height=self.height-10)
        self.frame_content.grid(row=0, column=0)
        self.frame_content.grid_propagate(0)

        # frame for buttons
        self.frame_butt = ttk.Frame(master=self.bframe, width=self.width, height=10)
        self.frame_butt.grid(row=1, column=0)
        self.frame_butt.grid_propagate(0)

        self.var = {}
        for i, data in enumerate(list_data):
            self.var[data] = tk.IntVar(value=list_data[data])
            check_butt = ttk.Checkbutton(master=self.frame_content, text=data, variable=self.var[data])
            check_butt.grid(row=i, column=0)
        confirm_butt = tk.Button(master=self.frame_butt, width=5, text='confirm', command=confirm_func)
        confirm_butt.grid(row=0, column=0)
        confirm_butt = tk.Button(master=self.frame_butt, width=5, text='cancle', command=cancel_func)
        confirm_butt.grid(row=0, column=1)


class EditPage:
    """
    class: a Page to display and edit the data, including a 2 columns tabel(left is name, right is value)
    """
    def __init__(self,
                 master=None,
                 row=0,
                 column=0,
                 width=None,
                 height=None,
                 text='Save',
                 func_save=None,
                 data=None):
        """
        method: create the Page
        :param master: the tkinter's frame to place the Page
        :param row: row in tkinter's .grid()
        :param column: column in tkinter's grid()
        :param width: Page's width, which is the same as master's width when default
        :param height: Page's height, which is the same as master's height when default
        :param text: text displayed on the confirm button
        :param func_save: "save" button callback function
        :param data: data to be displayed, dict
        """
        # master
        self.master = master

        # get the master's width和height
        self.master.update()
        master_width = self.master.winfo_width()
        master_height = self.master.winfo_height()

        # get the base frame's width和height
        if width is None or width > master_width:
            width = master_width
        if height is None or height > master_height:
            height = master_height
        # create the base frame
        self.frame = tk.LabelFrame(master=master, height=height, width=width)
        self.frame.grid(row=row, column=column)
        self.frame.grid_propagate(0)

        # tabel frame and button frame's width and height
        tbl_frm_width = width - 5
        btn_frm_heigh = 30
        tbl_frm_height = height - 20 - btn_frm_heigh

        # create frame for the tabel
        self.table_frm = tk.Frame(master=self.frame, height=tbl_frm_height, width=tbl_frm_width)
        self.table_frm.grid(row=0, column=0)
        self.table_frm.grid_propagate(0)

        # create frame for the button
        self.btn_frm = tk.Frame(master=self.frame, height=btn_frm_heigh, width=tbl_frm_width)
        self.btn_frm.grid(row=1, column=0)
        self.btn_frm.grid_propagate(0)

        # get the table's column width
        self.tab_col_width = ceil(tbl_frm_width / 16)
        # get the button's width
        self.btn_width = floor(tbl_frm_width / 24) - 1

        # create "save" button
        self.btn_save = tk.Button(self.btn_frm, text=text, width=self.btn_width, font=('楷体', 12))
        self.btn_save.grid(row=0, column=0)
        self.btn_save.config(command=self.save_data)

        # tabel's name and value
        self.table_nm = {}
        self.table_vl = {}
        # Entry
        self.entry_var = {}
        # "save" button's callback function
        self.func_save = func_save

        # data
        self.data = {}

        # display data
        self.disp_data(data)

    def disp_data(self,
                  data):
        """
        method: display data
        :param data: data, dict
        """
        if data is not None:
            for idx, key in enumerate(data):
                if key == 'id' or key == 'crd_x' or key == 'crd_y' or key == 'angle' or key == 'node1' or key == \
                        'node2' or key == 'vol_dir' or key == 'cur_dir':
                    continue
                self.table_nm[key] = tk.Label(self.table_frm, text=key, width=self.tab_col_width,
                                              relief=tk.RIDGE, bd=1)
                if data[key] is True:
                    self.entry_var[key] = tk.StringVar(value='True')
                elif data[key] is False:
                    self.entry_var[key] = tk.StringVar(value='False')
                elif type(data[key]) == float:
                    self.entry_var[key] = tk.DoubleVar(value=data[key])
                elif type(data[key]) == int:
                    self.entry_var[key] = tk.IntVar(value=data[key])
                else:
                    self.entry_var[key] = tk.StringVar(value=str(data[key]))

                self.table_vl[key] = tk.Entry(self.table_frm,
                                              width=self.tab_col_width - 3,
                                              textvariable=self.entry_var[key])

                self.table_vl[key].bind("<Return>", self.save_data)

                self.table_nm[key].grid(row=idx, column=0)
                self.table_nm[key].grid_propagate(0)
                self.table_vl[key].grid(row=idx, column=1)
                self.table_vl[key].grid_propagate(0)

    def save_data(self, event=None):
        """
        method: save data
        :param event: mouse or keyboard event
        :return: None
        """
        for key in self.entry_var:
            self.data[key] = self.entry_var[key].get()
        if self.func_save:
            self.func_save()

    def command(self,
                func_save):
        """
        method: define the callback function of the "save" button
        :param func_save: "save" button callback function
        :return: None
        """
        self.func_save = func_save


class NormalEditPage:
    """
    class: a normal Page for edition of data
    """
    def __init__(self,
                 master,
                 row=0,
                 column=0,
                 width=None,
                 height=None,
                 label=None,
                 save_butt_label='Save',
                 save_butt_func=None,
                 data=None):
        """
        method: create the Page
        :param master: the tkinter's frame to place the Page
        :param row: row in tkinter's .grid()
        :param column: column in tkinter's grid()
        :param width: Page's width, which is the same as master's width when default
        :param height: Page's height, which is the same as master's height when default
        :parma label: label on the page
        :param save_butt_label: text displayed on the confirm button
        :param save_butt_func: "save" button callback function
        :param data: data to be displayed, e.g.,
        [
        {'style': 'Radiobutton', 'label': 'DATA', 'name': 'data1', 'value': ['R1', 'R2', 'R3']},
        {'style': 'Entry', 'name': 'data2', 'value': 'E1'},
        {'style': 'Checkbutton', 'name': 'data3', 'value': ['C1', 'C2', 'C3']},
        {'style': 'Range', 'name': 'data4', 'value': [0, 100]}
        ]
        """
        # master
        self.master = master
        # base frame
        self.base_frame = None
        # table frame
        self.table_frame = None
        # button frame
        self.button_frame = None
        # control Variable
        self.var = []
        # data
        self.data = data
        # callback function
        self.func = save_butt_func

        # base frame
        self.build_base_frame(label=label, width=width, height=height, row=row, column=column)
        # table frame
        self.build_table_frame(row=0, column=0)
        # button frame
        if save_butt_label is not None:
            self.build_button_frame(row=1, column=0, save_butt_label=save_butt_label)

        for i, key in enumerate(self.data):
            if key['style'] == 'Radiobutton':
                self.build_radiobutton(row=i, column=0, data=key)
            elif key['style'] == 'Entry':
                self.build_entry(row=i, column=0, data=key)
            elif key['style'] == 'Checkbutton':
                self.build_checkbutton(row=i, column=0, data=key)
            elif key['style'] == 'Range':
                self.build_range(row=i, column=0, data=key)

    def build_base_frame(self,
                         label,
                         width,
                         height,
                         row=0,
                         column=0):
        """
        method: build base frame
        :param label: label on the frame
        :param width: base frame's width,
        :param height: base frame's height
        :param row:
        :param column:
        :return: None
        """
        # get the master's width和height
        self.master.update()
        master_width = self.master.winfo_width()
        master_height = self.master.winfo_height()

        # get the base frame's width和height
        if width is None or width > master_width:
            width = master_width - 5
        if height is None or height > master_height:
            height = master_height - 5
        # create the base frame
        self.base_frame = tk.LabelFrame(master=self.master, height=height, width=width, text=label)
        self.base_frame.grid(row=row, column=column)
        self.base_frame.grid_propagate(0)

    def build_table_frame(self, row=0, column=0):
        """
        method: build table frame
        :param row:
        :param column:
        :return: None
        """
        # create frame for the tabel
        self.base_frame.update()
        table_frame_height = self.base_frame.winfo_height() - 40
        self.table_frame = ttk.Frame(master=self.base_frame, height=table_frame_height,
                                    width=self.base_frame.winfo_height())
        self.table_frame.grid(row=row, column=column)
        self.table_frame.grid_propagate(0)

    def build_button_frame(self, row=0, column=0, save_butt_label='Save'):
        """
        method: build button frame
        :param row:
        :param column:
        :param save_butt_label: save button's label
        :return: None
        """
        self.base_frame.update()
        self.button_frame = ttk.Frame(master=self.base_frame, height=40, width=self.base_frame.winfo_height())
        self.button_frame.grid(row=row, column=column)
        self.button_frame.grid_propagate(0)

        # create "save" button
        save_button = ttk.Button(self.button_frame, text=save_butt_label, width=20)
        save_button.grid(row=0, column=0)
        save_button.config(command=self.save_data)

    def _build_line_frame(self, row=0, column=0, data=None):
        """
        method: build every line's frame
        :param row:
        :param column:
        :param data: data
        :return:
        """
        if 'label' in data.keys():
            label = data['label']
        else:
            label = None
        self.table_frame.update()
        frame = ttk.LabelFrame(self.table_frame, width=self.table_frame.winfo_width(), height=30, text=label,
                              labelanchor='w')
        frame.grid(row=row, column=column)
        frame.grid_propagate(0)
        name = ttk.Label(frame, text=data['name'], width=20, anchor=tk.CENTER)
        name.grid(row=0, column=0)
        return frame

    def build_entry(self, row=0, column=0, data=None):
        """
        method: display data
        :param row:
        :param column:
        :param data: data
        """
        frame = self._build_line_frame(row=row, column=column, data=data)
        if data['name'] == 'id' or data['name'] == 'crd_x' or data['name'] == 'crd_y' or data['name'] == 'angle' or \
                data['name'] == 'node1' or data['name'] == 'node2' or data['name'] == 'vol_dir' or \
                data['name'] == 'cur_dir':
            return
        if type(data['value']) == float:
            ctrl_var = tk.DoubleVar(value=data['value'])
        elif type(data['value']) == int:
            ctrl_var = tk.IntVar(value=data['value'])
        else:
            ctrl_var = tk.StringVar(value=str(data['value']))

        entry = ttk.Entry(frame, width=10, textvariable=ctrl_var)
        entry.grid(row=0, column=1)
        entry.grid_propagate(0)

        # entry.bind("<Return>", self.save_data)
        self.var.append(ctrl_var)

    def build_radiobutton(self, row=0, column=0, data=None):
        """
        method: build radiobutton
        :param row:
        :param column:
        :param data: data
        :return:
        """
        frame = self._build_line_frame(row=row, column=column, data=data)
        value_0 = data['value'][0]
        if type(value_0) == float:
            ctrl_var = tk.DoubleVar(value=value_0)
            width = 3
        elif type(value_0) == int:
            ctrl_var = tk.IntVar(value=value_0)
            width = 3
        else:
            ctrl_var = tk.StringVar(value=value_0)
            width = len(value_0)
        for i, value in enumerate(data['value']):
            radiobutton = ttk.Radiobutton(master=frame, width=width, text=value, value=value, variable=ctrl_var)
            radiobutton.grid(row=0, column=i+1)

        self.var.append(ctrl_var)

    def build_checkbutton(self, row=0, column=0, data=None):
        """
        method: build checkbutton
        :param row:
        :param column:
        :param data:
        :return:
        """
        frame = self._build_line_frame(row=row, column=column, data=data)
        ctrl_vars = []
        for i, value in enumerate(data['value']):
            ctrl_var = tk.IntVar(value=0)
            ctrl_vars.append(ctrl_var)
            checkbutton = ttk.Checkbutton(master=frame, width=len(value), text=value, variable=ctrl_var)
            checkbutton.grid(row=0, column=i+1)

        self.var.append(ctrl_vars)

    def build_range(self, row=0, column=0, data=None):
        """
        method: build range
        :param row:
        :param column:
        :param data:
        :return:
        """
        frame = self._build_line_frame(row=row, column=column, data=data)
        from_var = tk.DoubleVar(value=data['value'][0])
        to_var = tk.DoubleVar(value=data['value'][1])
        from_entry = ttk.Entry(frame, width=6, textvariable=from_var)
        from_entry.grid(row=0, column=1)
        ttk.Label(frame, width=2, text='-', anchor=tk.CENTER).grid(row=0, column=2)
        to_entry = ttk.Entry(frame, width=6, textvariable=to_var)
        to_entry.grid(row=0, column=3)

        self.var.append((from_var, to_var))

    def save_data(self):
        """
        method: save data
        :param func: callback function
        :return: None
        """
        save_data = []
        for i, key in enumerate(self.data):
            if key['style'] == 'Radiobutton':
                save_data.append(self.var[i].get())
            elif key['style'] == 'Entry':
                save_data.append(self.var[i].get())
            elif key['style'] == 'Checkbutton':
                check_data = []
                for j, sub_key in enumerate(key['value']):
                    if self.var[i][j].get():
                        check_data.append(sub_key)
                save_data.append(check_data)
            elif key['style'] == 'Range':
                save_data.append([self.var[i][0].get(), self.var[i][1].get()])

        if self.func:
            self.func(save_data)

    def command(self,
                save_butt_func):
        """
        method: define the callback function of the "save" button
        :param save_butt_func: "save" button callback function
        :return: None
        """
        self.func = save_butt_func


class ScrollCanvas:
    """
    class: a Canvas with x and y Scrollbars.
    can be placed on a tkinter.Frame. the scroll bar will disapear when the Canvas' geometry is less than the Frame.
    """
    def __init__(self,
                 master,
                 row=0,
                 column=0,
                 wdg_width=None,
                 wdg_height=None,
                 cav_width=None,
                 cav_height=None,
                 grid=None):
        """
        method: create the ScrollCanvas
        :param master: the tkinter Frame for placing the ScrollCanvas
        :param row: row in .grid(), default is 0
        :param column: column in .grid(), default is 0
        :param wdg_width: width of the ScrollCanvas, when default, the ScrollCanvas's width is the same as the master's
        width, e.g., 1200
        :param wdg_height: height of the ScrollCanvas, when default, the ScrollCanvas's width is the same as the
        master's height, e.g., 800
        :param cav_width: width of the Canvas, when default, the Canvas's width is the same as ScrollCanvas's width
        :param cav_height: height of the Canvas, when default, the Canvas's height is the same as ScrollCanvas's height
        :param grid: if grid is on the Canvas, True or False
        """
        self.master = master

        # get the master's width and height
        self.master.update()
        pfrm_width = self.master.winfo_width()
        pfrm_height = self.master.winfo_height()

        # get the master's width and height
        if wdg_width is None:
            wdg_width = pfrm_width - 10
        if wdg_height is None:
            wdg_height = pfrm_height - 25

        # get the self.__scrollregion
        if cav_width is None:
            cav_width = wdg_width
        if cav_height is None:
            cav_height = wdg_height
        self.__cav_width = cav_width
        self.__cav_height = cav_height
        self.__scrollregion = (0, 0, cav_width, cav_height)

        # create the base frame
        self.__frame = tk.Frame(self.master, width=wdg_width, height=wdg_height)
        self.__frame.grid(row=row, column=column)
        # create 1 canvas and 2 scrollbar on the frame
        self.canvas = tk.Canvas(self.__frame, width=wdg_width, height=wdg_height,
                                scrollregion=self.__scrollregion, bg='white')
        self.canvas.grid(row=0, column=0)
        if cav_width > wdg_width:
            self.canvas.config(width=wdg_width - 20)
            x_sbar = tk.Scrollbar(self.__frame, orient=tk.HORIZONTAL, width=20)
            self.canvas.config(xscrollcommand=x_sbar.set)
            x_sbar.config(command=self.canvas.xview)
            x_sbar.grid(row=1, column=0, sticky=tk.EW)
        if cav_height > wdg_height:
            self.canvas.config(height=wdg_height - 20)
            y_sbar = tk.Scrollbar(self.__frame, orient=tk.VERTICAL, width=20)
            self.canvas.config(yscrollcommand=y_sbar.set)
            y_sbar.config(command=self.canvas.yview)
            y_sbar.grid(row=0, column=1, sticky=tk.NS)

        # create grid
        self.creat_grid(grid=grid)

        # the mouse wheel event's callback function
        def mouse_wheel(event):
            a = int(-event.delta / 60)
            self.canvas.yview_scroll(a, 'units')

        # the shift+mouse whell event's callback function
        def shift_mouse_wheel(event):
            a = int(-event.delta / 60)
            self.canvas.xview_scroll(a, 'units')

        self.canvas.bind("<MouseWheel>", mouse_wheel, add='+')
        self.canvas.bind("<Shift-MouseWheel>", shift_mouse_wheel, add='+')

    def creat_grid(self,
                   grid=None):
        """
        method: create the grid
        :param grid: grid parameter, None: no grid, number: the interval of grid, e.g., None, 10, 20, etc,..
        :return: None
        """
        if grid:
            for i in range(1, int(self.__cav_width/grid)):
                for j in range(1, int(self.__cav_height / grid)):
                    self.canvas.create_oval(i*grid-1, j*grid-1, i*grid+1, j*grid+1, width=1, outline='#0696F7')

    def destroy(self):
        """
        method: tkinter's .destroy()
        :return: None
        """
        self.__frame.destroy()


class ScrollFrame(ScrollCanvas):
    """
    class: a Frame with x and y Scrollbars, subclass of ScrollCanvas
    refer to Elecpy.GUIElements.ScrollCanvas
    """
    def __init__(self,
                 master=None,
                 row=0,
                 column=0,
                 wdg_width=None,
                 wdg_height=None,
                 frm_width=None,
                 frm_height=None):
        """
        method: create a ScrollFrame
        :param row: row in .grid()
        :param column: column in .grid()
        :param wdg_width: width of ScrollCanvas's width, when default, is the same as master's width
        :param wdg_height: height of ScrollCanvas's width, when default, is the same as master's height
        :param frm_width: width of the Frame
        :param frm_height: height of the Frame
        """
        scroll_canvas = super().__init__(master=master,
                                         row=row,
                                         column=column,
                                         wdg_width=wdg_width,
                                         wdg_height=wdg_height,
                                         cav_width=frm_width,
                                         cav_height=frm_height).canvas
        win = scroll_canvas.create_window()
        self.frame = tk.Frame(win,
                              width=frm_width,
                              height=frm_height)


class ContentPage:
    """
    class: a page to display a content.
    """
    def __init__(self,
                 master=None,
                 row=0,
                 column=0,
                 wdg_width=None,
                 wdg_height=None,
                 cont_data=None,
                 fold_flag=None):
        """
        method: create the page
        :param master: the widget for placing the content, tkinter.Frame
        :param row: row in .grid()
        :param column: column in .grid()
        :param wdg_width: width of Contents' width, when default, is the same as master's width
        :param wdg_height: height of Contents's width, when default, is the same as master's height
        :param cont_data: data for displaying, pandas.DataFrame
        :param fold_flag: fold or unfold flag, False: fold, True: unfold, list([False, True, ...])
        """
        self.master = master
        if cont_data is not None:
            self.cont_data = cont_data.sort_index(ascending=False)
        else:
            self.cont_data = pd.DataFrame({'1L': ['1L1', '1L1', '1L1', '1L1', '1L1', '1L1'],
                                           '2L': ['2L1', '2L1', '2L1', '2L1', '2L1', '2L1'],
                                           '3L': ['3L1', '3L1', '3L1', '3L1', '3L2', '3L2'],
                                           '4L': ['4L1', '4L1', '4L2', '4L2', '4L3', '4L3'],
                                           '5L': ['5L1', '5L2', '5L3', '5L4', '5L5', '5L5']})
        self.cont_data.sort_values(by=list(self.cont_data.keys()))
        # fold flag
        if fold_flag is None:
            fold_flag = []
            length = len(self.cont_data.keys())
            for i in range(length):
                if i == length-2:
                    fold_flag.append(False)
                else:
                    fold_flag.append(True)

        self.work_area = None

        # get parent frame's width and height
        self.master.update()
        pfrm_width = self.master.winfo_width()
        pfrm_height = self.master.winfo_height()

        # get the base frame's width and height
        if wdg_width is None or wdg_width > pfrm_width - 10:
            wdg_width = pfrm_width - 10
        if wdg_height is None or wdg_height > pfrm_height - 20:
            wdg_wheight = pfrm_height - 20

        # base frame
        self.frame = tk.LabelFrame(self.master, width=wdg_width, height=wdg_height, font=('仿宋', 12), text='content')
        self.frame.grid(row=row, column=column)
        self.frame.grid_propagate(0)

        # read the content
        self.tree = ttk.Treeview(master=self.frame, show='tree')
        self.tree.column('#0', width=wdg_width-10)
        self.tree.grid(row=row, column=column)

        tree_list = {}
        for col in self.cont_data.columns:
            tree_list[col] = []

        for idx in self.cont_data.index:
            name = ''
            for i, col in enumerate(self.cont_data.columns):
                parent_name = name
                name = self.cont_data.loc[idx, col]
                if name not in tree_list[col]:
                    tree_list[col].append(name)
                    self.tree.insert(parent=parent_name, index=0, iid=name, text=name, open=fold_flag[i])

    def command(self,
                cal_func=None):
        """
        method: call back function
        :param cal_func:
        """
        def treeslct_func(event):
            tree_focus = self.tree.focus()
            cal_func(tree_focus)

        # when some item is selected
        if cal_func is not None:
            self.tree.bind(sequence='<<TreeviewSelect>>', func=treeslct_func)
        else:
            self.tree.unbind(sequence='<<TreeviewSelect>>')

    def destroy(self):
        """
        method: destroy
        """
        self.frame.destroy()


class MenuPage:
    """
    class: Menu Page
    """
    def __init__(self,
                 master=None,
                 row=0,
                 column=0,
                 menu_cont=None,
                 cal_func=None):
        """
        method: creat a menu page
        :param master: widget to place the MenuArea, tkinter.Frame
        :param menu_cont: menu content, dict({'menu1': list(['sub menu1', 'sub menu2', ...]),
        'menu2': list(['sub menu1', 'sub menu2', ...])})
        :param cal_func: call back function, dict({'sub menu1': cal_func1, 'sub menu2': cal_func2, ...})
        """
        # create a base frame on the master
        self.bframe = tk.Frame(master, width=200, height=100, relief=tk.RAISED, bg='green')
        self.bframe.grid(row=row, column=column)
        # content of the menu
        self.menu_cont = menu_cont
        # call back function
        if cal_func is None:
            cal_func = {}

        menu_obj = {}

        if self.menu_cont:
            for i, menu_nm in enumerate(self.menu_cont):
                menu_btn = tk.Menubutton(self.bframe, text=menu_nm, underline=0)
                menu_btn.grid(row=0, column=i)
                menu_obj[menu_nm] = tk.Menu(menu_btn, tearoff=0)
                menu_btn.config(menu=menu_obj[menu_nm])
                for j, sub_menu_nm in enumerate(self.menu_cont[menu_nm]):
                    if sub_menu_nm in cal_func.keys():
                        menu_obj[menu_nm].add_command(label=sub_menu_nm, command=cal_func[sub_menu_nm], underline=0)

                    else:
                        menu_obj[menu_nm].add_command(label=sub_menu_nm, command=None, underline=0)


class ListboxPage:
    """
    class Listbox widget
    """
    def __init__(self,
                 master=None,
                 width=None,
                 height=None,
                 row=0,
                 column=0,
                 label=None,
                 list_data=None,
                 nrows=10):
        """
        method: init the listbox page
        :param master: the tkinter's frame to place the Page
        :param width: Page's width, which is the same as master's width when default
        :param height: Page's height, which is the same as master's height when default
        :param label: label of the listbox page, str, e.g., 'ComponentVoltage'
        :param list_data: list consist of str, e.g., ['aaa', 'bbb']
        :parma nrows: number of rows for list
        """
        # get the master's width and height
        master.update()
        master_width = master.winfo_width()
        master_height = master.winfo_height()

        # get the Listbox's width and height
        if width is not None:
            self.width = width
        else:
            self.width = master_width - 5
        if height is not None:
            self.height = height
        else:
            self.height = master_height

        # base frame
        self.label = label
        self.bframe = ttk.LabelFrame(master=master, width=self.width, height=self.height, text=label)
        self.bframe.grid(row=row, column=column)
        self.bframe.grid_propagate(0)

        # Listbox
        self.listbox = None
        # list data
        self.list_data = list_data
        # listvariable
        self.listvariable = []

        self.set_data(list_data=list_data)

        self.yScroll = ttk.Scrollbar(self.bframe, orient=tk.VERTICAL)
        self.yScroll.grid(row=0, column=1, sticky=tk.N + tk.S)
        self.xScroll = ttk.Scrollbar(self.bframe, orient=tk.HORIZONTAL)
        self.xScroll.grid(row=1, column=0, sticky=tk.E + tk.W)
        self.listbox = tk.Listbox(master=self.bframe, listvariable=self.listvariable, width=int(self.width / 8),
                                  height=nrows, activestyle='none',
                                  xscrollcommand=self.xScroll.set,
                                  yscrollcommand=self.yScroll.set)
        self.listbox.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.xScroll['command'] = self.listbox.xview
        self.yScroll['command'] = self.listbox.yview

    def set_data(self,
                 list_data=None):
        """
        method: set the list's data
        :param list_data: list consist of str, e.g., ['aaa', 'bbb']
        :return: None
        """
        if list_data is not None:
            if self.listvariable:
                self.listvariable.set(value=list_data)
            else:
                self.listvariable = tk.StringVar(value=list_data)

    def command(self,
                cal_func):
        """
        method: config the cal_func
        :param cal_func: call back function, func(selected elment)
        :return: None
        """
        def func(event):
            """callback function"""
            if cal_func is not None:
                cal_func(self.label, self.get_selection(event))

        self.listbox.bind("<Double-Button-1>", func)

    def get_selection(self,
                      event=None):
        """
        method: get the selection item's number, from 0
        :param: listbox event
        :return: selection number, e.g., 0, 1, ..
        """
        if self.listbox.curselection():
            for i, key in enumerate(self.list_data):
                if i == self.listbox.curselection()[0]:
                    return key
        else:
            return None


class RadiobuttonPage:
    """
    class: Page to place several radiobuttons
    """
    def __init__(self,
                 master=None,
                 width=None,
                 height=None,
                 row=0,
                 column=0,
                 label=None,
                 list_data=None,
                 func=None):
        """
        method: init the Radiobutton page
        :param master: the tkinter's frame to place the Page
        :param width: Page's width, which is the same as master's width when default
        :param height: Page's height, which is the same as master's height when default
        :param label: label of the listbox page, str, e.g., 'ComponentVoltage'
        :param list_data: list consist of str, e.g., ['aaa', 'bbb']
        :param func: callback function, func(select_item)
        """
        # get the master's width and height
        master.update()
        master_width = master.winfo_width()
        master_height = master.winfo_height()

        # get the Listbox's width and height
        if width is not None:
            self.width = width
        else:
            self.width = master_width - 5
        if height is not None:
            self.height = height
        else:
            self.height = master_height

        # base frame
        self.bframe = ttk.LabelFrame(master=master, width=self.width, height=self.height, text=label)
        self.bframe.grid(row=row, column=column)
        self.bframe.grid_propagate(0)

        # Listbox
        self.radiobuttons = {}
        # listdata
        self.list_data = []
        # listvariable
        self.int_var = None
        # callback function
        self.func = func

        self.set_data(list_data=list_data)

    def set_data(self,
                 list_data):
        """
        method
        :return:
        """
        # delete the old radiobuttons
        for key in self.list_data:
            self.radiobuttons[key].destroy()
        self.radiobuttons.clear()
        # get the new radiobuttons
        if list_data is not None:
            self.list_data = list_data
        self.int_var = tk.StringVar()

        def func():
            """callback function"""
            self.func(self.int_var.get())

        for i, key in enumerate(self.list_data):
            self.radiobuttons[key] = ttk.Radiobutton(master=self.bframe, width=int(self.width / 8), text=key,
                                                     value=key, variable=self.int_var,
                                                     command=func)
            self.radiobuttons[key].grid(row=i, column=0)


if __name__ == '__main__':
    new_win = NormalWin(width=200, height=200)

    new_win.mainloop()

