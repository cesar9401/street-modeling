import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QStyleFactory, QWidget, QDesktopWidget, QGridLayout, QGroupBox, QVBoxLayout, \
    QPushButton
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class GraphWidget(QWidget):
    total_nodes = 1
    adding_node = False
    add_node_button = None

    def __init__(self):
        super(GraphWidget, self).__init__()
        self.figure = None
        self.canvas = None
        self.G = None

        font = QFont()
        font.setPointSize(16)
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 1000, 800)
        self.set_center()
        self.setWindowTitle("IA")

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        # add buttons here
        button_layout = self.create_buttons()
        self.grid.addLayout(button_layout, 0, 0)

        # canvas
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.grid.addWidget(self.canvas, 0, 1, 9, 9)

        self.canvas.mpl_connect('button_press_event', self.on_press)

        self.G = self.make_network()

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
        self.add_node_btn = QPushButton("Add Node")
        self.add_node_btn.setObjectName("add_node_btn")
        self.add_node_btn.clicked.connect(self.add_node)
        layout.addWidget(self.add_node_btn)

        # add edge button
        add_edge_btn = QPushButton("Add Edge")
        add_edge_btn.setObjectName("add_edge_btn")
        add_edge_btn.clicked.connect(self.add_edge)
        layout.addWidget(add_edge_btn)

        # remove object button
        remove_object_btn = QPushButton("Remove Object")
        remove_object_btn.setObjectName("remove_object_btn")
        remove_object_btn.clicked.connect(self.submit_command)
        layout.addWidget(remove_object_btn)

        return button_layout

    def submit_command(self):
        print('Submitted command', self.sender().objectName())

    def add_node(self):
        self.adding_node = not self.adding_node
        if self.adding_node:
            self.add_node_btn.setStyleSheet("background-color: #FF5722;")
        else:
            self.add_node_btn.setStyleSheet("background-color: none;")

        # print('Submitted command', self.sender().objectName())
        # self.figure = plt.figure()
        # self.canvas = FigureCanvas(self.figure)
        #
        # self.grid.addWidget(self.canvas, 0, 1, 9, 9)
        #
        # self.G.add_node('node3', pos=(200, 300))
        #
        # pos = nx.get_node_attributes(self.G, 'pos')
        #
        # # plt.clf()
        # plt.title('Demo')
        # plt.axis('off')
        #
        # nx.draw_networkx(self.G, pos=pos, arrows=True, node_size=2500, alpha=0.85, node_color='c', with_labels=True)
        #
        # nx.draw_networkx_edge_labels(
        #     self.G, pos=pos, edge_labels={('node1', 'node2'): 'A(100)'}, font_color='black', alpha=0.2
        # )

    def add_edge(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.grid.addWidget(self.canvas, 0, 1, 9, 9)

        self.G.add_edge('node1', 'node3', label='B(50)')

        pos = nx.get_node_attributes(self.G, 'pos')

        # plt.clf()
        plt.title('Demo')
        plt.axis('off')

        nx.draw_networkx(self.G, pos=pos, arrows=True, node_size=2500, alpha=0.85, node_color='c', with_labels=True)

        nx.draw_networkx_edge_labels(
            self.G, pos=pos, edge_labels={('node1', 'node2'): 'A(100)'}, font_color='black', alpha=0.2
        )

    def make_network(self):
        g = nx.DiGraph()
        g.add_node('node1', pos=(100, 100))
        g.add_node('node2', pos=(200, 100))
        g.add_edge('node1', 'node2', label='A(100)')

        pos = nx.get_node_attributes(g, 'pos')
        nx.draw_networkx(g, pos=pos, arrows=True, node_size=2500, alpha=0.85, node_color='c', with_labels=True)

        nx.draw_networkx_edge_labels(
            g, pos=pos, edge_labels={('node1', 'node2'): 'A(100)'}, font_color='black', alpha=0.2
        )
        plt.title('Demo')
        plt.axis('off')

        return g

    def on_press(self, event):
        if not self.adding_node:
            return

        # TODO: add the node here
        print("press")
        print("event.xdata", event.xdata)
        print("event.ydata", event.ydata)
        print("event.inaxes", event.inaxes)
        print("x", event.x)
        print("y", event.y)


app = QApplication(sys.argv)
app.aboutToQuit.connect(app.deleteLater)
app.setStyle(QStyleFactory.create("gtk"))

window = GraphWidget()
window.show()

sys.exit(app.exec_())
