# coding=utf-8
"""
This module defines some functions used as tools, e.g., sine function based on degree, coordinate transform,
transformer's connection recognition, etc..
"""
from math import *
import os
import pandas as pd


def cos_deg(angle):
    """
    func: cosine of angle with unit of degree
    :param angle: angle, unit is degree
    :return: cosine
    """
    if angle is not None:
        return cos(radians(angle))


def sin_deg(angle):
    """
    func： sine of angle with unit of degree
    :param angle: angle, unit is degree
    :return: sine
    """
    if angle is not None:
        return sin(radians(angle))


def tan_deg(angle):
    """
    func: tangent of angle with unit of degree
    :param angle: angle, unit is degree
    :return: tangent
    """
    if angle is not None:
        return tan(radians(angle))


def coord_mirr_rota(orig_crd=None,
                    cnt_crd=None,
                    mirr=None,
                    angle=0):
    """
    func: In a rectangular coordinate(original point is the left and upper vertex, x+ direction is orientation of right,
    y+ direction is orientation of down), when a point(orig_crd) makes a mirror transform or/and clockwise rotation,
    its coordinate's value will change.
    :param orig_crd: point's original coordinate
    :param cnt_crd: center coordinate around which the point rotate
    :param mirr: if there is a mirror transform
    None: no mirror,
    'x': mirror via x axis
    'y': mirror via x axis
    'xy': mirror via x axis and y axis
    :param angle: angle of clockwise rotation, 0°, 90°, 180°, 270°
    :return: new coordinate after transform, (x, y)
    """
    # if orig_crd equals to cnt_crd
    if orig_crd[0] == cnt_crd[0] and orig_crd[1] == cnt_crd[1]:
        new_coord = orig_crd
    # if orig_crd doesn't equal to cnt_crd
    else:
        # get the distance from point to center
        x_dstn = orig_crd[0] - cnt_crd[0]
        y_dstn = orig_crd[1] - cnt_crd[1]
        # mirror transform
        if mirr == 'x':
            y_dstn = -y_dstn
        elif mirr == 'y':
            x_dstn = -x_dstn
        elif mirr == 'xy' or mirr == 'yx':
            y_dstn = -y_dstn
            x_dstn = -x_dstn
        # clockwise rotation
        new_coord = (cnt_crd[0] + round(x_dstn * cos_deg(angle) - y_dstn * sin_deg(angle)),
                     cnt_crd[1] + round(y_dstn * cos_deg(angle) + x_dstn * sin_deg(angle)))

    return new_coord


