"""
This module is used for calculation of circuit
"""
from math import *
import numpy as np
import copy as copy
import tkinter as tk
import tkinter.ttk as ttk
import time
import tkinter.messagebox as messagebox
import Elecpy.Default as default
import Elecpy.Graph as graph
import Elecpy.Backup as backup
import Elecpy.GUIElements as gui_elements


class DynamicCirCal:
    """
    class: Dynamic Circuit Calculation
    """
    def __init__(self):
        """
        method:
        """
        # netlist
        self.netlist = None
        # step time
        self.h = None
        # number of components
        self.num_comps = None
        # number of nodes
        self.num_nodes = None
        # number of capacitor and inductor
        self.num_lc = None
        # concatenate matrix A E F H M N Q
        self.mat_aefhmnq = None
        # init value of matrix b
        self.mat_b = None
        # time iteratior, [0, 1, 2,..]
        self.time_iter = []
        # time consequence, [0, 1*self.h, 2*self.h,..]
        self.time = []
        # voltage of nodes, list of time
        self.u_nodes = None
        # voltage of components, list of time
        self.u_comps = None
        # current of components, list of time
        self.i_comps = None
        # diff of voltage of capacitor or current of inductor
        self.diff = None

    def set_params(self,
                   netlist,
                   h=1e-6):
        """
        method: initial
        :param netlist:
        :param h: interval, second, e.g., 1e-6(1us), 1e-4(100us), etc,..
        :return: None
        """
        # netlist
        self.netlist = netlist
        # time step
        self.h = h
        # number of components
        self.num_comps = self.get_num_comps()
        # number of nodes
        self.num_nodes = self.get_num_nodes()
        # number of capacitor and inductor
        self.num_lc = self.get_num_lc()
        # concatenate matrix A E F H M N Q
        self.mat_aefhmnq = self.get_init_mat_aefhmnq()
        # init value of matrix b
        self.mat_b = self.get_init_mat_b()
        # voltage of nodes, list of time
        self.u_nodes = self.init_voltage_nodes()
        # voltage of components, list of time
        self.u_comps = self.init_voltage_comps()
        # current of components, list of time
        self.i_comps = self.init_current_comps()
        # diff of voltage of capacitor or current of inductor
        self.diff = self.init_diff()

    def get_num_comps(self):
        """
        method: get number of components
        :return: int,
        """
        return len(self.netlist)

    def get_num_nodes(self):
        """
        method: get number of nodes
        :return: int
        """
        # num of nodes and comps
        num_nodes = 0
        for comp_data in self.netlist:
            if comp_data['node1'] > num_nodes:
                num_nodes = comp_data['node1']
            if comp_data['node2'] > num_nodes:
                num_nodes = comp_data['node2']
        return num_nodes

    def get_num_lc(self):
        """
        method: get number of inductor(L) and capacitor(C)
        :return: int
        """
        num_lc = 0
        for comp_data in self.netlist:
            comp_nm = comp_data['designator'].split('-')[0]
            if comp_nm == 'C':
                num_lc += 1
            if comp_nm == 'L':
                num_lc += 1
        return num_lc

    def init_voltage_nodes(self):
        """
        method:
        :return:
        """
        u_nodes = {}
        for k in range(self.num_nodes):
            u_nodes['node' + str(k + 1)] = []
        return u_nodes

    def init_voltage_comps(self):
        """
        method:
        :return:
        """
        u_comps = {}
        for comp_data in self.netlist:
            u_comps[comp_data['designator']] = []
        return u_comps

    def init_current_comps(self):
        """
        method:
        :return:
        """
        i_comps = {}
        for comp_data in self.netlist:
            i_comps[comp_data['designator']] = []
        return i_comps

    def init_diff(self):
        """
        method:
        :return:
        """
        diff = []
        for i in range(self.num_lc):
            diff.append(0)
        return diff

    def get_mat_a(self):
        """
        method: matrix A
        :return:
        """
        # get matrix A
        mat_a = np.zeros([self.num_nodes, self.num_comps])
        # fill matrix A
        for k, comp_data in enumerate(self.netlist):
            j = comp_data['node1']
            if j > 0:
                mat_a[j - 1, k] = comp_data['cur_dir']
            j = comp_data['node2']
            if j > 0:
                mat_a[j - 1, k] = -comp_data['cur_dir']
        return mat_a

    def get_mat_e(self):
        """
        method: matrix E
        :return:
        """
        # get matrix E
        mat_e = np.identity(self.num_comps)
        # change value of E
        for k, comp_data in enumerate(self.netlist):
            if comp_data['vol_dir'] != comp_data['cur_dir']:
                mat_e[k, k] *= -1
        return mat_e

    def get_index_from_designator(self,
                                  designator=None):
        """
        method: get index of a component whose designator is given
        :param designator:
        :return:
        """
        for index, comp_data in enumerate(self.netlist):
            if comp_data['designator'] == designator:
                return index

    def get_mat_fh(self):
        """
        method: matrix F and matrix H
        :return:
        """
        # Zero matrix F and H
        f = np.zeros([self.num_comps, self.num_comps], float)
        h = np.zeros([self.num_comps, self.num_comps], float)
        # fill matrix F and H
        for k, comp_data in enumerate(self.netlist):
            comp_nm = comp_data['designator'].split('-')[0]
            vol_dir = comp_data['vol_dir']
            cur_dir = comp_data['cur_dir']
            if comp_nm == 'G':
                f[k, k] = comp_data['value'] * vol_dir
                h[k, k] = -cur_dir
            elif comp_nm == 'C':
                f[k, k] = vol_dir
                h[k, k] = 0
            elif comp_nm == 'R':
                f[k, k] = -vol_dir
                h[k, k] = comp_data['value'] * cur_dir
            elif comp_nm == 'L':
                f[k, k] = 0
                h[k, k] = cur_dir
            elif comp_nm == 'D':
                f[k, k] = -vol_dir
                h[k, k] = comp_data['Rr'] * cur_dir
            elif 'U' in comp_nm:
                f[k, k] = vol_dir
                h[k, k] = 0
            elif 'I' in comp_nm:
                f[k, k] = 0
                h[k, k] = cur_dir
            # voltage control voltage source
            elif comp_nm == 'VcVs':
                j = self.get_index_from_designator(designator=comp_data['control'])
                f[k, k] = 1
                f[k, j] = comp_data['factor'] * (-1) * vol_dir
                h[k, k] = 0
            # voltage control current source
            elif comp_nm == 'VcCs':
                j = self.get_index_from_designator(designator=comp_data['control'])
                f[k, k] = 0
                f[k, j] = comp_data['factor'] * (-1) * cur_dir
                h[k, k] = 1
            # current control voltage source
            elif comp_nm == 'CcVs':
                j = self.get_index_from_designator(designator=comp_data['control'])
                f[k, k] = 1
                h[k, j] = comp_data['factor'] * (-1) * vol_dir
                h[k, k] = 0
            # current control current source
            elif comp_nm == 'CcCs':
                j = self.get_index_from_designator(designator=comp_data['control'])
                f[k, k] = 0
                h[k, j] = comp_data['factor'] * (-1) * cur_dir
                h[k, k] = 1
            # primary side of transformer
            elif comp_nm == 'Tp':
                sn = comp_data['designator'].split('-')[1]
                j = self.get_index_from_designator(designator='Ts-' + sn)
                f[k, k] = 1
                f[k, j] = -comp_data['ratio'] * vol_dir
                h[k, k] = 0
            # second side of transformer
            elif comp_nm == 'Ts':
                sn = comp_data['designator'].split('-')[1]
                j = self.get_index_from_designator(designator='Tp-' + sn)
                f[k, k] = 0
                h[k, j] = comp_data['ratio'] * cur_dir
                h[k, k] = 1
        return f, h

    def get_mat_mn(self):
        """
        method: matrix M and matrix N
        :return:
        """
        # matrix M and Matrix N
        m = np.zeros([self.num_lc, self.num_comps], float)
        n = np.zeros([self.num_lc, self.num_comps], float)

        j = 0
        for k, comp_data in enumerate(self.netlist):
            comp_nm = comp_data['designator'].split('-')[0]
            vol_dir = comp_data['vol_dir']
            cur_dir = comp_data['cur_dir']
            if comp_nm == 'L':
                m[j, k] = -vol_dir
                n[j, k] = 0
                j += 1
            elif comp_nm == 'C':
                m[j, k] = 0
                n[j, k] = -cur_dir
                j += 1
        return m, n

    def get_mat_q(self):
        """
        method: matrix Q
        :return:
        """
        # matrix Q
        q = np.zeros([self.num_lc, self.num_lc], float)

        j = 0
        for comp_data in self.netlist:
            comp_nm = comp_data['designator'].split('-')[0]
            if comp_nm == 'L':
                q[j, j] = comp_data['value']
                j += 1
            elif comp_nm == 'C':
                q[j, j] = comp_data['value']
                j += 1
        return q

    def get_init_mat_aefhmnq(self):
        """
        method:
        :return:
        """
        # matrix zero
        zero_1 = np.zeros([self.num_nodes, self.num_nodes])
        zero_2 = np.zeros([self.num_nodes, self.num_comps])
        zero_3 = np.zeros([self.num_comps, self.num_comps])
        zero_4 = np.zeros([self.num_comps, self.num_nodes])
        zero_5 = np.zeros([self.num_nodes, self.num_lc])
        zero_6 = np.zeros([self.num_comps, self.num_lc])
        zero_7 = np.zeros([self.num_comps, self.num_lc])
        zero_8 = np.zeros([self.num_lc, self.num_nodes])

        # matrix
        mat_a = self.get_mat_a()
        one = self.get_mat_e()
        mat_f, mat_h = self.get_mat_fh()
        mat_m, mat_n = self.get_mat_mn()
        mat_q = self.get_mat_q()
        # concatenate
        mat_1 = np.concatenate([zero_1, zero_2, mat_a, zero_5], axis=1)
        mat_2 = np.concatenate([-mat_a.T, one, zero_3, zero_6], axis=1)
        mat_3 = np.concatenate([zero_4, mat_f, mat_h, zero_7], axis=1)
        mat_4 = np.concatenate([zero_8, mat_m, mat_n, mat_q], axis=1)
        mat_aefhmnq = np.concatenate([mat_1, mat_2, mat_3, mat_4], axis=0)

        return mat_aefhmnq

    def get_init_mat_b(self):
        """
        method: get initial matrix mat_b
        :return:
        """
        ui_s = np.zeros([self.num_comps, 1], float)
        diff = np.zeros([self.num_lc, 1], float)
        j = 0
        for k, comp_data in enumerate(self.netlist):
            comp_nm = comp_data['designator'].split('-')[0]
            vol_dir = comp_data['vol_dir']
            cur_dir = comp_data['cur_dir']
            if 'Uac' in comp_nm:
                ui_s[k] = comp_data['amp'] * sin(radians(comp_data['phase']))
            elif 'Iac' in comp_nm:
                ui_s[k] = comp_data['amp'] * sin(radians(comp_data['phase']))
            elif 'Udc' in comp_nm:
                ui_s[k] = comp_data['amp']
            elif 'Idc' in comp_nm:
                ui_s[k] = comp_data['amp']
            elif comp_nm == 'C':
                ui_s[k] = comp_data['Uc']
            elif comp_nm == 'L':
                ui_s[k] = comp_data['Il']

        # vector zero
        zero_5 = np.zeros([self.num_nodes, 1])
        zero_6 = np.zeros([self.num_comps, 1])
        # concatenate
        mat_b = np.concatenate([zero_5, zero_6, ui_s, diff], axis=0)

        return mat_b

    def update_mat_aefhmnq(self,
                           iter):
        """
        method: update matrix aefhmnq
        :param iter: iterator, 1, 2, ...
        :return:
        """
        for k, comp_data in enumerate(self.netlist):
            comp_nm = comp_data['designator'].split('-')[0]
            if 'D' in comp_nm:
                ud = self.u_comps[comp_data['designator']][iter - 1]
                if ud * comp_data['vol_dir'] < 0:
                    self.mat_aefhmnq[self.num_nodes + self.num_comps + k, self.num_nodes + k] = \
                        1 / comp_data['Rr'] * comp_data['vol_dir']
                    self.mat_aefhmnq[self.num_nodes + self.num_comps + k, self.num_nodes + self.num_comps + k] = \
                        -comp_data['cur_dir']
                elif 0 <= ud * comp_data['vol_dir'] < comp_data['Vf']:
                    self.mat_aefhmnq[self.num_nodes + self.num_comps + k, self.num_nodes + k] = -comp_data['vol_dir']
                    self.mat_aefhmnq[self.num_nodes + self.num_comps + k, self.num_nodes + self.num_comps + k] = \
                        comp_data['Rr'] * comp_data['cur_dir']
                elif ud * comp_data['vol_dir'] >= comp_data['Vf']:
                    self.mat_aefhmnq[self.num_nodes + self.num_comps + k, self.num_nodes + k] = -comp_data['vol_dir']
                    self.mat_aefhmnq[self.num_nodes + self.num_comps + k, self.num_nodes + self.num_comps + k] = \
                        comp_data['Rf'] * comp_data['cur_dir']

    def update_mat_b(self,
                     iter):
        """
        method: update matrix b
        :param iter: iterator, 1, 2, ...
        :return: None
        """
        # for index of L and C
        j = 0
        for k, comp_data in enumerate(self.netlist):
            comp_nm = comp_data['designator'].split('-')[0]
            if 'Uac' in comp_nm:
                self.mat_b[self.num_nodes + self.num_comps + k, 0] = \
                    comp_data['amp'] * sin(2 * pi * comp_data['freq'] * self.h * iter + radians(comp_data['phase']))
            elif 'Iac' in comp_nm:
                self.mat_b[self.num_nodes + self.num_comps + k, 0] = \
                    comp_data['amp'] * sin(2 * pi * comp_data['freq'] * self.h * iter + radians(comp_data['phase']))
            elif comp_nm == 'C' or comp_nm == 'L':
                self.mat_b[self.num_nodes + self.num_comps + k, 0] += self.diff[j] * self.h
                j += 1
            elif 'D' in comp_nm:
                ud = self.u_comps[comp_data['designator']][iter - 1]
                if ud * comp_data['vol_dir'] < 0:
                    self.mat_b[self.num_nodes + self.num_comps + k, 0] = comp_data['Ir']
                elif comp_data['Vf'] > ud * comp_data['vol_dir'] >= 0:
                    self.mat_b[self.num_nodes + self.num_comps + k, 0] = 0
                elif ud * comp_data['vol_dir'] >= comp_data['Vf']:
                    self.mat_b[self.num_nodes + self.num_comps + k, 0] = -comp_data['Vf']

    def assign_result(self,
                      x):
        """
        method: assign self.u_nodes self.u_comps self.i_comps
        :param x: result
        :return: None
        """
        for i, node in enumerate(self.u_nodes):
            self.u_nodes[node].append(x[i, 0])
        for i, comp in enumerate(self.u_comps):
            self.u_comps[comp].append(x[i + self.num_nodes, 0])
            self.i_comps[comp].append(x[i + self.num_nodes + self.num_comps, 0])

    def init_cal(self):
        """
        method: init calculation
        :return:
        """
        # calculate
        x = np.linalg.solve(self.mat_aefhmnq, self.mat_b)
        # data append
        self.assign_result(x)
        # time append
        self.time_iter.append(0)
        self.time.append(0)

        self.diff = x[:, -1][self.num_nodes + self.num_comps * 2:]

    def repeat_cal(self,
                   iter):
        """
        method:
        :param iter: time step, 1, 2, ...
        :return:
        """
        self.update_mat_b(iter=iter)
        self.update_mat_aefhmnq(iter=iter)
        x = np.linalg.solve(self.mat_aefhmnq, self.mat_b)
        self.assign_result(x)
        self.time_iter.append(iter)
        self.time.append(iter*self.h)

        self.diff = x[:, -1][self.num_nodes + self.num_comps * 2:]


