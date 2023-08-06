"""
functions for drawing circuit component's diagram, such as draw_resistor, draw_capacitor, etc..
"""
import tkinter as tk
from Elecpy.Tools import *
import tkinter.font as tkFont


def draw_sine_symbol(tags='',
                     cnt_crd=None,
                     angle=0,
                     canvas=None,
                     lwidth=None,
                     lcolor=None,
                     radius=10.0):
    """
    func: draw the sine wave symbol
    :param tags: canvas geometry's tags, passing component id, str, e.g., 'voltage_ac-1'
    :param cnt_crd: center coordinate, tuple, e.g., (x, y)
    :param angle: angle, e.g., 0, 90, 180, 270, etc,..
    :param canvas: tkinter Canvas
    :param lwidth: line width
    :param lcolor: line color
    :param radius: radius of the circle around the sine wave symbol
    :return: None
    """
    x0 = cnt_crd[0] - radius / 2
    y0 = cnt_crd[1] - radius / 4 * sin((x0 - cnt_crd[0] - radius / 2) * 2 * pi / radius)
    x1 = x0 + radius / 4
    y1 = cnt_crd[1] - radius / 4 * sin((x1 - cnt_crd[0] - radius / 2) * 2 * pi / radius)
    x2 = x1 + radius / 4
    y2 = cnt_crd[1] - radius / 4 * sin((x2 - cnt_crd[0] - radius / 2) * 2 * pi / radius)
    x3 = x2 + radius / 4
    y3 = cnt_crd[1] - radius / 4 * sin((x3 - cnt_crd[0] - radius / 2) * 2 * pi / radius)
    x4 = x3 + radius / 4
    y4 = cnt_crd[1] - radius / 4 * sin((x4 - cnt_crd[0] - radius / 2) * 2 * pi / radius)
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    x2, y2 = coord_mirr_rota(orig_crd=(x2, y2), cnt_crd=cnt_crd, angle=angle)
    x3, y3 = coord_mirr_rota(orig_crd=(x3, y3), cnt_crd=cnt_crd, angle=angle)
    x4, y4 = coord_mirr_rota(orig_crd=(x4, y4), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, fill=lcolor, width=lwidth, smooth=True, tags=tags)


