# https://predictivehacks.com/feature-importance-in-python/
# https://www.naukri.com/learning/articles/feature-selection-techniques-python-code/
# https://stackoverflow.com/questions/72467117/how-to-find-which-features-are-responsible-for-predicted-label
# https://stackoverflow.com/questions/35249760/using-scikit-to-determine-contributions-of-each-feature-to-a-specific-class-pred
# https://www.google.com/search?q=how+to+know+each+feature+has+the+most+impact+when+model+predict&client=ubuntu&hs=SM9&channel=fs&sxsrf=AJOqlzUe5VcPIMBl2DpB6wYqx1WbuEfgsg%3A1674592123821&ei=ez_QY_HQMcPgkdUP9eiZ4As&ved=0ahUKEwix-rvlheH8AhVDcKQEHXV0BrwQ4dUDCA4&uact=5&oq=how+to+know+each+feature+has+the+most+impact+when+model+predict&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzoKCAAQRxDWBBCwAzoFCCEQoAE6BAghEBU6CggAEB4QogQQiwNKBAhBGABKBAhGGABQlSVY40VgnUdoA3ABeACAAa8BiAGpEpIBBDMuMTaYAQCgAQHIAQi4AQLAAQE&sclient=gws-wiz-serp


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, QTime
import pyqtgraph as pg
from random import randint

class App(QWidget):

    def __init__(self):
        super().__init__()

        self.title = 'WBG Fusion'
        self.left = 0
        self.top = 0
        self.width = 1280
        self.height = 764
        self.button_start = None
        self.button_audio = None
        self.button_velocity = None
        self.button_temperature = None
        self.graphWidget = None
        self.motor_status = None

        self.init_ui_buttons()
        self.init_ui_graph()

    def init_ui_buttons(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # changing the background color to cyan
        self.setStyleSheet("background-color: #E3e6e6;")

        self.button_start = QPushButton('Start Acquiring data', self)
        self.button_start.move(1000, 70)
        self.button_start.clicked.connect(self.on_click_start)

        self.button_temperature = QPushButton('Simulate temperature changing', self)
        self.button_temperature.move(1000, 120)
        self.button_temperature.clicked.connect(self.on_click_temperature)

        self.button_velocity = QPushButton('Simulate velocity changing', self)
        self.button_velocity.move(1000, 170)
        self.button_velocity.clicked.connect(self.on_click_velocity)

        self.button_audio = QPushButton('Simulate audio changing', self)
        self.button_audio.move(1000, 220)
        self.button_audio.clicked.connect(self.on_click_audio)

        # creating a label widget
        # by default label will display at top left corner
        s = 'ok'
        self.motor_status = QLabel(f'Motor Status is: \n {s}', self)
        self.motor_status.move(1000, 300)
        self.motor_status.setStyleSheet("background-color: orange; border: 1pxsolidblack;")

        s = 'None'
        self.motor_failure = QLabel(f'Motor probable failure is: \n {s}', self)
        self.motor_failure.move(1000, 400)
        self.motor_failure.setStyleSheet("background-color: orange; border: 1pxsolidblack;")

    def init_ui_graph(self):
        self.graphWidget = pg.PlotWidget(self)
        self.graphWidget.setGeometry(10, 30, 900, 700)

        self.graphWidget.setTitle("Real time Sensors Graph")
        self.graphWidget.setBackground('w')
        self.x = list(range(100))  # 100 time points
        self.y = [randint(0, 100) for _ in range(100)]  # 100 data points

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)

        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append(randint(0, 100))  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.

    @pyqtSlot()
    def on_click_start(self):
        print('PyQt5 button click')

    @pyqtSlot()
    def on_click_temperature(self):
        print('PyQt5 button click')

    @pyqtSlot()
    def on_click_velocity(self):
        print('PyQt5 button click')

    @pyqtSlot()
    def on_click_audio(self):
        print('PyQt5 button click')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