class SinSteadyCirCal:
    """
    class: Sinusoidal Steady-State circuit calculation
    """
    def __init__(self):
        """
        method:
        """
        # netlist
        self.netlist = None
        # frequency of the circuit
        self.freq = None
        # number of components
        self.num_comps = None
        # number of nodes
        self.num_nodes = None
        # concatenate matrix A E F H
        self.mat_aefh = None
        # init value of matrix b
        self.mat_b = None
        # voltage of nodes, list of time
        self.u_nodes = None
        # voltage of components, list of time
        self.u_comps = None
        # current of components, list of time
        self.i_comps = None

    def set_params(self,
                   netlist):
        """
        method: initial
        :param netlist:
        :return:
        """
        # netlist
        self.netlist = netlist
        # frequency of the circuit
        self.freq = self.get_freq()
        if self.freq is False:
            raise TypeError('The frequency is not unique！')
        # number of components
        self.num_comps = self.get_num_comps()
        # number of nodes
        self.num_nodes = self.get_num_nodes()
        # concatenate matrix A E F H
        self.mat_aefh = self.get_mat_aefh()
        # init value of matrix b
        self.mat_b = self.get_mat_b()
        # voltage of nodes, list of time
        self.u_nodes = self.init_voltage_nodes()
        # voltage of components, list of time
        self.u_comps = self.init_voltage_comps()
        # current of components, list of time
        self.i_comps = self.init_current_comps()

    def get_num_comps(self):
        """
        method: get number of components
        :return:
        """
        return len(self.netlist)

    def get_num_nodes(self):
        """
        method: get number of nodes
        :return:
        """
        # num of nodes and comps
        num_nodes = 0
        for comp_data in self.netlist:
            if comp_data['node1'] > num_nodes:
                num_nodes = comp_data['node1']
            if comp_data['node2'] > num_nodes:
                num_nodes = comp_data['node2']
        return num_nodes

    def get_num_dc(self):
        """
        method: get number of Udc or Idc
        :return:
        """
        num_dc = 0
        for comp_data in self.netlist:
            comp_nm = comp_data['designator'].split('-')[0]
            if comp_nm == 'Udc':
                num_dc += 1
            if comp_nm == 'Idc':
                num_dc += 1
        return num_dc

    def get_freq(self):
        """
        method: get freq of the circuit
        :return: frequent of the circuit
        """
        freq = None
        for comp_data in self.netlist:
            comp_nm = comp_data['designator'].split('-')[0]
            if comp_nm == 'Uac' or comp_nm == 'Iac':
                if freq is None:
                    freq = comp_data['freq']
                elif freq != comp_data['freq']:
                    return False
        return freq

    def init_voltage_nodes(self):
        """
        method:
        :return:
        """
        u_nodes = {}
        for k in range(self.num_nodes):
            u_nodes['node' + str(k + 1)] = 0
        return u_nodes

    def init_voltage_comps(self):
        """
        method:
        :return:
        """
        u_comps = {}
        for comp_data in self.netlist:
            u_comps[comp_data['designator']] = 0
        return u_comps

    def init_current_comps(self):
        """
        method:
        :return:
        """
        i_comps = {}
        for comp_data in self.netlist:
            i_comps[comp_data['designator']] = 0
        return i_comps

    def get_mat_a(self):
        """
        method: matrix A
        :return:
        """
        # get matrix A
        mat_a = np.zeros([self.num_nodes, self.num_comps])
        # fill matrix A according to the netlist
        for k, comp_data in enumerate(self.netlist):
            j = comp_data['node1']
            if j > 0:
                mat_a[j - 1, k] = comp_data['cur_dir']
            j = comp_data['node2']
            if j > 0:
                mat_a[j - 1, k] = -comp_data['cur_dir']
        return mat_a

    def get_mat_e(self):
        """
        method: matrix E
        :return:
        """
        # get matrix E
        mat_e = np.identity(self.num_comps)
        # change value of E
        for k, comp_data in enumerate(self.netlist):
            if comp_data['vol_dir'] != comp_data['cur_dir']:
                mat_e[k, k] *= -1
        return mat_e

    def get_index_from_designator(self,
                                  designator=None):
        """
        method: get index of a component whose designator is given
        :param designator:
        :return:
        """
        for index, comp_data in enumerate(self.netlist):
            if comp_data['designator'] == designator:
                return index

    def get_mat_fh(self):
        """
        method: matrix F and matrix H
        :return:
        """
        # Zero matrix F and H
        f = np.zeros([self.num_comps, self.num_comps], complex)
        h = np.zeros([self.num_comps, self.num_comps], complex)
        # fill F and H
        for k, comp_data in enumerate(self.netlist):
            comp_nm = comp_data['designator'].split('-')[0]
            vol_dir = comp_data['vol_dir']
            cur_dir = comp_data['cur_dir']
            if comp_nm == 'G':
                f[k, k] = comp_data['value'] * vol_dir
                h[k, k] = -cur_dir
            elif comp_nm == 'C':
                f[k, k] = comp_data['value'] * self.freq * 2 * pi * 1j * vol_dir
                h[k, k] = -cur_dir
            elif comp_nm == 'R':
                f[k, k] = -vol_dir
                h[k, k] = comp_data['value'] * cur_dir
            elif comp_nm == 'L':
                f[k, k] = -vol_dir
                h[k, k] = comp_data['value'] * self.freq * 2 * pi * 1j * cur_dir
            elif 'U' in comp_nm:
                f[k, k] = vol_dir
                h[k, k] = 0
            elif 'I' in comp_nm:
                f[k, k] = 0
                h[k, k] = cur_dir
            # voltage control voltage source
            elif comp_nm == 'VcVs':
                j = self.get_index_from_designator(designator=comp_data['control'])
                f[k, k] = 1
                f[k, j] = comp_data['factor'] * (-1) * vol_dir
                h[k, k] = 0
            # voltage control current source
            elif comp_nm == 'VcCs':
                j = self.get_index_from_designator(designator=comp_data['control'])
                f[k, k] = 0
                f[k, j] = comp_data['factor'] * (-1) * cur_dir
                h[k, k] = 1
            # current control voltage source
            elif comp_nm == 'CcVs':
                j = self.get_index_from_designator(designator=comp_data['control'])
                f[k, k] = 1
                h[k, j] = comp_data['factor'] * (-1) * vol_dir
                h[k, k] = 0
            # current control current source
            elif comp_nm == 'CcCs':
                j = self.get_index_from_designator(designator=comp_data['control'])
                f[k, k] = 0
                h[k, j] = comp_data['factor'] * (-1) * cur_dir
                h[k, k] = 1
            # primary side of transformer
            elif comp_nm == 'Tp':
                sn = comp_data['designator'].split('-')[1]
                j = self.get_index_from_designator(designator='Ts-' + sn)
                f[k, k] = 1
                f[k, j] = -comp_data['ratio'] * vol_dir
                h[k, k] = 0
            # second side of transformer
            elif comp_nm == 'Ts':
                sn = comp_data['designator'].split('-')[1]
                j = self.get_index_from_designator(designator='Tp-' + sn)
                f[k, k] = 0
                h[k, j] = comp_data['ratio'] * cur_dir
                h[k, k] = 1
        return f, h

    def get_mat_aefh(self):
        """
        method:
        :return:
        """
        # matrix zero
        zero_1 = np.zeros([self.num_nodes, self.num_nodes], complex)
        zero_2 = np.zeros([self.num_nodes, self.num_comps], complex)
        zero_3 = np.zeros([self.num_comps, self.num_comps], complex)
        zero_4 = np.zeros([self.num_comps, self.num_nodes], complex)

        # matrix
        mat_a = self.get_mat_a()
        one = self.get_mat_e()
        mat_f, mat_h = self.get_mat_fh()
        # concatenate
        mat_1 = np.concatenate([zero_1, zero_2, mat_a], axis=1)
        mat_2 = np.concatenate([-mat_a.T, one, zero_3], axis=1)
        mat_3 = np.concatenate([zero_4, mat_f, mat_h], axis=1)
        mat_aefhmnq = np.concatenate([mat_1, mat_2, mat_3], axis=0)

        return mat_aefhmnq

    def get_mat_b(self):
        """
        method: get matrix mat_b
        :return:
        """
        ui_s = np.zeros([self.num_comps, 1], complex)
        j = 0
        for k, comp_data in enumerate(self.netlist):
            comp_nm = comp_data['designator'].split('-')[0]
            if 'Uac' in comp_nm:
                ui_s[k] = comp_data['amp'] * (cos(radians(comp_data['phase'])) + sin(radians(comp_data['phase'])) * 1j)
            elif 'Iac' in comp_nm:
                ui_s[k] = comp_data['amp'] * (cos(radians(comp_data['phase'])) + sin(radians(comp_data['phase'])) * 1j)

        # vector zero
        zero_5 = np.zeros([self.num_nodes, 1], complex)
        zero_6 = np.zeros([self.num_comps, 1], complex)
        # concatenate
        mat_b = np.concatenate([zero_5, zero_6, ui_s], axis=0)

        return mat_b

    def assign_result(self,
                      x):
        """
        method: assign self.u_nodes self.u_comps self.i_comps
        :param x: result
        :return: None
        """
        for i, node in enumerate(self.u_nodes):
            self.u_nodes[node] = x[i, 0]
        for i, comp in enumerate(self.u_comps):
            self.u_comps[comp] = x[i + self.num_nodes, 0]
            self.i_comps[comp] = x[i + self.num_nodes + self.num_comps, 0]

    def calculate(self):
        """
        method: calculate
        :return:
        """
        x = np.linalg.solve(self.mat_aefh, self.mat_b)
        self.assign_result(x)