def draw_2_pins(tags='',
                cnt_crd=None,
                angle=0,
                canvas=None,
                pin_len=25,
                pin1_color=None,
                pin2_color=None,
                lwidth=None,
                distance=10.0):
    """
    func: draw 2 pins in component with 2 pins
    :param tags: canvas geometry's tags, passing component id, str, e.g., 'voltage_ac-1'
    :param cnt_crd: center coordinate, tuple, e.g., (x, y)
    :param angle: angle, e.g., 0, 90, 180, 270, etc,..
    :param canvas: tkinter Canvas
    :param pin_len: pin length
    :param pin1_color: pin1's color
    :param pin2_color: pin2's color
    :param lwidth: line width
    :param distance: distance between 2 pins
    :return: 2 terminals' coordinates, ((x1, y1), (x2, y2))
    """
    # pin1
    x1_0 = cnt_crd[0] - (distance / 2 + pin_len)
    y1_0 = cnt_crd[1]
    x1_1 = cnt_crd[0] - (distance / 2)
    y1_1 = cnt_crd[1]
    x1_0, y1_0 = coord_mirr_rota(orig_crd=(x1_0, y1_0), cnt_crd=cnt_crd, angle=angle)
    x1_1, y1_1 = coord_mirr_rota(orig_crd=(x1_1, y1_1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x1_0, y1_0, x1_1, y1_1, fill=pin1_color, width=lwidth, tags=tags)

    # pin2
    x2_0 = cnt_crd[0] + (distance / 2 + pin_len)
    y2_0 = cnt_crd[1]
    x2_1 = cnt_crd[0] + (distance / 2)
    y2_1 = cnt_crd[1]
    x2_0, y2_0 = coord_mirr_rota(orig_crd=(x2_0, y2_0), cnt_crd=cnt_crd, angle=angle)
    x2_1, y2_1 = coord_mirr_rota(orig_crd=(x2_1, y2_1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x2_0, y2_0, x2_1, y2_1, fill=pin2_color, width=lwidth, tags=tags)
    return (x1_0, y1_0), (x2_0, y2_0)


def draw_1_pin(tags='',
               cnt_crd=None,
               angle=0,
               canvas=None,
               pin_len=20,
               pin_color=None,
               lwidth=None):
    """
    func: draw 1 pin
    :param tags: canvas geometry's tags, passing component id, str, e.g., 'voltage_ac-1'
    :param cnt_crd: center coordinate, tuple, e.g., (x, y)
    :param angle: angle, e.g., 0, 90, 180, 270, etc,..
    :param canvas: tkinter Canvas
    :param pin_len: pin length
    :param pin_color: pin's color
    :param lwidth: line width
    :return: (x1_0, y1_0),
    """
    x1_0 = cnt_crd[0] - pin_len
    y1_0 = cnt_crd[1]
    x1_1 = cnt_crd[0]
    y1_1 = cnt_crd[1]
    x1_0, y1_0 = coord_mirr_rota(orig_crd=(x1_0, y1_0), cnt_crd=cnt_crd, angle=angle)
    x1_1, y1_1 = coord_mirr_rota(orig_crd=(x1_1, y1_1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x1_0, y1_0, x1_1, y1_1, fill=pin_color, width=lwidth, tags=tags)
    return (x1_0, y1_0),


def draw_arrow(id='a?',
               cnt_crd=None,
               angle=0,
               canvas=None,
               slct=False,
               color='black',
               tail_len=10,
               arrw_len=20,
               arrw_wid=5):
    """
    func: draw an arrow
    :param id:
    :param cnt_crd:
    :param angle:
    :param canvas:
    :param slct:
    :param color:
    :param tail_len: tail length
    :param arrw_len: head length
    :param arrw_wid: head width
    :return: {'square': (square_x , square_y)}
    """
    if cnt_crd is None:
        cnt_crd = (400, 400)

    if slct:
        lwidth = 4
        color = 'blue'
    else:
        lwidth = 2
        color = color

    # draw the line
    x0 = cnt_crd[0] - tail_len
    y0 = cnt_crd[1]
    x1 = cnt_crd[0] + arrw_len
    y1 = cnt_crd[1]
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, fill=color, width=lwidth, tags=id,
                       arrow=tk.LAST, arrowshape=(arrw_len, sqrt(arrw_wid**2+arrw_len**2), arrw_wid))

    # square
    square_x = (tail_len + arrw_len) / 2
    square_y = arrw_wid
    square_x, square_y = coord_mirr_rota(orig_crd=(square_x, square_y), cnt_crd=(0, 0), angle=angle)

    # return
    return {'square': (abs(square_x * 2), abs(square_y * 2))}


def draw_pn(id='Gph-?',
            cnt_crd=None,
            angle=0,
            canvas=None,
            slct=False,
            distance=10,
            size=8,
            color='black'):
    """
    func: draw a positive-negative symbol
    :param id:
    :param cnt_crd:
    :param angle:
    :param canvas:
    :param slct:
    :param distance: distance between positive and negative
    :param size: size of the symbols
    :param color: color of the symbols
    :return: {'square': (square_x, square_y)}
    """
    if cnt_crd is None:
        cnt_crd = (400, 400)

    if slct:
        size = 10
        color = 'blue'
    else:
        size = size
        color = color

    # draw the + -
    x0 = cnt_crd[0] - distance / 2
    y0 = cnt_crd[1]
    x1 = cnt_crd[0] + distance / 2
    y1 = cnt_crd[1]
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    font = tkFont.Font(size=size,
                       weight='bold')
    canvas.create_text(x0,
                       y0,
                       text='+',
                       font=font,
                       tag=id,
                       fill=color,
                       activefill='blue')
    canvas.create_text(x1,
                       y1,
                       text='-',
                       font=font,
                       tag=id,
                       fill=color,
                       activefill='blue')

    # square
    square_x = distance / 2
    square_y = (size + 6) / 2
    square_x, square_y = coord_mirr_rota(orig_crd=(square_x, square_y), cnt_crd=(0, 0), angle=angle)

    # return
    return {'square': (abs(square_x * 2), abs(square_y * 2))}


def draw_tmnl_circle(id='compnm-?',
                     tmnls_crd=((0, 0), (0, 0)),
                     canvas=None):
    """
    func: draw a circle in the component's terminal
    :param id: component id
    :param tmnls_crd: terminal's coordinate, e.g., tuple((x1, y1), (x2, y2))
    :param canvas: tkinter Canvas
    :return: None
    """
    for crd in tmnls_crd:
        cen_x = crd[0]
        cen_y = crd[1]
        canvas.create_oval(cen_x - 2, cen_y - 2, cen_x + 2, cen_y + 2, outline='black', fill='black',
                           width=1, activefill='green', activeoutline='green', activewidth=8, tag=id)


def draw_resistor_rect(id='R?',
                       cnt_crd=None,
                       angle=0,
                       canvas=None,
                       slct=False,
                       tmnls_vol=None,
                       max_vol=1.0):
    """
    func: draw a resistor with a rectangle
    :param id: component id, e.g., 'resistor-1'
    :param cnt_crd: component's center coordinate, e.g., (x, y)
    :param angle: component's angle, e.g., 0, 90, 180, 270, etc..
    :param canvas: tkinter Canvas
    :param slct: select status of the component, True or False
    :param tmnls_vol: terminal's voltage, tuple or list, consist of float, unit is voltage, e.g., (0.0, 0.0)
    :param max_vol: the maximum voltage in the circuit, float, unit is voltage , e.g., 0.0
    :return: {'square': (square_x, square_y), 'tmnls_crd': ((x1, y1), (x2, y2))}
    """
    if tmnls_vol is None:
        tmnls_vol = (0.0, 0.0)
    if cnt_crd is None:
        cnt_crd = (400, 400)

    # rectangle length and width
    length = 40
    width = 10
    # pin length
    pin_len = 20
    # line width and color
    if slct:
        lwidth = 4
        pin1_color = 'blue'
        pin2_color = 'blue'
        rect_color = 'blue'
    else:
        lwidth = 2
        if tmnls_vol[0] / max_vol > 0.5:
            pin1_color = 'red'
        else:
            pin1_color = 'black'
        if tmnls_vol[1] / max_vol > 0.5:
            pin2_color = 'red'
        else:
            pin2_color = 'black'
        if pin1_color == 'red' or pin2_color == 'red':
            rect_color = 'red'
        else:
            rect_color = 'black'
    # square of the rectangle
    square_x = length / 2
    square_y = width / 2
    square_x, square_y = coord_mirr_rota(orig_crd=(square_x, square_y),
                                         cnt_crd=(0, 0),
                                         angle=angle)

    # draw the rectangle
    x0 = cnt_crd[0] - (length / 2)
    y0 = cnt_crd[1] - (width / 2)
    x1 = cnt_crd[0] + (length / 2)
    y1 = cnt_crd[1] + (width / 2)
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_rectangle(x0, y0, x1, y1, outline=rect_color, tags=id, width=lwidth)

    # draw 2 pins
    tmnls_crd = draw_2_pins(tags=id, cnt_crd=cnt_crd, angle=angle, canvas=canvas, pin_len=pin_len,
                            pin1_color=pin1_color, pin2_color=pin2_color, lwidth=lwidth, distance=length)
    # return
    return {'square': (abs(square_x * 2), abs(square_y * 2)), 'tmnls_crd': tmnls_crd}


def draw_resistor_wave(id='R?',
                       cnt_crd=None,
                       angle=0,
                       canvas=None,
                       slct=False,
                       tmnls_vol=None,
                       max_vol=1.0):
    """
    func: draw the resistor with wave style
    :param id: resistor id, e.g., 'resistor-1'
    :param cnt_crd: center coordinate, e.g., (100, 100)
    :param angle: angle, e.g., 0, 90, 180, 270, etc,..
    :param canvas: tkinter Canvas
    :param slct: select status, True or False
    :param tmnls_vol: terminal voltage, unit is V, tuple or list, e.g., (10.0, 0.0)
    :param max_vol: the maximum voltage in the circuit, unit is V, float, e.g., 10.0
    :return: {'square': (square_x, square_y), 'tmnls_crd': ((x1, y1), (x2, y2))}
    """
    if tmnls_vol is None:
        tmnls_vol = (0.0, 0.0)
    if cnt_crd is None:
        cnt_crd = (400, 400)

    # length and width of the contour of the wave
    length = 40
    width = 15
    # wave number
    wave_num = 4
    # pin length
    pin_len = 20
    # line width and color
    if slct:
        lwidth = 4
        pin1_color = 'blue'
        pin2_color = 'blue'
        wave_color = 'blue'
    else:
        lwidth = 2
        if tmnls_vol[0] / max_vol > 0.5:
            pin1_color = 'red'
        else:
            pin1_color = 'black'
        if tmnls_vol[1] / max_vol > 0.5:
            pin2_color = 'red'
        else:
            pin2_color = 'black'
        if pin1_color == 'red' or pin2_color == 'red':
            wave_color = 'red'
        else:
            wave_color = 'black'
    # square of contour around the wave
    square_x = length / 2
    square_y = width / 2
    square_x, square_y = coord_mirr_rota(orig_crd=(square_x, square_y),
                                         cnt_crd=(0, 0),
                                         angle=angle)

    # draw the wave
    wave_len = int(length/wave_num)
    for i in range(wave_num):
        x0 = cnt_crd[0] - int(length / 2) + i * wave_len
        y0 = cnt_crd[1]
        x1 = x0 + int(wave_len / 4)
        y1 = y0 - int(width/2)
        x2 = x0 + int(wave_len * 3 / 4)
        y2 = y0 + int(width/2)
        x3 = x0 + wave_len
        y3 = y0
        x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
        x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
        x2, y2 = coord_mirr_rota(orig_crd=(x2, y2), cnt_crd=cnt_crd, angle=angle)
        x3, y3 = coord_mirr_rota(orig_crd=(x3, y3), cnt_crd=cnt_crd, angle=angle)
        canvas.create_line(x0, y0, x1, y1, x2, y2, x3, y3, fill=wave_color, tags=id, width=lwidth)

    # draw 2 pins
    tmnls_crd = draw_2_pins(tags=id, cnt_crd=cnt_crd, angle=angle, canvas=canvas, pin_len=pin_len,
                            pin1_color=pin1_color, pin2_color=pin2_color, lwidth=lwidth, distance=length)

    # return
    return {'square': (abs(square_x * 2), abs(square_y * 2)), 'tmnls_crd': tmnls_crd}


def draw_capacitor(id='capacitor-?',
                   cnt_crd=None,
                   angle=0,
                   canvas=None,
                   slct=False,
                   tmnls_vol=None,
                   max_vol=1.0):
    """
    func: draw capacitor
    :param id: capacitor id, e.g., 'capacitor-1'
    :param cnt_crd: center coordinate, (0, 0)
    :param angle: angle, e.g., 0, 90, 180, 270, etc,..
    :param canvas: tkinter Canvas
    :param slct: select status
    :param tmnls_vol: terminal's voltage, unit is V, tuple, e.g., (0.0, 0.0)
    :param max_vol: maximum voltage, unit is V, float, e.g., 10.0
    :return: {'square': (square_x, square_y), 'tmnls_crd': ((x1, y1), (x2, y2))}
    """
    if cnt_crd is None:
        cnt_crd = (400, 400)
    if tmnls_vol is None:
        tmnls_vol = (0.0, 0.0)

    # distance between two poles
    dstn = 10
    # length of pole
    length = 30
    # pin length
    pin_len = 15
    if slct:
        lwidth = 4
        pin1_color = 'blue'
        pin2_color = 'blue'
    else:
        lwidth = 2
        if tmnls_vol[0] / max_vol > 0.5:
            pin1_color = 'red'
        else:
            pin1_color = 'black'
        if tmnls_vol[1] / max_vol > 0.5:
            pin2_color = 'red'
        else:
            pin2_color = 'black'

    # draw two poles
    x0 = cnt_crd[0] - (dstn / 2)
    y0 = cnt_crd[1] - (length / 2)
    x1 = cnt_crd[0] - (dstn / 2)
    y1 = cnt_crd[1] + (length / 2)
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, fill=pin1_color, tags=id, width=lwidth)

    x0 = cnt_crd[0] + (dstn / 2)
    y0 = cnt_crd[1] - (length / 2)
    x1 = cnt_crd[0] + (dstn / 2)
    y1 = cnt_crd[1] + (length / 2)
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, fill=pin2_color, tags=id, width=lwidth)

    # draw 2 pins
    tmnls_crd = draw_2_pins(tags=id, cnt_crd=cnt_crd, angle=angle, canvas=canvas, pin_len=pin_len,
                            pin1_color=pin1_color, pin2_color=pin2_color, lwidth=lwidth, distance=dstn)

    # square of the contour around the capacitor(not including the pin)
    square_x = dstn/2
    square_y = length / 2
    square_x, square_y = coord_mirr_rota(orig_crd=(square_x, square_y), cnt_crd=(0, 0), angle=angle)

    # return
    return {'square': (abs(square_x * 2), abs(square_y * 2)), 'tmnls_crd': tmnls_crd}


