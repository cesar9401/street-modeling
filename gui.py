import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QStyleFactory, QWidget, QDesktopWidget, QGridLayout, QGroupBox, QVBoxLayout, \
    QPushButton
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
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

        # add buttons here
        button_layout = self.create_buttons()
        grid.addLayout(button_layout, 0, 0)

        # canvas
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas, 0, 1, 9, 9)

        self.make_network()

    def set_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_buttons(self):
        button_layout = QVBoxLayout()
        vertical_group_box = QGroupBox()
        button_layout.addWidget(vertical_group_box)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        vertical_group_box.setLayout(layout)

        # add node button
        add_node_btn = QPushButton("Add Node")
        add_node_btn.setObjectName("add_node_btn")
        add_node_btn.clicked.connect(self.submit_command)
        layout.addWidget(add_node_btn)

        # add edge button
        add_edge_btn = QPushButton("Add Edge")
        add_edge_btn.setObjectName("add_edge_btn")
        add_edge_btn.clicked.connect(self.submit_command)
        layout.addWidget(add_edge_btn)

        # remove object button
        remove_object_btn = QPushButton("Remove Object")
        remove_object_btn.setObjectName("remove_object_btn")
        remove_object_btn.clicked.connect(self.submit_command)
        layout.addWidget(remove_object_btn)

        return button_layout

    def submit_command(self):
        print('Submitted command', self.sender().objectName())

    def make_network(self):
        g = nx.DiGraph()
        g.add_node('node1', pos=(100, 100))
        g.add_node('node2', pos=(200, 100))
        g.add_node('node3', pos=(400, 100))
        g.add_edge('node1', 'node2', label='A(100)')

        pos = nx.get_node_attributes(g, 'pos')
        nx.draw_networkx(g, pos=pos, arrows=True, node_size=2500, alpha=0.85, node_color='c', with_labels=True)

        nx.draw_networkx_edge_labels(
            g, pos=pos, edge_labels={('node1', 'node2'): 'A(100)'}, font_color='black', alpha=0.2
        )
        plt.title('Demo')
        plt.axis('off')


app = QApplication(sys.argv)
app.aboutToQuit.connect(app.deleteLater)
app.setStyle(QStyleFactory.create("gtk"))

window = GraphWidget()
window.show()

sys.exit(app.exec_())
