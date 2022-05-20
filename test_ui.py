import os
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('home.ui')
form_class = uic.loadUiType(form)[0]

form_second = resource_path('result_end.ui')
form_secondwindow = uic.loadUiType(form_second)[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def ok_btn_click(self):
        self.hide()                     # 메인윈도우 숨김
        self.second = secondwindow()    #
        self.second.exec()              # 두번째 창을 닫을 때 까지 기다림
        self.show()                     # 두번째 창을 닫으면 다시 첫 번째 창이 보여짐짐

class secondwindow(QDialog,QWidget,form_secondwindow):
    def __init__(self):
        super(secondwindow,self).__init__()
        self.initUi()
        self.show()
        data = pd.read_excel('total.xlsx', index_col=0)

        # 결측치 드랍
        data = data.dropna(axis=0)

        print('data : ', len(data))

        good = data[data['react'] == '긍정']
        good_len = len(good)


        bad = data[data['react'] == '부정']
        bad_len = len(bad)


        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.small_graph.addWidget(self.canvas)

        ax = self.fig.add_subplot(111)

        x = [1,2]
        y = [good_len,bad_len]
        label = ['positive', 'negative']
        ax.barh(x,y,tick_label =label)

        ax.set_title("positive negative ratio")

        self.canvas.draw()

    def initUi(self):
        self.setupUi(self)

    def return_click(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()