def draw_inductor(id='R?',
                  cnt_crd=None,
                  angle=0,
                  canvas=None,
                  slct=False,
                  tmnls_vol=None,
                  max_vol=None):
    """
    func: draw inductor
    :param id: inductor id, e.g., 'inductor-1'
    :param cnt_crd: center coordinate, e.g., (x, y)
    :param angle: angle, e.g., 0, 90, 180, 270, etc,..
    :param canvas: tkinter Canvas
    :param slct: select status, True or False
    :param tmnls_vol: terminals' voltage, tuple or list, e.g., (10.0, 0.0)
    :param max_vol: the maximum voltage in the circuit, V, e.g., 10.0
    :return: {'square': (square_x, square_y), 'tmnls_crd': ((x1, y1), (x2, y2))}
    """
    if tmnls_vol is None:
        tmnls_vol = (0.0, 0.0)
    if cnt_crd is None:
        cnt_crd = (400, 400)

    # draw length of the inductor
    length = 60
    # wave number
    wave_num = 4
    # pin length
    pin_len = 10
    # line width and color
    if slct:
        lwidth = 4
        pin1_color = 'blue'
        pin2_color = 'blue'
        wave_color = 'blue'
    else:
        lwidth = 1.5
        if tmnls_vol[0] / max_vol > 0.5:
            pin1_color = 'red'
        else:
            pin1_color = 'black'
        if tmnls_vol[1] / max_vol > 0.5:
            pin2_color = 'red'
        else:
            pin2_color = 'black'
        if pin1_color == 'red' or pin2_color == 'red':
            wave_color = 'red'
        else:
            wave_color = 'black'
    # square
    square_x = length / 2
    square_y = int(length/wave_num)
    square_x, square_y = coord_mirr_rota(orig_crd=(square_x, square_y), cnt_crd=(0, 0), angle=angle)

    # draw the wave line
    wave_len = int(length/wave_num)
    for i in range(wave_num):
        x0 = cnt_crd[0] - int(length / 2) + i * wave_len
        y0 = cnt_crd[1] - wave_len / 2
        x1 = x0 + wave_len
        y1 = cnt_crd[1] + wave_len / 2
        x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
        x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
        canvas.create_arc(x0, y0, x1, y1, start=angle, extent=180, outline=wave_color, tags=id, width=lwidth,
                          style=tk.ARC)

    # draw 2 pins
    tmnls_crd = draw_2_pins(tags=id, cnt_crd=cnt_crd, angle=angle, canvas=canvas, pin_len=pin_len,
                            pin1_color=pin1_color, pin2_color=pin2_color, lwidth=lwidth, distance=length)

    # return
    return {'square': (abs(square_x * 2), abs(square_y * 2)), 'tmnls_crd': tmnls_crd}


