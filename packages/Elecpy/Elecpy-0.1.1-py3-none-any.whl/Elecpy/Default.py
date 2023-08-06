"""
This module is used for default data's definition.
"""
import copy


# component's name mapping to designator
nm2designator = {'resistor': 'R',
                 'capacitor': 'C',
                 'inductor': 'L',
                 'diode': 'D',
                 'voltage_ac': 'Uac',
                 'voltage_dc': 'Udc',
                 'current_ac': 'Iac',
                 'current_dc': 'Idc',
                 'ground': 'GND',
                 'gap': 'Gap',
                 'vcvs': 'VCVS',
                 'vccs': 'VCCS',
                 'ccvs': 'CCVS',
                 'cccs': 'CCCS'}

# default circuit's calculation data
# calc_method: str, 'Dynamic', 'SinSteady', 'DCSteady'
# t_step: every step of time, second, float, 1e-6 means 1us
# t_lim: limitation of time, second, float, None
dft_calc_data = {'calc_method': 'Dynamic',
                 't_step': 1e-5,
                 't_lim': 1.0,
                 'u_comps': None,
                 'i_comps': None,
                 'u_nodes': None,
                 'time': None}

# default circuit configuration
# ref_vol_visible: visible of reference direction of voltage, None, True, False
# ref_cur_visible: visible of reference direction of current, None, True, False
# canvas_grid_line: line style of grid on the circuit's canvas, str, 'line', 'dot'
# canvas_grid_intvl: grid's interval, int, 20
dft_elec_config = {'ref_vol_visible': None,
                   'ref_cur_visible': None,
                   'canvas_grid_line': 'line',
                   'canvas_grid_intvl': 20}


# default circuit data
dft_elc_data = {'elec_name': 'New Elec',
                'elec_config': copy.deepcopy(dft_elec_config),
                'comps_data': {},
                'conns_data': {},
                'texts_data': {},
                'grphs_data': {},
                'calc_data': copy.deepcopy(dft_calc_data)}

# default resistor data
dft_res_data = {'id': 'resistor-?',
                'designator': 'R-?',
                'value': 10.0,
                'node1': None,
                'node2': None,
                'vol_dir': 1,
                'cur_dir': 1,
                'crd_x': 60,
                'crd_y': 60,
                'angle': 0}

# default capacitor data
dft_cap_data = {'id': 'capacitor-?',
                'designator': 'C-?',
                'value': 1E-6,
                'Uc': 0,
                'node1': None,
                'node2': None,
                'vol_dir': 1,
                'cur_dir': 1,
                'crd_x': 60,
                'crd_y': 60,
                'angle': 0}

# default inductor data
dft_ind_data = {'id': 'inductor-?',
                'designator': 'L-?',
                'value': 1E-6,
                'Il': 0,
                'node1': None,
                'node2': None,
                'vol_dir': 1,
                'cur_dir': 1,
                'crd_x': 60,
                'crd_y': 60,
                'angle': 0}

# default diode data
dft_dio_data = {'id': 'diode-?',
                'designator': 'D-?',
                'Ir': 55E-6,
                'Rr': 1000000.0,
                'Vf': 0.5,
                'Rf': 0.0001,
                'node1': None,
                'node2': None,
                'vol_dir': 1,
                'cur_dir': 1,
                'crd_x': 60,
                'crd_y': 60,
                'angle': 0}

# default gap data
dft_gap_data = {'id': 'gap-?',
                'designator': 'Gap-?',
                'Roff': 1E9,
                'Ron': 1.0,
                'node1': None,
                'node2': None,
                'vol_dir': 1,
                'cur_dir': 1,
                'crd_x': 60,
                'crd_y': 60,
                'angle': 0}

# default dc voltage source data
dft_vdc_data = {'id': 'voltage_dc-?',
                'designator': 'Udc-?',
                'amp': 10.0,
                'node1': None,
                'node2': None,
                'vol_dir': 1,
                'cur_dir': -1,
                'crd_x': 60,
                'crd_y': 60,
                'angle': 0}

# default ac voltage source data
dft_vac_data = {'id': 'voltage_ac-?',
                'designator': 'Uac-?',
                'amp': 10.0,
                'freq': 50.0,
                'phase': 0.0,
                'node1': None,
                'node2': None,
                'vol_dir': 1,
                'cur_dir': -1,
                'crd_x': 60,
                'crd_y': 60,
                'angle': 0}

# default dc current source data
dft_idc_data = {'id': 'current_dc-?',
                'designator': 'Idc-?',
                'amp': 10.0,
                'node1': None,
                'node2': None,
                'vol_dir': -1,
                'cur_dir': 1,
                'crd_x': 60,
                'crd_y': 60,
                'angle': 0}

