import sys
from typing import List

import networkx as nx
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QGridLayout, QVBoxLayout, QGroupBox, QPushButton, QApplication, \
    QStyleFactory, QComboBox, QLabel
from matplotlib import pyplot as plt
from matplotlib.backend_tools import Cursors
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from model.edge import Edge
from model.node import Node


class GraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.total_nodes: int = 0
        self.current_nodes: List[Node] = []
        self.current_edges: List[Edge] = []
        self.selected_node_color: str = '#FF5621'

        self.G = nx.DiGraph()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.selected_node: Node | None = None  # node to move
        self.from_node: Node | None = None  # to add edge, from node
        self.to_node: Node | None = None  # to add edge, to node

        # canvas events
        self.canvas.mpl_connect('button_press_event', self.on_press_add_node)
        self.canvas.mpl_connect('motion_notify_event', self.on_press_move_node)
        self.canvas.mpl_connect('button_release_event', self.on_release_button)

        self.adding_node = False
        self.adding_edge = False

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

        # remove node button
        self.remove_node_btn = QPushButton('Remove Node')
        self.remove_node_btn.setObjectName('remove_node_btn')
        self.remove_node_btn.clicked.connect(self.remove_node)
        layout.addWidget(self.remove_node_btn)

        # add edge button
        self.add_edge_btn = QPushButton('Add Edge')
        self.add_edge_btn.setObjectName('add_edge_btn')
        self.add_edge_btn.clicked.connect(self.add_edge)
        layout.addWidget(self.add_edge_btn)

        # add edge list
        self.edge_combo = QComboBox()
        layout.addWidget(QLabel('Edges'))
        layout.addWidget(self.edge_combo)

        # remove edge button
        self.remove_edge_button = QPushButton('Remove Edge')
        self.remove_edge_button.setObjectName('remove_edge_button')
        self.remove_edge_button.clicked.connect(self.remove_edge)
        layout.addWidget(self.remove_edge_button)

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

        if pos_x is None or pos_y is None:
            return

        # add edge
        if self.adding_edge:
            # TODO: select node here
            for node in self.current_nodes:
                if abs(node.pos_x - pos_x) < 0.009 and abs(node.pos_y - pos_y) < 0.009:
                    if not self.from_node:
                        self.from_node = node
                        self.draw_digraph()
                    elif not self.to_node and node.id != self.from_node.id:
                        self.to_node = node

                        # TODO: add edge here
                        self.draw_digraph()

                        new_edge = Edge(f'{self.from_node.label}-{self.to_node.label}', self.from_node, self.to_node, 0)
                        self.current_edges.append(new_edge)

                        self.from_node = None
                        self.to_node = None
                        self.draw_digraph()
                        return
            return

        # add nodes
        if self.adding_node:
            # add node here
            self.total_nodes += 1
            tmp_node = Node(f'{self.total_nodes}')
            tmp_node.pos_x = float(pos_x)
            tmp_node.pos_y = float(pos_y)
            self.current_nodes.append(tmp_node)

            # self.G.add_node(tmp_node.label, pos=(tmp_node.pos_x, tmp_node.pos_y))
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
                self.draw_digraph()
                return

        self.selected_node = None
        self.draw_digraph()

    def on_press_move_node(self, event):
        pos_x, pos_y = event.xdata, event.ydata
        if pos_x is None or pos_y is None:
            return

        if event.button == Qt.LeftButton and self.selected_node is not None:
            self.selected_node.pos_x = float(pos_x)
            self.selected_node.pos_y = float(pos_y)
            self.draw_digraph()

    def on_release_button(self, event):
        self.canvas.set_cursor(Cursors.POINTER)

    def add_node(self):
        self.adding_node = not self.adding_node
        self.adding_edge = False
        self.update_buttons_colors()

    def remove_node(self):
        if not self.selected_node:
            return

        for edge in self.current_edges:
            if (edge.from_node and edge.from_node.id == self.selected_node.id) or (edge.to_node and edge.to_node.id == self.selected_node.id):
                return

        self.current_nodes.remove(self.selected_node)  # remove node
        self.selected_node = None
        self.draw_digraph()  # draw, again

    def add_edge(self):
        self.adding_edge = not self.adding_edge
        self.adding_node = False
        self.update_buttons_colors()

    def remove_edge(self):
        index = self.edge_combo.currentIndex()
        if index != -1 and self.current_edges[index]:
            self.current_edges.remove(self.current_edges[index])
            self.draw_digraph()

    def update_buttons_colors(self):
        if self.adding_node:
            self.add_node_btn.setStyleSheet("background-color: #FF5722;")
        else:
            self.add_node_btn.setStyleSheet("background-color: none;")

        if self.adding_edge:
            self.add_edge_btn.setStyleSheet("background-color: #FF5722;")
        else:
            self.add_edge_btn.setStyleSheet("background-color: none;")

        if not self.adding_edge:
            self.from_node = None
            self.to_node = None
            self.draw_digraph()

    def draw_digraph(self):
        plt.clf()
        self.G.clear()
        color_map: List[str] = []

        for node in self.current_nodes:
            self.G.add_node(node.label, pos=(node.pos_x, node.pos_y))
            if self.selected_node and self.selected_node.id == node.id:
                color_map.append(self.selected_node_color)
            elif self.to_node and self.to_node.id == node.id:
                color_map.append(self.selected_node_color)
            elif self.from_node and self.from_node.id == node.id:
                color_map.append(self.selected_node_color)
            else:
                color_map.append(node.color)

        self.edge_combo.clear()
        for edge in self.current_edges:
            self.edge_combo.addItem(f'{edge.from_node.label}->{edge.to_node.label}')
            self.G.add_edge(edge.from_node.label, edge.to_node.label)

        pos = nx.get_node_attributes(self.G, 'pos')
        nx.draw_networkx(self.G, pos=pos, arrows=True, node_size=2500, alpha=0.85, node_color=color_map,
                         with_labels=True)
        plt.autoscale(enable=False)
        self.canvas.draw()


app = QApplication(sys.argv)
app.aboutToQuit.connect(app.deleteLater)
app.setStyle(QStyleFactory.create("gtk"))

window = GraphWidget()
window.show()

sys.exit(app.exec_())