def draw_voltage_dc(id='voltage_dc-1',
                    cnt_crd=None,
                    angle=0,
                    canvas=None,
                    slct=False,
                    tmnls_vol=None,
                    max_vol=1.0):
    """
    func: draw the direct voltage source
    :param id: source id
    :param cnt_crd: center coordinate, (100, 100)
    :param angle: angle, e.g., 0, 90, 180, 270, etc,..
    :param canvas: tkinter Canvas
    :param slct: select status, True or False
    :param tmnls_vol: terminals' voltage, tuple or list, e.g., (10.0, 0.0)
    :param max_vol: the maximum voltage in the circuit, V, float, e.g., 10.0
    :return: {'square': (square_x, square_y), 'tmnls_crd': ((x1, y1), (x2, y2))}
    """
    if tmnls_vol is None:
        tmnls_vol = (0.0, 0.0)
    if cnt_crd is None:
        cnt_crd = (400, 400)

    # radius
    radius = 20
    # pin length
    pin_len = 20
    # line width and color
    if slct:
        lwidth = 4
        pin1_color = 'blue'
        pin2_color = 'blue'
        circle_color = 'blue'
    else:
        lwidth = 1.5
        if tmnls_vol[0] / max_vol > 0.5:
            pin1_color = 'red'
        else:
            pin1_color = 'black'
        if tmnls_vol[1] / max_vol > 0.5:
            pin2_color = 'red'
        else:
            pin2_color = 'black'
        if pin1_color == 'red' or pin2_color == 'red':
            circle_color = 'red'
        else:
            circle_color = 'black'
    # square
    square_x = radius * 2
    square_y = radius * 2

    # draw the circle
    x0 = cnt_crd[0] - radius
    y0 = cnt_crd[1] - radius
    x1 = cnt_crd[0] + radius
    y1 = cnt_crd[1] + radius
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_oval(x0, y0, x1, y1, outline=circle_color, width=lwidth, tags=id)

    # draw the positive-negative symbol
    x0 = cnt_crd[0] - radius / 2
    y0 = cnt_crd[1] - radius / 4
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    canvas.create_text(x0, y0, text='+', tags=id, fill=circle_color)
    x0 = cnt_crd[0] + radius / 2
    y0 = cnt_crd[1] - radius / 4
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    canvas.create_text(x0, y0, text='-', tags=id, fill=circle_color)

    # draw the line in the circle
    x0 = cnt_crd[0] - radius
    y0 = cnt_crd[1]
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1 = cnt_crd[0] + radius
    y1 = cnt_crd[1]
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, fill=circle_color, width=lwidth, tags=id)

    # draw 2 pins
    tmnls_crd = draw_2_pins(tags=id, cnt_crd=cnt_crd, angle=angle, canvas=canvas, pin_len=pin_len,
                            pin1_color=pin1_color, pin2_color=pin2_color, lwidth=lwidth, distance=2 * radius)

    # return
    return {'square': (abs(square_x), abs(square_y)), 'tmnls_crd': tmnls_crd}