class DCSteadyCirCal:
    """
    class: DC Steady-State circuit calculation
    """
    def __init__(self):
        """
        method:
        """
        # netlist
        self.netlist = None
        # number of components
        self.num_comps = None
        # number of nodes
        self.num_nodes = None
        # concatenate matrix A E F H
        self.mat_aefh = None
        # init value of matrix b
        self.mat_b = None
        # voltage of nodes, list of time
        self.u_nodes = None
        # voltage of components, list of time
        self.u_comps = None
        # current of components, list of time
        self.i_comps = None

    def set_params(self,
                   netlist):
        """
        method: initial
        :param netlist:
        :return:
        """
        # netlist
        self.netlist = netlist
        # number of components
        self.num_comps = self.get_num_comps()
        # number of nodes
        self.num_nodes = self.get_num_nodes()
        # concatenate matrix A E F H
        self.mat_aefh = self.get_mat_aefh()
        # init value of matrix b
        self.mat_b = self.get_mat_b()
        # voltage of nodes, list of time
        self.u_nodes = self.init_voltage_nodes()
        # voltage of components, list of time
        self.u_comps = self.init_voltage_comps()
        # current of components, list of time
        self.i_comps = self.init_current_comps()

    def get_num_comps(self):
        """
        method: get number of components
        :return:
        """
        return len(self.netlist)

    def get_num_nodes(self):
        """
        method: get number of nodes
        :return:
        """
        # num of nodes and comps
        num_nodes = 0
        for comp_data in self.netlist:
            if comp_data['node1'] > num_nodes:
                num_nodes = comp_data['node1']
            if comp_data['node2'] > num_nodes:
                num_nodes = comp_data['node2']
        return num_nodes

    def get_num_dc(self):
        """
        method: get number of Udc or Idc
        :return:
        """
        num_dc = 0
        for comp_data in self.netlist:
            comp_nm = comp_data['designator'].split('-')[0]
            if comp_nm == 'Udc':
                num_dc += 1
            if comp_nm == 'Idc':
                num_dc += 1
        return num_dc

    def init_voltage_nodes(self):
        """
        method:
        :return:
        """
        u_nodes = {}
        for k in range(self.num_nodes):
            u_nodes['node' + str(k + 1)] = 0
        return u_nodes

    def init_voltage_comps(self):
        """
        method:
        :return:
        """
        u_comps = {}
        for comp_data in self.netlist:
            u_comps[comp_data['designator']] = 0
        return u_comps

    def init_current_comps(self):
        """
        method:
        :return:
        """
        i_comps = {}
        for comp_data in self.netlist:
            i_comps[comp_data['designator']] = 0
        return i_comps

    def get_mat_a(self):
        """
        method: matrix A
        :return:
        """
        # get matrix A
        mat_a = np.zeros([self.num_nodes, self.num_comps])
        # fill matrix A according to the netlist
        for k, comp_data in enumerate(self.netlist):
            j = comp_data['node1']
            if j > 0:
                mat_a[j - 1, k] = comp_data['cur_dir']
            j = comp_data['node2']
            if j > 0:
                mat_a[j - 1, k] = -comp_data['cur_dir']
        return mat_a

    def get_mat_e(self):
        """
        method: matrix E
        :return:
        """
        # get matrix E
        mat_e = np.identity(self.num_comps)
        # change value of E
        for k, comp_data in enumerate(self.netlist):
            if comp_data['vol_dir'] != comp_data['cur_dir']:
                mat_e[k, k] *= -1
        return mat_e

    def get_index_from_designator(self,
                                  designator=None):
        """
        method: get index of a component whose designator is given
        :param designator:
        :return:
        """
        for index, comp_data in enumerate(self.netlist):
            if comp_data['designator'] == designator:
                return index

    def get_mat_fh(self):
        """
        method: matrix F and matrix H
        :return:
        """
        # Zero matrix F and H
        f = np.zeros([self.num_comps, self.num_comps], float)
        h = np.zeros([self.num_comps, self.num_comps], float)
        # fill F and H
        for k, comp_data in enumerate(self.netlist):
            comp_nm = comp_data['designator'].split('-')[0]
            vol_dir = comp_data['vol_dir']
            cur_dir = comp_data['cur_dir']
            if comp_nm == 'G':
                f[k, k] = comp_data['value'] * vol_dir
                h[k, k] = -cur_dir
            elif comp_nm == 'C':
                f[k, k] = 1e-9 * vol_dir
                h[k, k] = -cur_dir
            elif comp_nm == 'R':
                f[k, k] = -vol_dir
                h[k, k] = comp_data['value'] * cur_dir
            elif comp_nm == 'L':
                f[k, k] = -vol_dir
                h[k, k] = 1e-9 * cur_dir
            elif 'U' in comp_nm:
                f[k, k] = vol_dir
                h[k, k] = 0
            elif 'I' in comp_nm:
                f[k, k] = 0
                h[k, k] = cur_dir
            # voltage control voltage source
            elif comp_nm == 'VcVs':
                j = self.get_index_from_designator(designator=comp_data['control'])
                f[k, k] = 1
                f[k, j] = comp_data['factor'] * (-1) * vol_dir
                h[k, k] = 0
            # voltage control current source
            elif comp_nm == 'VcCs':
                j = self.get_index_from_designator(designator=comp_data['control'])
                f[k, k] = 0
                f[k, j] = comp_data['factor'] * (-1) * cur_dir
                h[k, k] = 1
            # current control voltage source
            elif comp_nm == 'CcVs':
                j = self.get_index_from_designator(designator=comp_data['control'])
                f[k, k] = 1
                h[k, j] = comp_data['factor'] * (-1) * vol_dir
                h[k, k] = 0
            # current control current source
            elif comp_nm == 'CcCs':
                j = self.get_index_from_designator(designator=comp_data['control'])
                f[k, k] = 0
                h[k, j] = comp_data['factor'] * (-1) * cur_dir
                h[k, k] = 1
            # primary side of transformer
            elif comp_nm == 'Tp':
                sn = comp_data['designator'].split('-')[1]
                j = self.get_index_from_designator(designator='Ts-' + sn)
                f[k, k] = 1
                f[k, j] = -comp_data['ratio'] * vol_dir
                h[k, k] = 0
            # second side of transformer
            elif comp_nm == 'Ts':
                sn = comp_data['designator'].split('-')[1]
                j = self.get_index_from_designator(designator='Tp-' + sn)
                f[k, k] = 0
                h[k, j] = comp_data['ratio'] * cur_dir
                h[k, k] = 1
        return f, h

    def get_mat_aefh(self):
        """
        method:
        :return:
        """
        # matrix zero
        zero_1 = np.zeros([self.num_nodes, self.num_nodes], float)
        zero_2 = np.zeros([self.num_nodes, self.num_comps], float)
        zero_3 = np.zeros([self.num_comps, self.num_comps], float)
        zero_4 = np.zeros([self.num_comps, self.num_nodes], float)

        # matrix
        mat_a = self.get_mat_a()
        one = self.get_mat_e()
        mat_f, mat_h = self.get_mat_fh()
        # concatenate
        mat_1 = np.concatenate([zero_1, zero_2, mat_a], axis=1)
        mat_2 = np.concatenate([-mat_a.T, one, zero_3], axis=1)
        mat_3 = np.concatenate([zero_4, mat_f, mat_h], axis=1)
        mat_aefhmnq = np.concatenate([mat_1, mat_2, mat_3], axis=0)

        return mat_aefhmnq

    def get_mat_b(self):
        """
        method: get matrix mat_b
        :return:
        """
        ui_s = np.zeros([self.num_comps, 1], float)
        j = 0
        for k, comp_data in enumerate(self.netlist):
            comp_nm = comp_data['designator'].split('-')[0]
            if 'Udc' in comp_nm:
                ui_s[k] = comp_data['amp']
            elif 'Idc' in comp_nm:
                ui_s[k] = comp_data['amp']

        # vector zero
        zero_5 = np.zeros([self.num_nodes, 1], float)
        zero_6 = np.zeros([self.num_comps, 1], float)
        # concatenate
        mat_b = np.concatenate([zero_5, zero_6, ui_s], axis=0)

        return mat_b

    def assign_result(self,
                      x):
        """
        method: assign self.u_nodes self.u_comps self.i_comps
        :param x: result
        :return: None
        """
        for i, node in enumerate(self.u_nodes):
            self.u_nodes[node] = x[i, 0]
        for i, comp in enumerate(self.u_comps):
            self.u_comps[comp] = x[i + self.num_nodes, 0]
            self.i_comps[comp] = x[i + self.num_nodes + self.num_comps, 0]

    def calculate(self):
        """
        method: calculate
        :return:
        """
        x = np.linalg.solve(self.mat_aefh, self.mat_b)
        self.assign_result(x)


