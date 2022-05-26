import os
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PyQt5.QtGui import *
from wordCreate import wordcreate


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
        self.setWindowTitle('Comments Detector')

    def ok_btn_click(self):
        self.hide()                     # 메인윈도우 숨김
        self.url = self.textEdit.toPlainText()
        self.second = secondwindow(self.url)    #
        self.second.exec()              # 두번째 창을 닫을 때 까지 기다림
        self.show()                     # 두번째 창을 닫으면 다시 첫 번째 창이 보여짐짐

class secondwindow(QDialog,QWidget,form_secondwindow):
    def __init__(self, url):
        super(secondwindow,self).__init__()
        self.initUi()
        self.show()


        self.read_data()
        self.draw_canvas()
        self.createWordcloud()
        self.setPhoto()

    def createWordcloud(self):
         self.worldcloud = wordcreate()
         self.worldcloud.create()

    def setPhoto(self):
        self.picture = QPixmap()
        self.picture.load('word.png')
        self.picture = self.picture.scaled(700, 300)
        self.photo.setPixmap(self.picture)

    def initUi(self):
        self.setupUi(self)
        self.setWindowTitle('Result')

    def return_click(self):
        self.close()

    def draw_canvas(self):
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.small_graph.addWidget(self.canvas)

        self.ax = self.fig.add_subplot(111)

        self.x = [1, 2]
        self.y = [self.good_len, self.bad_len]
        self.label = ['Good', 'Bad']
        self.ax.barh(self.x, self.y, tick_label=self.label)
        self.ax.set_title("Ratio of malicious comments")

        self.canvas.draw()

    def read_data(self):
        self.data = pd.read_excel('total.xlsx', index_col=0)
        self.data = self.data.dropna(axis=0)

        self.good = self.data[self.data['react'] == '긍정']
        self.good_len = len(self.good)
        self.bad = self.data[self.data['react'] == '부정']
        self.bad_len = len(self.bad)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()