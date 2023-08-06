"""
This module is used for manipulating of files, e.g., reading, writing, etc..
"""
import os


class File:
    """
    class: File
    """
    def __init__(self):
        """
        method: create a file manipulator
        """
        # .elc file's path(full path, including path and file)
        self.source_elcfilepath = None
        # .cmp file's path(full path, including path and file)
        self.source_cmpfilepath = None

    @staticmethod
    def jdg_elc_file_sta(fline):
        """
        func: judge start sign of the .elc file
        :param fline: one line of a file's data
        :return: It's the .elc file: True, It's not the .elc file: False
        """
        if '<<elc_file>>' in fline:
            return True
        else:
            return False

    @staticmethod
    def jdg_cmp_file_sta(fline):
        """
        func: judge start sign of the .cmp file
        :param fline: one line of a file's data
        :return:
        """
        if '<<cmp_file>>' in fline:
            return True
        else:
            return False

    @staticmethod
    def jdg_file_end(fline):
        """
        func: judge end sign of a file
        :param fline: one line of a file's data
        :return:
        """
        if '<<end>>' in fline:
            return True
        else:
            return False

    @staticmethod
    def wr_elc_file_sta(file):
        """
        func: write a start sign to a .elc file
        :param file: "with open(filepath, 'r') as file"
        :return: None
        """
        file.write('<<elc_file>>\n\n\n')

    @staticmethod
    def wr_cmp_file_sta(file):
        """
        func: write a start sign to a .cmp file
        :param file: "with open(filepath, 'r') as file"
        :return: None
        """
        file.write('<<cmp_file>>\n\n\n')

    @staticmethod
    def wr_file_end(file):
        """
        func: write a end sign to a file
        :param file: "with open(filepath, 'r') as file"
        :return: None
        """
        file.write('\n\n\n<<end>>')

    def open_elcfile(self,
                     path=None,
                     file=None):
        """
        method: Open a .elc file, return cir_data={'comps_data': [], 'wires_data': [], 'texts_data': []}
        :param path: path of file, e.g., 'E:/'
        :param file: file, e.g., 'xxx.elc'
        :return:
        """
        if file.split('.')[1] != 'elc':
            raise TypeError('The file must be .elc!')
        filepath = os.path.join(path, file)
        if not os.path.isfile(filepath):
            raise TypeError('The file is not exist!!')

        self.source_elcfilepath = filepath

        # data segment start flag
        elc_rd_section = False
        # data container
        elc_data = None

        with open(filepath, 'r') as file:
            lines = file.readlines()
            for i, el in enumerate(lines):
                # check the .elc file's start sign
                if File.jdg_elc_file_sta(el):
                    elc_rd_section = True

                # judge if the data segment starts
                elif elc_rd_section and el != '\n' and el != '<<end>>':
                    elc_data = eval(el)

                # check the .elc file's end sign
                elif File.jdg_file_end(el):
                    break
        # record the full path of the source data from which get the source data
        self.source_cmpfilepath = filepath

        # return electric data
        return elc_data

    def save_elcfile(self,
                     elc_data,
                     filepath=None,
                     overwrite=False):
        """
        method: save .elc file, following the rules as below:
        If filepath is not default, cir_data will be saved into filepath.
        If filepath is default, cir_data will be saved into self.source_cirfilepath.
        If filepath is default and self.source_cirfilepath is None, nothing will be done
        :param elc_data: data of the electric or electronic
        :param filepath: file's full path(inclucing path and file, e.g., 'E:/xxx.elc')
        :param overwrite: if the file can be overwritten.
        When the filepath is already existed, if overwrite is True, overwritten to filepath will occur,
        otherwise, nothing will be done.
        :return: saved: True, not saved: False
        """
        # check the file style
        if filepath is not None:
            if os.path.basename(filepath).split('.')[1] != 'elc':
                print('The file must be .elc!')
                return

        # if filepath is not default, save elc_data into filepath.
        if filepath:
            if os.path.isfile(filepath):
                if overwrite:
                    print('Overwritten occured!')
                    elcfilepath = filepath
                else:
                    print('The file is already existed!')
                    return False
            else:
                elcfilepath = filepath
        # if filepath is default and self.source_cirfilepath is not None, save cir_data into self.source_cirfilepath.
        elif self.source_elcfilepath:
            elcfilepath = self.source_elcfilepath
        # else, nothing will be done
        else:
            print('The directory to save the file is needed!')
            return False

        # open file-cirfilepath
        with open(elcfilepath, 'w') as file:
            File.wr_elc_file_sta(file)
            file.write(str(elc_data))
            File.wr_file_end(file)

        # store filepath
        self.source_elcfilepath = elcfilepath
        # return
        return True

    def open_cmpfile(self,
                     path,
                     file):
        """
        method: Open a .cmp file, return comp_data={'id': 'crd_x': 'crd_y': , ...}
        :param path: path of the file, e.g., 'E:/'
        :param file: file, e.g., 'xxx.cmp'
        :return: data from the file
        """
        if file.split('.')[1] != 'cmp':
            raise TypeError('The file must be .cmp!')
        filepath = os.path.join(path, file)
        if not os.path.isfile(filepath):
            raise TypeError('The file is not exist!!')

        # data segment start flag
        comp_rd_section = False
        # data container
        comp_data = {}

        with open(filepath, 'r') as file:
            lines = file.readlines()
            for i, el in enumerate(lines):
                if File.jdg_cmp_file_sta(el):
                    comp_rd_section = True
                elif comp_rd_section and el != '\n' and el != '<<end>>':
                    comp_data = eval(el)
                elif File.jdg_file_end(el):
                    break

        # record the full path of the source data from which get the source data
        self.source_cmpfilepath = filepath

        return comp_data

    def save_cmpfile(self,
                     comp_data,
                     filepath=None,
                     overwrite=False):
        """
        method: save the .cmp file, following rules as below:
        If filepath is not default, save comp_data to filepath.
        If filepath is default, save comp_data to self.source_cmpfilepath.
        If filepath is default and self.source_cmpfilepath is None, nothing will be done.
        :param comp_data: Component source data
        :param filepath: path/file, e.g., 'E:/xxx.cmp'
        :param overwrite: if the file can be overwritten.
        When the filepath is already existed, if overwrite is True, overwritten to filepath will occur,
        otherwise, nothing will be done.
        :return: saved: True, not saved: False
        """
        # check the file style
        if os.path.basename(filepath).split('.')[1] != 'cmp':
            raise TypeError('The file must be .cmp!')

        # if filepath is not default, save comp_data to filepath
        if filepath:
            if os.path.isfile(filepath):
                if overwrite:
                    print('Overwritten occured!')
                    cmpfilepath = filepath
                else:
                    print('The file is already existed!')
                    return False
            else:
                cmpfilepath = filepath
        # if filepath is default, save comp_data to self.source_cirfilepath if it is not None
        elif self.source_cmpfilepath:
            cmpfilepath = self.source_elcfilepath
        else:
            print('The directory to save the file is needed!!')
            return False

        # open cmpfilepath and write comp_data in.
        with open(cmpfilepath, 'w') as file:
            File.wr_cmp_file_sta(file)
            file.write(str(comp_data))
            File.wr_file_end(file)

        # store the filepath to self.source_cmpfilepath
        self.source_cmpfilepath = filepath
        return True


if __name__ == '__main__':
    cirfile = File()
