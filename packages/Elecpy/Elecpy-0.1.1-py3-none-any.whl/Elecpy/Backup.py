"""
This module is used for some backup code segments
"""
from Elecpy.Default import *
import copy
from Elecpy.File import *
from Elecpy.Platform import *
from Elecpy.Graph import *
import Elecpy.GUIElements as GUIElements


class Project:
    """
    class: project
    """
    def __init__(self,
                 root_path):
        """
        method: create a project
        :param root_path: root path of the project
        """
        self.root_path = root_path

        # circuit data
        self.cirs_data = {}
        #
        self.cir_obj = None
        self.content = None

        self.load_cirs_data()

    def cir_content(self,
                    pframe=None):
        """
        method: content for circuit
        :param pframe: parent frame
        :return: None
        """
        cont_data = pd.DataFrame({'directory': [],
                                 'file': []})
        for i, directory in enumerate(os.listdir(self.root_path)):
            dir_path = os.path.join(self.root_path, directory)
            for j, file in enumerate(os.listdir(dir_path)):
                file = file.replace('.xlsx', '')
                data = pd.DataFrame({'directory': [directory],
                                     'file': [file]})
                cont_data = cont_data.append(data,
                                             ignore_index=True)
        self.content = Contents(pframe=pframe,
                                wdg_height=250,
                                cont_data=cont_data,
                                open_flag=(True, False))

    def load_cirs_data(self):
        """
        method: load all the circuits' data
        :return:
        """
        for i, directory in enumerate(os.listdir(self.root_path)):
            dir_path = os.path.join(self.root_path, directory)
            for j, file in enumerate(os.listdir(dir_path)):
                cir_id = file.replace('.xlsx', '')
                cir_data_path = os.path.join(self.root_path, directory, file).replace('\\', '/')
                comps_data = pd.read_excel(io=cir_data_path,
                                           sheet_name='comps_data')
                wires_data = pd.read_excel(io=cir_data_path,
                                           sheet_name='wires_data')
                cirdata = {'comps_data': comps_data, 'wires_data': wires_data}

                self.cirs_data[cir_id] = cirdata

    def create_circuit(self,
                       cir_id=None,
                       pframe=None,
                       cav_width=None,
                       cav_height=None):
        """
        method: create circuit
        :param cir_id: circuit id
        :param pframe: parent frame
        :param cav_width: canvas width
        :param cav_height: canvas height
        :return:
        """
        if cir_id in self.cirs_data.keys():
            cirdata = self.cirs_data[cir_id]
            self.cir_obj = CirDiagram(cir_id=cir_id,
                                   pframe=pframe,
                                   cav_width=cav_width,
                                   cav_height=cav_height,
                                   **cirdata)
            self.cir_obj.mode_normal()
            # self.cir_obj.calc_sin_steady_cir()

    def new_circuit(self,
                    cir_id=None,
                    pframe=None,
                    cav_width=None,
                    cav_height=None):
        """
        method:
        :param cir_id:
        :param pframe: parent frame
        :param cav_width: canvas width
        :param cav_height: canvas height
        :return:
        """
        self.cir_objs = CirDiagram(cir_id=cir_id,
                                pframe=pframe,
                                cav_width=cav_width,
                                cav_height=cav_height)


if __name__ == '__main__':
    cir = Platform(cir_name='test')
    cir.add_res(designator='R-3')
    crd = (60, 60)
    cir.select(crd)

    # cir.add_component(comp_nm='resistor')
    print(cir.source_data)