class Calculation:
    """
    class: Calculation of circuit
    """
    def __init__(self,
                 netlist,
                 cir_calc_data=None,
                 **kwargs):
        """
        method: create Calculation
        :param netlist: netlist
        :param cir_calc_data: circuit calculation data,
        :param kwargs: Keyword arguments, refer to Elecpy.dft_cal_config, e.g.,
        'calc_method': calculation method, e.g., 'Dynamic', 'SinSteady'
        't_step': time step, second, e.g., 1e-6
        't_lim': time limitation, second, e.g., 1.0
        """
        # netlist
        self.netlist = None
        # calculation data of circuit
        self.cir_calc_data = cir_calc_data
        # calculation config_data
        self.calc_data = copy.deepcopy(default.dft_calc_data)
        # Progressbar variable
        self.calc_progress_var = None

        # set the data
        self.set_data(netlist,
                      cir_calc_data=cir_calc_data,
                      **kwargs)

    def is_method_legal(self,
                        method):
        """
        method: judge if the method is legal for the netlist
        :parma method: calculation method, Dynamic, SinSteady, DCSteady
        :return: True, False
        """
        # check the source, resistor and capacitor
        source = False
        resistor = False
        capacitor = False
        for key in self.netlist:
            if 'U' in key['designator'] or 'I' in key['designator']:
                source = True
            if 'C' in key['designator']:
                capacitor = True
            if 'R' in key['designator']:
                resistor = True
        # judge if the method is legal
        if method == 'Dynamic':
            if source is True and capacitor is True and resistor is False:
                return False
            return True
        elif method == 'SinSteady':
            for key in self.netlist:
                if 'Udc' in key['designator'] or 'Idc' in key['designator']:
                    return False
                if 'D' in key['designator']:
                    return False
            if source:
                return True
        elif method == 'DCSteady':
            for key in self.netlist:
                if 'ac' in key['designator']:
                    return False
            return True

    def set_data(self,
                 netlist=None,
                 cir_calc_data=None,
                 **kwargs):
        """
        method: set data
        :param netlist: netlist
        :param cir_calc_data: circuit's calculation data
        :param kwargs: Keyword arguments, refer to Elecpy.dft_cal_config, e.g.,
        :return: None
        """
        if netlist is not None:
            self.netlist = netlist
        if cir_calc_data:
            for key in self.calc_data:
                self.calc_data[key] = cir_calc_data[key]
        for key in kwargs:
            if kwargs[key] is not None and key in self.calc_data.keys():
                self.calc_data[key] = kwargs[key]

    def dynamic_calc(self):
        """
        method: Dynamic calculation of circuit
        :return: None
        """
        # calculate
        dyn_cal = DynamicCirCal()
        dyn_cal.set_params(self.netlist, h=self.calc_data['t_step'])
        dyn_cal.init_cal()

        for i in np.arange(0, int(self.calc_data['t_lim'] / self.calc_data['t_step'])):
            # repeat calculation
            dyn_cal.repeat_cal(iter=i)

        # get the result
        self.cir_calc_data['u_comps'] = self.calc_data['u_comps'] = dyn_cal.u_comps
        self.cir_calc_data['i_comps'] = self.calc_data['i_comps'] = dyn_cal.i_comps
        self.cir_calc_data['u_nodes'] = self.calc_data['u_nodes'] = dyn_cal.u_nodes
        self.cir_calc_data['time'] = self.calc_data['time'] = dyn_cal.time

    def sinsteady_calc(self):
        """
        method: sinusoidal steady-state calculation of circuit
        :return: None
        """
        # calculate
        sst_cal = SinSteadyCirCal()
        sst_cal.set_params(self.netlist)
        sst_cal.calculate()
        # get the result
        self.cir_calc_data['u_comps'] = self.calc_data['u_comps'] = sst_cal.u_comps
        self.cir_calc_data['i_comps'] = self.calc_data['i_comps'] = sst_cal.i_comps
        self.cir_calc_data['u_nodes'] = self.calc_data['u_nodes'] = sst_cal.u_nodes

    def dcsteady_calc(self):
        """
        method: dc steady-state calculation of circuit
        :return: None
        """
        # calculate
        sst_cal = DCSteadyCirCal()
        sst_cal.set_params(self.netlist)
        sst_cal.calculate()
        # get the result
        self.cir_calc_data['u_comps'] = self.calc_data['u_comps'] = sst_cal.u_comps
        self.cir_calc_data['i_comps'] = self.calc_data['i_comps'] = sst_cal.i_comps
        self.cir_calc_data['u_nodes'] = self.calc_data['u_nodes'] = sst_cal.u_nodes

    def calculate(self):
        """
        method: calculate the circuit
        :return:
        """
        # implement certain calculation algorithm according to calc_method chosen
        if self.calc_data['calc_method'] == 'Dynamic':
            self.dynamic_calc()
        elif self.calc_data['calc_method'] == 'SinSteady':
            self.sinsteady_calc()
        elif self.calc_data['calc_method'] == 'DCSteady':
            self.dcsteady_calc()
        # refresh the calc_method
        self.cir_calc_data['calc_method'] = self.calc_data['calc_method']


