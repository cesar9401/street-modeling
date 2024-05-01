import sys
from typing import List

import networkx as nx
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QGridLayout, QVBoxLayout, QGroupBox, QPushButton, QApplication, \
    QStyleFactory
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from model.node import Node


class GraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.total_nodes: int = 0
        self.current_nodes: List[Node] = []
        self.G = nx.DiGraph()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # canvas events
        self.canvas.mpl_connect('button_press_event', self.on_press_add_node)

        self.adding_node = False

        self.setGeometry(100, 100, 1000, 800)
        self.set_center()
        self.setWindowTitle("IA")
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        # buttons here
        self.button_layout = QVBoxLayout()
        vertical_group_box = QGroupBox()
        self.button_layout.addWidget(vertical_group_box)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        vertical_group_box.setLayout(layout)

        self.add_node_btn = QPushButton("Add Node")
        self.add_node_btn.setObjectName("add_node_btn")
        self.add_node_btn.clicked.connect(self.add_node)
        layout.addWidget(self.add_node_btn)

        # add button layou
        self.grid.addLayout(self.button_layout, 0, 0)

        # add canvas
        self.grid.addWidget(self.canvas, 0, 1, 9, 9)

        plt.title('Demo IA')

    def set_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_press_add_node(self, event):
        print(event)
        if not self.adding_node:
            return

        # TODO: add node here
        pos_x, pos_y = event.xdata, event.ydata
        self.total_nodes += 1
        tmp_node = Node(f'{self.total_nodes}')
        tmp_node.pos_x = int(pos_x)
        tmp_node.pos_y = int(pos_y)
        self.current_nodes.append(tmp_node)

        self.G.add_node(tmp_node.label, pos=(pos_x, pos_y))
        self.draw_digraph()

    def add_node(self):
        self.adding_node = not self.adding_node
        if self.adding_node:
            self.add_node_btn.setStyleSheet("background-color: #FF5722;")
        else:
            self.add_node_btn.setStyleSheet("background-color: none;")

    def draw_digraph(self):
        plt.clf()
        pos = nx.get_node_attributes(self.G, 'pos')
        nx.draw_networkx(self.G, pos=pos, arrows=True, node_size=2500, alpha=0.85, node_color='c', with_labels=True)
        self.canvas.draw()


app = QApplication(sys.argv)
app.aboutToQuit.connect(app.deleteLater)
app.setStyle(QStyleFactory.create("gtk"))

window = GraphWidget()
window.show()

sys.exit(app.exec_())