def draw_voltage_ac(id='voltage_ac-1',
                    cnt_crd=None,
                    angle=0,
                    canvas=None,
                    slct=False,
                    tmnls_vol=None,
                    max_vol=1.0):
    """
    func: draw alternative current voltage source
    :param id: component id, e.g., 'voltage_ac-1'
    :param cnt_crd: center coordinate, e.g., (x, y)
    :param angle: angle, e.g., 0, 90, 180, 270, etc,..
    :param canvas: tkinter Canvas
    :param slct: select status, True or False
    :param tmnls_vol: terminal's voltage, unit is V, tuple, e.g., (10.0, 0.0)
    :param max_vol: maximum voltage in the circuit
    :return: {'square': square_x, square_y, 'tmnls_crd': ((x1, y1), (x2, y2))}
    """
    if tmnls_vol is None:
        tmnls_vol = (0.0, 0.0)
    if cnt_crd is None:
        cnt_crd = (400, 400)

    # radius of the circle
    radius = 20
    # pin length
    pin_len = 20
    # line width and color
    if slct:
        lwidth = 4
        pin1_color = 'blue'
        pin2_color = 'blue'
        circle_color = 'blue'
    else:
        lwidth = 1.5
        if tmnls_vol[0] / max_vol > 0.5:
            pin1_color = 'red'
        else:
            pin1_color = 'black'
        if tmnls_vol[1] / max_vol > 0.5:
            pin2_color = 'red'
        else:
            pin2_color = 'black'
        if pin1_color == 'red' or pin2_color == 'red':
            circle_color = 'red'
        else:
            circle_color = 'black'
    # square
    square_x = radius * 2
    square_y = radius * 2

    # draw the circle
    x0 = cnt_crd[0] - radius
    y0 = cnt_crd[1] - radius
    x1 = cnt_crd[0] + radius
    y1 = cnt_crd[1] + radius
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_oval(x0, y0, x1, y1, outline=circle_color, width=lwidth, tags=id)

    # draw sine symbol
    x = cnt_crd[0]
    y = cnt_crd[1] - 3 * radius / 2
    x, y = coord_mirr_rota(orig_crd=(x, y), cnt_crd=cnt_crd, angle=angle)
    draw_sine_symbol(tags=id, cnt_crd=(x, y), angle=0, canvas=canvas, lwidth=lwidth, lcolor=circle_color,
                     radius=radius)

    # draw the line in the circle
    x0 = cnt_crd[0] - radius
    y0 = cnt_crd[1]
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1 = cnt_crd[0] + radius
    y1 = cnt_crd[1]
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, fill=circle_color, width=lwidth, tags=id)

    # draw 2 pins
    tmnls_crd = draw_2_pins(tags=id, cnt_crd=cnt_crd, angle=angle, canvas=canvas, pin_len=pin_len,
                            pin1_color=pin1_color, pin2_color=pin2_color, lwidth=lwidth, distance=2 * radius)

    # return
    return {'square': (abs(square_x), abs(square_y)), 'tmnls_crd': tmnls_crd}


