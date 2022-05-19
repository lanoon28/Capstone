import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QDesktopWidget, QDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class start(QMainWindow):
    def __init__(self):
        super().__init__()

class result(QDialog,QWidget):

    def __init__(self):
        super().__init__()
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        canvas = FigureCanvas(Figure(figsize=(4, 3)))
        vbox = QVBoxLayout(self.main_widget)
        vbox.addWidget(canvas)

        self.addToolBar(NavigationToolbar(canvas, self))

        self.ax = canvas.figure.subplots()
        self.ax.plot([0, 1, 2], [1, 5, 3], '-')

        self.setWindowTitle('Bad Comments Detecter')
        self.resize(600, 400)
        self.center()
        self.show()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = result()
   sys.exit(app.exec_())