class CalculationGUI(Calculation):
    """
    class: GUI for the Calculation
    """
    def __init__(self,
                 netlist,
                 cir_calc_data=None):
        """
        method: create the GUI
        :param netlist:
        :param cir_calc_data: a circuit's config data
        """
        # root window of the Calculation
        self.root_win = None
        self.win_width = None
        self.win_height = None
        # frame operation, project, content
        self.frame_oper = None
        self.frame_prj = None
        self.frame_cont = None
        # operation page and variable list page
        self.page_oper = None
        self.page_method_list = None

        super().__init__(netlist=netlist,
                         cir_calc_data=cir_calc_data)

        self.build_root_win(geometry='800x600')
        self.build_oper_page(master=self.frame_oper)
        self.build_method_list(master=self.frame_prj)

    def build_root_win(self,
                       geometry=None):
        """
        method: build a root window for circuit GUI
        :param geometry: window's geometry, e.g., '1920x1200'
        :return: None
        """
        self.root_win = tk.Toplevel()
        self.root_win.grid_propagate(0)
        self.root_win.title('Elecpy->Calculation')
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

        # operation frame
        self.frame_oper = tk.LabelFrame(self.root_win, bg='#F0F0F0', text=None, font=('仿宋', 12),
                                        height=32,
                                        width=self.win_width)
        self.frame_oper.grid(row=0, column=0, columnspan=2)
        self.frame_oper.grid_propagate(0)

        # project frame
        self.frame_prj = tk.LabelFrame(self.root_win, bg='#F0F0F0', text=None, font=('仿宋', 12),
                                       height=self.win_height - 32,
                                       width=200)
        self.frame_prj.grid(row=1, column=0)
        self.frame_prj.grid_propagate(0)

        # cont frame
        self.frame_cont = tk.LabelFrame(self.root_win, bg='#F0F0F0', text=None, font=('仿宋', 12),
                                        height=self.win_height - 32,
                                        width=self.win_width - 200)
        self.frame_cont.grid(row=1, column=1)
        self.frame_cont.grid_propagate(0)

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
                                                  btn_lst=['Run'],
                                                  wdg_width=80,
                                                  num_per_row=20)
        self.calc_progress_var = tk.StringVar(value='')
        label = ttk.Label(master=master, textvariable=self.calc_progress_var)
        label.grid(row=0, column=1)
        label.grid_propagate(0)
        self.page_oper.command(btn_nm='Run',
                               cal_func=self.gui_calculate)

    def build_method_list(self,
                          master):
        """
        method:
        :param master: the tkinter widget, tkinter.Frame
        :return:
        """
        list_data = []
        for data in ['Dynamic', 'SinSteady', 'DCSteady']:
            if self.is_method_legal(method=data):
                list_data.append(data)
        self.page_method_list = gui_elements.ListboxPage(master=master,
                                                         row=1,
                                                         height=250,
                                                         label='Algorithm Method',
                                                         list_data=list_data)
        self.page_method_list.command(cal_func=self.build_cont_page)

    def build_dynamic_page(self):
        """
        method:
        :return:
        """
        def cal_func(value):
            """cal function"""
            self.calc_data['t_step'] = value[0]
            self.calc_data['t_lim'] = value[1]
            self.cir_calc_data['t_step'] = self.calc_data['t_step']
            self.cir_calc_data['t_lim'] = self.calc_data['t_lim']

        data = [{'style': 'Entry', 'name': 't_step', 'value': self.cir_calc_data['t_step']},
                {'style': 'Entry', 'name': 't_lim', 'value': self.cir_calc_data['t_lim']}]

        edit_page = gui_elements.NormalEditPage(master=self.frame_cont,
                                                label='Dynamic Calculation Config',
                                                save_butt_label='Confirm',
                                                save_butt_func=cal_func,
                                                data=data)

    def build_sinsteady_page(self):
        """
        method:
        :return:
        """
        def cal_func(value):
            """cal function"""
            pass

        data = []

        edit_page = gui_elements.NormalEditPage(master=self.frame_cont,
                                                label='Sinusoidal Steady-State Calculation Config',
                                                save_butt_label='Confirm',
                                                save_butt_func=cal_func,
                                                data=data)

    def build_dcsteady_page(self):
        """
        method:
        :return:
        """
        def cal_func(value):
            """cal function"""
            pass

        data = []

        edit_page = gui_elements.NormalEditPage(master=self.frame_cont,
                                                label='DC Steady-State Calculation Config',
                                                save_butt_label='Confirm',
                                                save_butt_func=cal_func,
                                                data=data)

    def build_cont_page(self,
                        label=None,
                        method=None):
        """
        method:
        :param label:
        :param method:
        :return:
        """
        self.calc_data['calc_method'] = method
        if method == 'Dynamic':
            self.build_dynamic_page()
        elif method == 'SinSteady':
            self.build_sinsteady_page()
        elif method == 'DCSteady':
            self.build_dcsteady_page()

    def gui_calculate(self):
        """
        method: gui calculation
        :return:
        """
        self.calculate()
        answer = messagebox.askquestion(title='calculation completed!',
                                        message='The calculation is completed, do you want to open the graph config'
                                                ' window?')
        self.root_win.destroy()
        if answer == 'yes':
            self.open_graph()

    def open_graph(self):
        """
        method:
        :return:
        """
        if self.calc_data['calc_method'] == 'Dynamic':
            graph.GraphGUI(data_ucomps=self.calc_data['u_comps'],
                           data_icomps=self.calc_data['i_comps'],
                           data_unodes=self.calc_data['u_nodes'],
                           data_time=self.calc_data['time'])
        elif self.calc_data['calc_method'] == 'SinSteady':
            graph.GraphGUI(data_ucomps=self.calc_data['u_comps'],
                           data_icomps=self.calc_data['i_comps'],
                           data_unodes=self.calc_data['u_nodes'])
        elif self.calc_data['calc_method'] == 'DCSteady':
            graph.GraphGUI(data_ucomps=self.calc_data['u_comps'],
                           data_icomps=self.calc_data['i_comps'],
                           data_unodes=self.calc_data['u_nodes'])