def draw_current_dc(id='current_dc-1',
                    cnt_crd=None,
                    angle=0,
                    canvas=None,
                    slct=False,
                    tmnls_vol=None,
                    max_vol=1.0):
    """
    func: draw the direct current source
    :param id: direct current source id
    :param cnt_crd: center coordinate, (100, 100)
    :param angle: angle, e.g., 0, 90, 180, 270, etc,..
    :param canvas: tkinter Canvas
    :param slct: select status, True or False
    :param tmnls_vol: terminals' voltage, tuple or list, e.g., (10.0, 0.0)
    :param max_vol: the maximum voltage in the circuit, V, float, e.g., 10.0
    :return: {'square': (square_x, square_y), 'tmnls_crd': ((x1, y1), (x2, y2))}
    """
    if tmnls_vol is None:
        tmnls_vol = (0.0, 0.0)
    if cnt_crd is None:
        cnt_crd = (400, 400)

    # radius
    radius = 20
    # pin length
    pin_len = 20
    # line width and color
    if slct:
        lwidth = 4
        pin1_color = 'blue'
        pin2_color = 'blue'
        circle_color = 'blue'
    else:
        lwidth = 1.5
        if tmnls_vol[0] / max_vol > 0.5:
            pin1_color = 'red'
        else:
            pin1_color = 'black'
        if tmnls_vol[1] / max_vol > 0.5:
            pin2_color = 'red'
        else:
            pin2_color = 'black'
        if pin1_color == 'red' or pin2_color == 'red':
            circle_color = 'red'
        else:
            circle_color = 'black'
    # square
    square_x = radius * 2
    square_y = radius * 2

    # draw the circle
    x0 = cnt_crd[0] - radius
    y0 = cnt_crd[1] - radius
    x1 = cnt_crd[0] + radius
    y1 = cnt_crd[1] + radius
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_oval(x0, y0, x1, y1, outline=circle_color, width=lwidth, tags=id)

    # draw the positive-negative symbol
    x0 = cnt_crd[0]
    y0 = cnt_crd[1] - 3 * radius / 2
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    canvas.create_text(x0, y0, text='+', tags=id, fill=circle_color, font=12)
    x0 = cnt_crd[0]
    y0 = cnt_crd[1] - 2 * radius
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    canvas.create_text(x0, y0, text='-', tags=id, fill=circle_color, font=12)

    # draw the line in the circle
    x0 = cnt_crd[0]
    y0 = cnt_crd[1] - radius
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1 = cnt_crd[0]
    y1 = cnt_crd[1] + radius
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, fill=circle_color, width=lwidth, tags=id)

    # draw the arrow
    x0 = cnt_crd[0] + radius + 5
    y0 = cnt_crd[1]
    x1 = cnt_crd[0] + radius + 15
    y1 = cnt_crd[1]
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    arrw_len = 10
    arrw_wid = 4
    canvas.create_line(x0, y0, x1, y1, fill=circle_color, width=lwidth, tags=id,
                       arrow=tk.LAST, arrowshape=(arrw_len, sqrt(arrw_wid ** 2 + arrw_len ** 2), arrw_wid))

    # draw 2 pins
    tmnls_crd = draw_2_pins(tags=id, cnt_crd=cnt_crd, angle=angle, canvas=canvas, pin_len=pin_len,
                            pin1_color=pin1_color, pin2_color=pin2_color, lwidth=lwidth, distance=2 * radius)

    # return
    return {'square': (abs(square_x), abs(square_y)), 'tmnls_crd': tmnls_crd}