# default data of ac current source
dft_iac_data = {'id': 'current_ac-?',
                'designator': 'Iac-?',
                'amp': 10.0,
                'freq': 50.0,
                'phase': 0.0,
                'node1': None,
                'node2': None,
                'vol_dir': -1,
                'cur_dir': 1,
                'crd_x': 60,
                'crd_y': 60,
                'angle': 0}

# default data of primary side of transformer
dft_transformer_data = {'id': 'transformer-?',
                        'designator': 'T-?',
                        'ratio': 10.0,
                        'node1': None,
                        'node2': None,
                        'node3': None,
                        'node4': None,
                        'vol_dir': 1,
                        'cur_dir': 1,
                        'crd_x': 60,
                        'crd_y': 60,
                        'angle': 0}

# default data of voltage control voltage source
dft_vcvs_data = {'id': 'VcVs-?',
                 'designator': 'VcVs-?',
                 'control': '',
                 'factor': 1,
                 'node1': None,
                 'node2': None,
                 'vol_dir': 1,
                 'cur_dir': 1,
                 'crd_x': 60,
                 'crd_y': 60,
                 'angle': 0}

# default data of voltage control current source
dft_vccs_data = {'id': 'VcCs-?',
                 'designator': 'VcCs-?',
                 'control': '',
                 'factor': 1,
                 'node1': None,
                 'node2': None,
                 'vol_dir': 1,
                 'cur_dir': 1,
                 'crd_x': 60,
                 'crd_y': 60,
                 'angle': 0}

# default data of current control voltage source
dft_ccvs_data = {'id': 'CcVs-?',
                 'designator': 'CcVs-?',
                 'control': '',
                 'factor': 1,
                 'node1': None,
                 'node2': None,
                 'vol_dir': 1,
                 'cur_dir': 1,
                 'crd_x': 60,
                 'crd_y': 60,
                 'angle': 0}

# default data of current control current source
dft_cccs_data = {'id': 'CcCs-?',
                 'designator': 'CcCs-?',
                 'control': '',
                 'factor': 1,
                 'node1': None,
                 'node2': None,
                 'vol_dir': 1,
                 'cur_dir': 1,
                 'crd_x': 60,
                 'crd_y': 60,
                 'angle': 0}

# default data of ground
dft_gnd_data = {'id': 'ground-?',
                'designator': 'GND-?',
                'node1': None,
                'vol_dir': 1,
                'cur_dir': 1,
                'crd_x': 60,
                'crd_y': 60,
                'angle': 0}

# default data of all kinds of components
dft_comps_data = {'resistor': dft_res_data,
                  'capacitor': dft_cap_data,
                  'inductor': dft_ind_data,
                  'diode': dft_dio_data,
                  'voltage_ac': dft_vac_data,
                  'voltage_dc': dft_vdc_data,
                  'current_ac': dft_iac_data,
                  'current_dc': dft_idc_data,
                  'ground': dft_gnd_data,
                  'gap': dft_gap_data,
                  'vcvs': dft_vcvs_data,
                  'vccs': dft_vccs_data,
                  'ccvs': dft_ccvs_data,
                  'cccs': dft_cccs_data}

# default data of wire
dft_wire_data = {'id': 'wire-1',
                 'designator': 'w-?',
                 'net_id': '1',
                 'sta_comp': None,
                 'sta_tmnl': None,
                 'end_comp': None,
                 'end_tmnl': None,
                 'mid_crds': None}

# default data of text
dft_text_data = {'id': 'text-1',
                 'crd_x': 0,
                 'crd_y': 20,
                 'angle': 0,
                 'color': 'black',
                 'visible': True,
                 'content': 'text',
                 'font_family': 'Times',
                 'font_size': '8',
                 'font_weight': 'bold',
                 'font_slant': 'roman',
                 'font_underline': 0,
                 'font_overstrike': 0}

# default data of current direction arrow symbol
dft_arrow_data = {'id': 'arrow-1',
                  'crd_x': 0,
                  'crd_y': 20,
                  'angle': 0,
                  'visible': True,
                  'tail_len': 20,
                  'arrw_len': 20,
                  'arrw_wid': 5,
                  'color': '#F64F5F'}

# default data of positive-negative symbol
dft_posneg_data = {'id': 'pn-1',
                   'crd_x': 0,
                   'crd_y': 20,
                   'angle': 0,
                   'visible': True,
                   'size': 8,
                   'distance': 60,
                   'color': '#F64F5F'}

# default data of graph of component
dft_graphs_data = {'arrow': dft_arrow_data,
                   'pn': dft_posneg_data}

# default phasor
dft_phasor_data = {'origin': (0, 0),
                   'amp': 0,
                   'phase': 0}

if __name__ == '__main__':
    print(dft_comps_data['R'])