if __name__ == '__main__':

    """netlist = [{'designator': 'Uac-1', 'amp': 10.0, 'freq': 50.0, 'phase': 0, 'node1': 1, 'node2': 0, 'vol_dir': 1, 
    'cur_dir': 1},
               {'designator': 'Tp-1', 'ratio': 2, 'node1': 1, 'node2': 0, 'vol_dir': 1, 'cur_dir': 1},
               {'designator': 'Ts-1', 'ratio': 2, 'node1': 2, 'node2': 0, 'vol_dir': 1, 'cur_dir': 1},
               {'designator': 'R-1', 'value': 10.0, 'node1': 2, 'node2': 0, 'vol_dir': 1, 'cur_dir': 1}]"""
    netlist = [{'designator': 'Uac-1', 'amp': 10.0, 'freq': 50.0, 'phase': 0, 'node1': 1, 'node2': 0, 'vol_dir': 1,
                'cur_dir': 1},
               {'designator': 'R-1', 'value': 10.0, 'node1': 1, 'node2': 2, 'vol_dir': 1, 'cur_dir': 1},
               {'designator': 'C-1', 'value': 0.0001, 'Uc': 0, 'node1': 2, 'node2': 0, 'vol_dir': 1, 'cur_dir': 1}]

    circal = SinSteadyCirCal()
    circal.set_params(netlist)
    circal.calculate()

    """circal = DynamicCirCal()
    circal.set_params(netlist)
    circal.init_cal()
    for i in range(1, 100000):
        circal.repeat_cal(iter=i)"""

    """root_win = tk.Tk()
    root_win.geometry('1500x1000')

    grph = graph.Graph(master=root_win,
                       data_ucomps=circal.u_comps,
                       data_icomps=circal.i_comps,
                       data_unodes=circal.u_nodes)
    grph.divide_figure(nrows=2, ncols=1)
    grph.add_pha_axes(axes_id='0-0')
    grph.add_axes(row=1, col=0, axes_id='1-0')
    root_win.mainloop()"""

    grph = backup.GraphGUI(data_ucomps=circal.u_comps,
                           data_icomps=circal.i_comps,
                           data_unodes=circal.u_nodes)
