"""
formula edition
"""


def sqrt(pcanv, x, y, low, up, formula, diff, char_size=8):
    pass


def Integral(pcanv, x, y, low, up, formula, diff, char_size=8):
    """
    func: integral formula
    :param pcanv:
    :param x:
    :param y:
    :param low:
    :param up:
    :param formula:
    :param diff:
    :param char_size:
    :return:
    """
    pcanv.create_text(x, y, text='∫', font=('Calibri', char_size * 3))
    pcanv.create_text(x + char_size, y, text=str(up), font=('Calibri', char_size), anchor=tk.SW)
    pcanv.create_text(x + int(char_size / 2), y + char_size * 2, text=str(low), font=('Calibri', char_size),
                      anchor=tk.W)
    pcanv.create_text(x + char_size * 2, y, text=formula, font=('Calibri', int(char_size * 3 / 2)), anchor=tk.W)
    pcanv.create_text(x + char_size * 2 + len(formula) * char_size, y, text='d',
                      font=('Calibri', int(char_size * 3 / 2)))
    pcanv.create_text(x + char_size * 2 + (len(formula) + 1) * char_size, y, text=diff,
                      font=('Calibri', int(char_size * 3 / 2)))


def disp_formula(pcanv, formula_list):
    """

    :param pcanv:
    :param formula_list: formula list, [{'类别': 导线, '参数': {[顶点列表]}}]
    :return:
    """
    if formula_list['类别'] == 'line':
        pcanv.create_line(x, y)
    elif formula_list['类别'] == 'text':
        pcanv.create_text(x, y)
    elif fromula_list['类别'] == 'circle':
        pass
    pcanv.create_text(x, y, text='∫', font=('Calibri', char_size*3))
    pcanv.create_text(x+char_size, y, text=str(up), font=('Calibri', char_size), anchor=tk.SW)
    pcanv.create_text(x+int(char_size/2), y+char_size*2, text=str(low), font=('Calibri', char_size), anchor=tk.W)
    pcanv.create_text(x+char_size*2, y, text=formula, font=('Calibri', int(char_size*3/2)), anchor=tk.W)
    pcanv.create_text(x+char_size*2+len(formula)*char_size, y, text='d', font=('Calibri', int(char_size*3/2)))
    pcanv.create_text(x+char_size*2+(len(formula)+1)*char_size, y, text=diff, font=('Calibri', int(char_size*3/2)))


def Differential(pcanv, x, y, low, up, formula, diff, char_size=8):
    pass


if __name__ == '__main__':
    import tkinter as tk
    from Elecpy.GUIElements import *
    root = tk.Tk()
    root.geometry('1400x800')
    bcanvas = ScrollCanvas(master=root, row=0, column=0, cav_width=2000, cav_height=1000, grid=None).canvas
    Integral(bcanvas, 100, 100, 0, 5, 'x^2+5*x+sqrt(x)', 'x', char_size=15)
    root.mainloop()
