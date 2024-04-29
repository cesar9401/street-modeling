import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QStyleFactory, QWidget, QDesktopWidget, QGridLayout, QGroupBox, QVBoxLayout, \
    QPushButton
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class GraphWidget(QWidget):
    def __init__(self):
        super(GraphWidget, self).__init__()
        font = QFont()
        font.setPointSize(16)
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 1000, 800)
        self.set_center()
        self.setWindowTitle("IA")

        grid = QGridLayout()
        self.setLayout(grid)

        button_layout = self.create_buttons()

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        grid.addLayout(button_layout, 0, 0)
        grid.addWidget(self.canvas, 0, 1, 9, 9)

    def set_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_buttons(self):
        button_layout = QVBoxLayout()
        vertical_group_box = QGroupBox()

        layout = QVBoxLayout()

        add_node_btn = QPushButton("Add Node")
        add_node_btn.setObjectName("add_node_btn")
        add_node_btn.clicked.connect(self.submit_command)

        layout.addWidget(add_node_btn)
        layout.setSpacing(10)

        vertical_group_box.setLayout(layout)
        button_layout.addWidget(vertical_group_box)
        return button_layout

    def submit_command(self):
        print('Submitted command', self.sender().objectName())


app = QApplication(sys.argv)
app.aboutToQuit.connect(app.deleteLater)
app.setStyle(QStyleFactory.create("gtk"))

window = GraphWidget()
window.show()

sys.exit(app.exec_())