def draw_current_ac(id='current_ac-1',
                    cnt_crd=None,
                    angle=0,
                    canvas=None,
                    slct=False,
                    tmnls_vol=None,
                    max_vol=1.0):
    """
    func: draw alternative current source
    :param id: component id, e.g., 'voltage_ac-1'
    :param cnt_crd: center coordinate, e.g., (x, y)
    :param angle: angle, e.g., 0, 90, 180, 270, etc,..
    :param canvas: tkinter Canvas
    :param slct: select status, True or False
    :param tmnls_vol: terminal's voltage, unit is V, tuple, e.g., (10.0, 0.0)
    :param max_vol: maximum voltage in the circuit
    :return: {'square': square_x, square_y, 'tmnls_crd': ((x1, y1), (x2, y2))}
    """
    if tmnls_vol is None:
        tmnls_vol = (0.0, 0.0)
    if cnt_crd is None:
        cnt_crd = (400, 400)

    # radius of the circle
    radius = 20
    # pin length
    pin_len = 20
    # line width and color
    if slct:
        lwidth = 4
        pin1_color = 'blue'
        pin2_color = 'blue'
        circle_color = 'blue'
    else:
        lwidth = 1.5
        if tmnls_vol[0] / max_vol > 0.5:
            pin1_color = 'red'
        else:
            pin1_color = 'black'
        if tmnls_vol[1] / max_vol > 0.5:
            pin2_color = 'red'
        else:
            pin2_color = 'black'
        if pin1_color == 'red' or pin2_color == 'red':
            circle_color = 'red'
        else:
            circle_color = 'black'
    # square
    square_x = radius * 2
    square_y = radius * 2

    # draw the circle
    x0 = cnt_crd[0] - radius
    y0 = cnt_crd[1] - radius
    x1 = cnt_crd[0] + radius
    y1 = cnt_crd[1] + radius
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_oval(x0, y0, x1, y1, outline=circle_color, width=lwidth, tags=id)

    # draw sine symbol
    x = cnt_crd[0]
    y = cnt_crd[1] - 3 * radius / 2
    x, y = coord_mirr_rota(orig_crd=(x, y), cnt_crd=cnt_crd, angle=angle)
    draw_sine_symbol(tags=id, cnt_crd=(x, y), angle=0, canvas=canvas, lwidth=lwidth, lcolor=circle_color,
                     radius=radius)

    # draw the line in the circle
    x0 = cnt_crd[0]
    y0 = cnt_crd[1] - radius
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1 = cnt_crd[0]
    y1 = cnt_crd[1] + radius
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, fill=circle_color, width=lwidth, tags=id)

    # draw the arrow
    x0 = cnt_crd[0] + radius + 5
    y0 = cnt_crd[1]
    x1 = cnt_crd[0] + radius + 15
    y1 = cnt_crd[1]
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    arrw_len = 10
    arrw_wid = 4
    canvas.create_line(x0, y0, x1, y1, fill=circle_color, width=lwidth, tags=id,
                       arrow=tk.LAST, arrowshape=(arrw_len, sqrt(arrw_wid ** 2 + arrw_len ** 2), arrw_wid))

    # draw 2 pins
    tmnls_crd = draw_2_pins(tags=id, cnt_crd=cnt_crd, angle=angle, canvas=canvas, pin_len=pin_len,
                            pin1_color=pin1_color, pin2_color=pin2_color, lwidth=lwidth, distance=2 * radius)

    # return
    return {'square': (abs(square_x), abs(square_y)), 'tmnls_crd': tmnls_crd}


def draw_switch(id='S?',
                cnt_crd=None,
                angle=0,
                canvas=None,
                swst='open',
                slct=False,
                tmnls_vol=None,
                max_vol=None):
    """
    func: draw the switch
    :param id: switch id, 'switch-1'
    :param cnt_crd: center coordinate, tuple, (x, y)
    :param angle: angle, e.g., 0, 90, 180, 270, etc,..
    :param canvas: tkinter Canvas
    :param swst: switch status, 'open' or 'close'
    :param slct: select status, True or False
    :param tmnls_vol: terminal voltage, tuple, e.g., (0.0, 0.0)
    :param max_vol: maximum voltage, V, float, e.g., 1.0
    :return: {'square': (square_x, square_y), 'tmnls_crd': ((x1, y1), (x2, y2))}
    """
    if tmnls_vol is None:
        tmnls_vol = (0.0, 0.0)
    if cnt_crd is None:
        cnt_crd = (400, 400)

    # length of switch
    length = 30
    width = 16
    # length of switch's arm
    arm_len = length * 1.1
    # pin length
    pin_len = 15
    if float(tmnls_vol[0].replace('V', '')) / float(max_vol.replace('V', '')) > 0.5:
        pin1_color = 'red'
    else:
        pin1_color = 'black'
    if float(tmnls_vol[1].replace('V', '')) / float(max_vol.replace('V', '')) > 0.5:
        pin2_color = 'red'
    else:
        pin2_color = 'black'
    if pin1_color != pin2_color and swst == 'close':
        print('Wrong Status：voltage of 2 terminals is not the same while switch is closed!')
    if swst == 'open':
        ang = 25
    else:
        ang = 10
    if slct:
        lwidth = 4
        pin1_color = 'blue'
        pin2_color = 'blue'
    else:
        lwidth = 2

    # draw the middle 2 lines
    x0 = cnt_crd[0] - length / 2
    y0 = cnt_crd[1] - width / 2
    x1 = cnt_crd[0] - length / 2
    y1 = cnt_crd[1] + width / 2
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, fill=pin1_color, width=lwidth, tags=id)

    x0 = cnt_crd[0] + length / 2
    y0 = cnt_crd[1]
    x1 = x0 - length * cos_deg(ang)
    y1 = y0 - length * sin_deg(ang)
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, fill=pin2_color, width=lwidth, tags=id)

    # draw 2 pins
    tmnls_crd = draw_2_pins(tags=id, cnt_crd=cnt_crd, angle=angle, canvas=canvas, pin_len=pin_len,
                            pin1_color=pin1_color, pin2_color=pin2_color, lwidth=lwidth, distance=length)

    # square
    square_x = length/2
    square_y = width/2
    square_x, square_y = coord_mirr_rota(orig_crd=(square_x, square_y), cnt_crd=(0, 0), angle=angle)

    # return
    return {'square': (abs(square_x * 2), abs(square_y * 2)), 'tmnls_crd': tmnls_crd}