def winding_info(conn_set='YNyn0d11'):
    """
    method: get the string of connection set and transform it to dict variable
    :param conn_set: connection set
    :return: dict({'winding_num': 3, 'winding1': 'y', 'winding1neutral': True, 'winding2': 'y', 'winding2neural': True,
     'winding3': 'd', 'winding1_direction': 0, 'winding2direction': 0, 'winding3dirction': 11 })
    """
    wind_info = {}
    # winding number
    num = conn_set.count('Y') + conn_set.count('y') + conn_set.count('d')
    wind_info['winding_num'] = num

    # separate the string of connection set to 3 parts, e.g., list(['YN00', 'yn00', 'd11'])
    conn_set_lst = []
    wind_i = 0
    if conn_set[0] == 'Y' or conn_set[0] == 'y' or conn_set[0] == 'd' or conn_set[0] == 'D':
        conn_set_lst.append(conn_set[0])
    for i in range(1, len(conn_set)):
        if conn_set[i] == 'Y' or conn_set[i] == 'y' or conn_set[i] == 'd' or conn_set[i] == 'D':
            wind_i += 1
            conn_set_lst.append(conn_set[i])
        else:
            conn_set_lst[wind_i] += conn_set[i]

    # handle each winding
    for i in range(num):
        if 'Y' in conn_set_lst[i] or 'y' in conn_set_lst[i]:
            wind_info['winding' + str(i+1)] = 'y'
            if 'N' in conn_set_lst[i] or 'n' in conn_set_lst[i]:
                wind_info['winding' + str(i + 1) + 'neutral'] = True
                if len(conn_set_lst[i]) == 2:
                    wind_info['winding' + str(i + 1) + 'direction'] = 0
                elif len(conn_set_lst[i]) == 3:
                    wind_info['winding' + str(i + 1) + 'direction'] = int(conn_set_lst[i][2])
                elif len(conn_set_lst[i]) == 4:
                    wind_info['winding' + str(i + 1) + 'direction'] = int(conn_set_lst[i][2:4])
            else:
                wind_info['winding' + str(i + 1) + 'neutral'] = False
                if len(conn_set_lst[i]) == 1:
                    wind_info['winding' + str(i + 1) + 'direction'] = 0
                elif len(conn_set_lst[i]) == 2:
                    wind_info['winding' + str(i + 1) + 'direction'] = int(conn_set_lst[i][1])
                elif len(conn_set_lst[i]) == 3:
                    wind_info['winding' + str(i + 1) + 'direction'] = int(conn_set_lst[i][1:3])
        elif 'D' in conn_set_lst[i] or 'd' in conn_set_lst[i]:
            wind_info['winding' + str(i + 1)] = 'd'
            wind_info['winding' + str(i + 1) + 'neutral'] = False
            if len(conn_set_lst[i]) == 1:
                wind_info['winding' + str(i + 1) + 'direction'] = 0
            elif len(conn_set_lst[i]) == 2:
                wind_info['winding' + str(i + 1) + 'direction'] = int(conn_set_lst[i][1])
            elif len(conn_set_lst[i]) == 3:
                wind_info['winding' + str(i + 1) + 'direction'] = int(conn_set_lst[i][1:3])

    return wind_info


def point_capture(crd=None, x_intvl=20, y_intvl=20):
    """
    func: capture the point whose coordinate is crd in a rectangle area of (x_intvl, y_intvl)
    :param crd: coordinate of the point
    :param x_intvl: interval in x direction
    :param y_intvl: interval in y direction
    :return: captured: modified coordinate，not captured: False
    """
    if crd is not None:
        x = crd[0]
        y = crd[1]
        if abs(x - x_intvl * round(float(x) / x_intvl)) < 10 and abs(y - y_intvl * round(float(y) / y_intvl)) < 10:
            x = round(float(x) / x_intvl) * x_intvl
            y = round(float(y) / y_intvl) * y_intvl
            return x, y
        else:
            return False
    else:
        return False


def get_multi_value(value=None):
    """
    func: get the multiple factor and value, e.g., give 1000, get ('k', 1)
    :return: multiple factor and value, e.g., ('k', 1)
    """
    if value is None:
        value = ''
        multi = ''
    else:
        if value >= 1E12:
            value /= 1E12
            multi = 'T'
        elif value >= 1E9:
            value /= 1E9
            multi = 'G'
        elif value >= 1E6:
            value /= 1E6
            multi = 'M'
        elif value >= 1E3:
            value /= 1E3
            multi = 'k'
        elif value <= 1E-12:
            value /= 1E-12
            multi = 'p'
        elif value <= 1E-9:
            value /= 1E-9
            multi = 'n'
        elif value <= 1E-6:
            value /= 1E-6
            multi = 'u'
        elif value <= 1E-3:
            value /= 1E-3
            multi = 'm'
        else:
            multi = ''
    return multi, value


def get_unit(comp_nm):
    """
    func: get the unit of the component from its name, e.g., give 'R', get 'Ω'
    :return: unit of the component, e.g., 'Ω', 'H'
    """
    unit = ''
    if comp_nm == 'R':
        unit = 'Ω'
    elif comp_nm == 'C':
        unit = 'F'
    elif comp_nm == 'L':
        unit = 'H'
    elif comp_nm == 'Uac' or comp_nm == 'Udc':
        unit = 'V'
    elif comp_nm == 'Iac' or comp_nm == 'Idc':
        unit = 'A'
    return unit


if __name__ == "__main__":
    print(get_multi_value(1580))
