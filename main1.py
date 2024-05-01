import sys
from typing import List

import networkx as nx
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QGridLayout, QVBoxLayout, QGroupBox, QPushButton, QApplication, \
    QStyleFactory
from matplotlib import pyplot as plt
from matplotlib.backend_tools import Cursors
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

        self.selected_node: Node | None = None

        # canvas events
        self.canvas.mpl_connect('button_press_event', self.on_press_add_node)
        self.canvas.mpl_connect('motion_notify_event', self.on_press_move_node)
        self.canvas.mpl_connect('button_release_event', self.on_release_button)

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

        # add node button
        self.add_node_btn = QPushButton('Add Node')
        self.add_node_btn.setObjectName('add_node_btn')
        self.add_node_btn.clicked.connect(self.add_node)
        layout.addWidget(self.add_node_btn)

        # add button layout
        self.grid.addLayout(self.button_layout, 0, 0)

        # add canvas
        self.grid.addWidget(self.canvas, 0, 1, 9, 9)
        plt.autoscale(enable=False)
        plt.title('Demo IA')

    def set_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_press_add_node(self, event):
        self.selected_node = None  # selected node is none
        pos_x, pos_y = event.xdata, event.ydata  # get position of the cursor
        print(f'Pos X: {pos_x}, Pos Y: {pos_y}')

        # add nodes
        if self.adding_node:
            if pos_x is None or pos_y is None:
                return

            # add node here
            self.total_nodes += 1
            tmp_node = Node(f'{self.total_nodes}')
            tmp_node.pos_x = float(pos_x)
            tmp_node.pos_y = float(pos_y)
            self.current_nodes.append(tmp_node)

            self.G.add_node(tmp_node.label, pos=(tmp_node.pos_x, tmp_node.pos_y))
            self.draw_digraph()
            return

        # select node to move here
        if pos_x is None or pos_y is None:
            return

        for node in self.current_nodes:
            print(node)
            if abs(node.pos_x - pos_x) < 0.009 and abs(node.pos_y - pos_y) < 0.009:
                self.selected_node = node
                self.canvas.set_cursor(Cursors.MOVE)
                print(f'selected node: {self.selected_node}')
                return

        self.selected_node = None

    def on_press_move_node(self, event):
        pos_x, pos_y = event.xdata, event.ydata
        if pos_x is None or pos_y is None:
            return

        if event.button == Qt.LeftButton and self.selected_node is not None:
            # self.canvas.set_cursor(Cursors.MOVE)
            self.selected_node.pos_x = float(pos_x)
            self.selected_node.pos_y = float(pos_y)
            self.G.remove_node(self.selected_node.label)
            self.G.add_node(self.selected_node.label, pos=(self.selected_node.pos_x, self.selected_node.pos_y))
            self.draw_digraph()

    def on_release_button(self, event):
        self.canvas.set_cursor(Cursors.POINTER)

    def add_node(self):
        self.adding_node = not self.adding_node
        self.update_buttons_colors()

    def update_buttons_colors(self):
        if self.adding_node:
            self.add_node_btn.setStyleSheet("background-color: #FF5722;")
        else:
            self.add_node_btn.setStyleSheet("background-color: none;")

    def draw_digraph(self):
        plt.clf()
        pos = nx.get_node_attributes(self.G, 'pos')
        nx.draw_networkx(self.G, pos=pos, arrows=True, node_size=2500, alpha=0.85, node_color='c', with_labels=True)
        plt.autoscale(enable=False)
        self.canvas.draw()


app = QApplication(sys.argv)
app.aboutToQuit.connect(app.deleteLater)
app.setStyle(QStyleFactory.create("gtk"))

window = GraphWidget()
window.show()

sys.exit(app.exec_())