def draw_ground(id='ground-?',
                cnt_crd=None,
                angle=0,
                canvas=None,
                slct=False):
    """
    func: draw the ground
    :param id: ground id
    :param cnt_crd: center coordinate, (x, y)
    :param angle: angel, e.g., 0, 90, 180, 270, etc,..
    :param canvas: tkinter Canvas
    :param slct: select status, True or False
    :return: {'square': (square_x, square_y), 'tmnls_crd': ((x1, y1),)}
    """
    if cnt_crd is None:
        cnt_crd = (400, 400)

    # length of the longest line
    length = 30
    # interval between 3 lines
    intvl = 8
    if slct:
        lwidth = 4
        pin_color = 'blue'
    else:
        lwidth = 2
        pin_color = 'black'

    # draw 3 lines
    x0 = cnt_crd[0]
    y0 = cnt_crd[1] - length / 2
    x1 = cnt_crd[0]
    y1 = cnt_crd[1] + length / 2
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, fill=pin_color, width=lwidth, tags=id)

    x0 = cnt_crd[0] + intvl
    y0 = cnt_crd[1] - length / 4
    x1 = cnt_crd[0] + intvl
    y1 = cnt_crd[1] + length / 4
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, fill=pin_color, width=lwidth, tags=id)

    x0 = cnt_crd[0] + intvl * 2
    y0 = cnt_crd[1] - length / 8
    x1 = cnt_crd[0] + intvl * 2
    y1 = cnt_crd[1] + length / 8
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, fill=pin_color, width=lwidth, tags=id)

    # draw pin
    tmnl_crd = draw_1_pin(tags=id, cnt_crd=cnt_crd, angle=angle, canvas=canvas, pin_len=20, pin_color=pin_color,
                          lwidth=lwidth)

    # square
    square_x = length
    square_y = intvl * 2
    square_x, square_y = coord_mirr_rota(orig_crd=(square_x, square_y), cnt_crd=(0, 0), angle=angle)

    # return
    return {'square': (abs(square_x), abs(square_y)), 'tmnls_crd': tmnl_crd}


def draw_diode(id='Us?',
               cnt_crd=None,
               angle=0,
               canvas=None,
               slct=False,
               tmnls_vol=None,
               max_vol=1.0,
               fill=False):
    """
    func: draw diode
    :param id:
    :param cnt_crd:
    :param angle:
    :param canvas:
    :param slct:
    :param tmnls_vol:
    :param max_vol:
    :param fill: if fill the inside of triangle, True or False
    :return:
    """
    if tmnls_vol is None:
        tmnls_vol = (0.0, 0.0)
    if cnt_crd is None:
        cnt_crd = (400, 400)

    # length and width of the middle part of diode
    length = 20
    width = 20
    # pin_len
    pin_len = 30
    # line width and color
    if slct:
        lwidth = 4
        pin1_color = 'blue'
        pin2_color = 'blue'
        tri_line_color = 'blue'
        if fill:
            tri_fill_color = 'blue'
        else:
            tri_fill_color = 'white'
    else:
        lwidth = 2
        if float(tmnls_vol[0]) / float(max_vol) > 0.5:
            pin1_color = 'red'
        else:
            pin1_color = 'black'
        if float(tmnls_vol[1]) / float(max_vol) > 0.5:
            pin2_color = 'red'
        else:
            pin2_color = 'black'
        if pin1_color == 'red' or pin2_color == 'red':
            tri_line_color = 'red'
            if fill:
                tri_fill_color = 'red'
            else:
                tri_fill_color = 'white'
        else:
            tri_line_color = 'black'
            if fill:
                tri_fill_color = 'black'
            else:
                tri_fill_color = 'white'
    # square
    square_x = length / 2
    square_y = width / 2
    square_x, square_y = coord_mirr_rota(orig_crd=(square_x, square_y), cnt_crd=(0, 0), angle=angle)

    # draw the triangle
    x0 = cnt_crd[0] + (length / 2)
    y0 = cnt_crd[1]
    x1 = cnt_crd[0] - (length / 2)
    y1 = cnt_crd[1] - (width / 2)
    x2 = cnt_crd[0] - (length / 2)
    y2 = cnt_crd[1] + (width / 2)
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    x2, y2 = coord_mirr_rota(orig_crd=(x2, y2), cnt_crd=cnt_crd, angle=angle)
    canvas.create_polygon(x0, y0, x1, y1, x2, y2, fill=tri_fill_color, outline=tri_line_color, tags=id, width=lwidth)

    # line beside the triangle
    x0 = cnt_crd[0] + (length / 2)
    y0 = cnt_crd[1] - (width / 2)
    x1 = cnt_crd[0] + (length / 2)
    y1 = cnt_crd[1] + (width / 2)
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, fill=tri_line_color, tags=id, width=lwidth)

    # draw 2 pins
    tmnls_crd = draw_2_pins(tags=id, cnt_crd=cnt_crd, angle=angle, canvas=canvas, pin_len=pin_len,
                            pin1_color=pin1_color, pin2_color=pin2_color, lwidth=lwidth, distance=length)

    # return
    return {'square': (abs(square_x * 2), abs(square_y * 2)), 'tmnls_crd': tmnls_crd}


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1000x800')
    frm = tk.Frame(root, width=1400, height=800)
    frm.grid(row=0, column=0)

    bcanv = tk.Canvas(frm, width=1000, height=800)
    bcanv.grid(row=0, column=0)
    draw_pn(id='D-1',
            cnt_crd=None,
            angle=0,
            distance=20,
            canvas=bcanv,
            slct=False)

    root.mainloop()
