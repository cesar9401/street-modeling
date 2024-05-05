import math
import sys
from typing import List

import networkx as nx
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QGridLayout, QVBoxLayout, QGroupBox, QPushButton, QApplication, \
    QStyleFactory, QComboBox, QLabel, QDialog, QSpinBox, QHBoxLayout, QDoubleSpinBox, QSpacerItem, QSizePolicy, \
    QFileDialog
from matplotlib import pyplot as plt
from matplotlib.backend_tools import Cursors
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from geneticalgorithm.genetic_algorithm import GeneticAlgorithm
from model.edge import Edge
from model.node import Node

from persistence import persistence_util


class EdgeDialog(QDialog):
    def __init__(self, current_nodes: List[Node], from_node: Node, to_node: Node, cur_edge: Edge | None):
        super().__init__()
        self.current_nodes: List[Node] = current_nodes
        self.cur_edge: Edge | None = cur_edge
        self.from_node: Node = from_node
        self.to_node: Node = to_node

        self.setWindowTitle('Add edge')
        self.setGeometry(100, 100, 300, 300)
        general_layout = QVBoxLayout()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)

        # from
        self.combo1 = QComboBox()
        self.combo1.addItems(map(lambda x: x.label, current_nodes))
        layout.addWidget(QLabel('Node from'))
        layout.addWidget(self.combo1)
        if from_node:
            self.combo1.setCurrentIndex(self.combo1.findText(from_node.label))

        # to
        self.combo2 = QComboBox()
        self.combo2.addItems(map(lambda x: x.label, current_nodes))
        layout.addWidget(QLabel('Node to'))
        layout.addWidget(self.combo2)
        if to_node:
            self.combo2.setCurrentIndex(self.combo2.findText(to_node.label))

        # capacity
        self.capacity = QSpinBox()
        self.capacity.setRange(0, 2147483647)
        layout.addWidget(QLabel("Max capacity"))
        layout.addWidget(self.capacity)
        if cur_edge:
            self.capacity.setValue(cur_edge.capacity)

        general_layout.addLayout(layout)

        # btn
        save_btn = QPushButton('Save')
        save_btn.setObjectName("save_btn")
        save_btn.clicked.connect(self.on_save_btn_clicked)
        general_layout.addWidget(save_btn)
        self.setLayout(general_layout)

        # set center
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_save_btn_clicked(self):
        from_node: Node = next(item for item in self.current_nodes if item.label == self.combo1.currentText())
        to_node: Node = next(item for item in self.current_nodes if item.label == self.combo2.currentText())
        capacity: int = self.capacity.value()

        if not from_node or not to_node or capacity is None:
            return

        if from_node.id == to_node.id:
            return

        label = f'{from_node.label}->{to_node.label}'
        if not self.cur_edge:
            self.cur_edge = Edge(label, from_node, to_node, capacity)
        else:
            self.cur_edge.label = label
            self.cur_edge.from_node = from_node
            self.cur_edge.to_node = to_node
            self.cur_edge.capacity = self.capacity.value()

        print(f'edge: {self.cur_edge}, capacity: {self.cur_edge.capacity}')
        self.close()


class GraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.total_nodes: int = 0
        self.current_nodes: List[Node] = []
        self.current_edges: List[Edge] = []
        self.selected_node_color: str = '#FF5621'
        self.population_size: int = 100
        self.mutations_quantity: int = 1
        self.mutations_generations_quantity: int = 1
        self.completion_criteria_items = ['Number of generations', 'Efficiency percentage']
        self.completion_criteria_value = 100

        self.G = nx.DiGraph()
        self.figure = plt.figure(figsize=(10, 10), dpi=80)
        self.canvas = FigureCanvas(self.figure)

        self.selected_node: Node | None = None  # node to move
        self.from_node: Node | None = None  # to add edge, from node
        self.to_node: Node | None = None  # to add edge, to node

        # canvas events
        self.canvas.mpl_connect('button_press_event', self.on_press_add_node)
        self.canvas.mpl_connect('motion_notify_event', self.on_press_move_node)
        self.canvas.mpl_connect('button_release_event', self.on_release_button)

        self.adding_aux_node = False
        self.adding_node = False
        self.adding_edge = False

        self.setGeometry(100, 100, 1100, 800)
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

        # open and save button
        # open
        self.open_btn = QPushButton('Open')
        self.open_btn.setObjectName('open_btn')
        self.open_btn.clicked.connect(self.open_action)
        layout.addWidget(self.open_btn)

        # save
        self.save_btn = QPushButton('Save')
        self.save_btn.setObjectName('save_btn')
        self.save_btn.clicked.connect(self.save_action)
        layout.addWidget(self.save_btn)

        layout.addSpacerItem(QSpacerItem(0, 50, QSizePolicy.Minimum, QSizePolicy.Minimum))

        # add aux node button here
        self.add_aux_node_btn = QPushButton('Aux Node')
        self.add_aux_node_btn.setObjectName('add_aux_node_button')
        self.add_aux_node_btn.clicked.connect(self.add_aux_node)
        layout.addWidget(self.add_aux_node_btn)

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

        # edit edge button
        self.edit_edge_button = QPushButton('Edit Edge')
        self.edit_edge_button.setObjectName('edit_edge_button')
        self.edit_edge_button.clicked.connect(self.edit_edge)
        layout.addWidget(self.edit_edge_button)

        # remove edge button
        self.remove_edge_button = QPushButton('Remove Edge')
        self.remove_edge_button.setObjectName('remove_edge_button')
        self.remove_edge_button.clicked.connect(self.remove_edge)
        layout.addWidget(self.remove_edge_button)

        # reset button
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setObjectName("reset_button")
        self.reset_btn.clicked.connect(self.reset_action)
        layout.addWidget(self.reset_btn)

        # about the algorithm
        layout.addSpacerItem(QSpacerItem(0, 50, QSizePolicy.Minimum, QSizePolicy.Minimum))
        layout.addWidget(QLabel("About the algorithm"))

        # size population here
        self.population_size_spin = QSpinBox()
        self.population_size_spin.setRange(1, 2147483647)
        self.population_size_spin.setValue(self.population_size)
        layout.addWidget(QLabel('Size population'))
        layout.addWidget(self.population_size_spin)

        # mutations per population
        layout.addWidget(QLabel('X mutations / Y generations'))
        horizontal_layout = QHBoxLayout()

        self.mutations_quantity_spin = QSpinBox()
        self.mutations_quantity_spin.setRange(0, 2147483647)
        self.mutations_quantity_spin.setValue(self.mutations_quantity)

        self.mutations_generations_quantity_spin = QSpinBox()
        self.mutations_generations_quantity_spin.setRange(1, 2147483647)
        self.mutations_generations_quantity_spin.setValue(self.mutations_generations_quantity)

        horizontal_layout.addWidget(self.mutations_quantity_spin)
        horizontal_layout.addWidget(self.mutations_generations_quantity_spin)
        layout.addLayout(horizontal_layout)

        # completion criteria
        self.completion_criteria_combo = QComboBox()
        self.completion_criteria_combo.addItems(self.completion_criteria_items)
        layout.addWidget(QLabel('Completion criteria'))
        layout.addWidget(self.completion_criteria_combo)

        self.completion_criteria_spin = QDoubleSpinBox()
        self.completion_criteria_spin.setRange(1, 2147483647)
        self.completion_criteria_spin.setValue(self.completion_criteria_value)
        layout.addWidget(self.completion_criteria_spin)

        # start algorithm button
        self.start_algorithm_btn = QPushButton("Start")
        self.start_algorithm_btn.setObjectName('start_algorithm')
        self.start_algorithm_btn.clicked.connect(self.start_algorithm)
        layout.addWidget(self.start_algorithm_btn)

        # stop algorithm button
        self.stop_algorithm_btn = QPushButton("Stop")
        self.stop_algorithm_btn.setObjectName('stop_algorithm')
        self.stop_algorithm_btn.clicked.connect(self.stop_algorithm)
        layout.addWidget(self.stop_algorithm_btn)

        # add button layout
        self.grid.addLayout(self.button_layout, 0, 0)

        # add canvas
        self.grid.addWidget(self.canvas, 0, 1, 9, 9)
        plt.autoscale(enable=False)
        plt.axis('on')
        plt.title('Demo IA')

    def set_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_press_add_node(self, event):
        self.selected_node = None  # selected node is none
        pos_x, pos_y = event.xdata, event.ydata  # get position of the cursor

        if pos_x is None or pos_y is None:
            return

        # add edge
        if self.adding_edge:
            # select node here
            for node in self.current_nodes:
                if abs(node.pos_x - pos_x) < 0.009 and abs(node.pos_y - pos_y) < 0.009:
                    if not self.from_node:
                        self.from_node = node
                        self.draw_digraph()
                    elif not self.to_node and node.id != self.from_node.id:
                        self.to_node = node
                        self.draw_digraph()

                        # not allow when both nodes are aux nodes
                        if self.from_node.in_or_out and self.to_node.in_or_out:
                            self.from_node = None
                            self.to_node = None
                            self.draw_digraph()
                            return

                        # adding edge info here
                        new_edge = self.edit_edge_action()
                        self.current_edges.append(new_edge)
                        self.from_node = None
                        self.to_node = None
                        self.draw_digraph()
                        return
            return

        # add nodes
        if self.adding_node or self.adding_aux_node:
            # add node here
            self.total_nodes += 1
            tmp_node = Node(f'{self.total_nodes}')
            tmp_node.pos_x = float(pos_x)
            tmp_node.pos_y = float(pos_y)

            if self.adding_aux_node:
                tmp_node.in_or_out = True
                tmp_node.color = '#FDFEFE'

            self.current_nodes.append(tmp_node)
            self.draw_digraph()
            return

        # select node to move here
        if pos_x is None or pos_y is None:
            return

        for node in self.current_nodes:
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

    def open_action(self):
        dlg = QFileDialog()
        dlg.setAcceptMode(QFileDialog.AcceptOpen)
        dlg.setFileMode(QFileDialog.ExistingFiles)
        if dlg.exec_() != QDialog.Accepted:
            return

        filename = dlg.selectedFiles()[0]
        if not filename:
            return

        wrapper = persistence_util.load_from_file(filename)
        if not wrapper:
            print('no info loaded')
            return

        self.reset_action()
        self.current_nodes = wrapper.nodes
        self.current_edges = wrapper.edges
        self.draw_digraph()

    def save_action(self):
        save_file_info = QFileDialog().getSaveFileName()
        if not save_file_info[0]:
            return

        filename = save_file_info[0] + '.pkl'
        saved = persistence_util.save_to_file(self.current_nodes, self.current_edges, filename)
        print(f'saved: {saved}')

    def add_aux_node(self):
        self.adding_aux_node = not self.adding_aux_node
        self.adding_node = False
        self.adding_edge = False
        self.update_buttons_colors()

    def add_node(self):
        self.adding_node = not self.adding_node
        self.adding_aux_node = False
        self.adding_edge = False
        self.update_buttons_colors()

    def remove_node(self):
        if not self.selected_node:
            return

        for edge in self.current_edges:
            if (edge.from_node and edge.from_node.id == self.selected_node.id) or (
                    edge.to_node and edge.to_node.id == self.selected_node.id):
                return

        self.current_nodes.remove(self.selected_node)  # remove node
        self.selected_node = None
        self.draw_digraph()  # draw, again

    def add_edge(self):
        self.adding_edge = not self.adding_edge
        self.adding_aux_node = False
        self.adding_node = False
        self.update_buttons_colors()

    # to remove any edge
    def remove_edge(self):
        index = self.edge_combo.currentIndex()
        if index != -1 and self.current_edges[index]:
            self.current_edges.remove(self.current_edges[index])
            self.draw_digraph()

    # to edit any edge
    def edit_edge(self):
        index = self.edge_combo.currentIndex()
        if index != -1 and self.current_edges[index]:
            cur_edge = self.current_edges[index]
            self.current_edges.remove(cur_edge)

            edit_dialog = EdgeDialog(self.current_nodes, cur_edge.from_node, cur_edge.to_node, cur_edge)
            edit_dialog.exec()
            new_edge = edit_dialog.cur_edge
            self.current_edges.append(new_edge)
            self.draw_digraph()

    def reset_action(self):
        self.total_nodes = 0
        self.current_nodes = []
        self.current_edges = []
        self.selected_node = None
        self.from_node = None
        self.to_node = None
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

        if self.adding_aux_node:
            self.add_aux_node_btn.setStyleSheet("background-color: #FF5722;")
        else:
            self.add_aux_node_btn.setStyleSheet("background-color: none;")

        if not self.adding_edge:
            self.from_node = None
            self.to_node = None
            self.draw_digraph()

    def edit_edge_action(self) -> Edge:
        edit_dialog = EdgeDialog(self.current_nodes, self.from_node, self.to_node, None)
        edit_dialog.exec()
        return edit_dialog.cur_edge

    def draw_digraph(self):
        plt.clf()
        plt.title('Demo IA')
        plt.axis('on')
        plt.autoscale(enable=False)
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
        edge_labels = {}
        for edge in self.current_edges:
            # combo to list edges
            self.edge_combo.addItem(f'{edge.from_node.label}->{edge.to_node.label}')
            self.G.add_edge(edge.from_node.label, edge.to_node.label)  # add edge to networkx
            edge_labels[(edge.from_node.label,
                         edge.to_node.label)] = f'{edge.from_node.label}{edge.to_node.label} ({edge.capacity})'

        pos = nx.get_node_attributes(self.G, 'pos')
        nx.draw_networkx(
            self.G, pos=pos, arrows=True, node_size=2500, alpha=0.85, node_color=color_map,
            with_labels=True
        )
        nx.draw_networkx_edge_labels(self.G, pos=pos, edge_labels=edge_labels)
        self.canvas.draw()

    def start_algorithm(self):
        print('Starting algorithm')
        self.population_size = int(self.population_size_spin.value())
        self.mutations_quantity = int(self.mutations_quantity_spin.value())
        self.mutations_generations_quantity = int(self.mutations_generations_quantity_spin.value())
        self.completion_criteria_value = float(self.completion_criteria_spin.value())
        completion_by_generations = self.completion_criteria_combo.currentText() == 'Number of generations'
        if completion_by_generations:
            self.completion_criteria_value = math.floor(self.completion_criteria_value)

        algorithm = GeneticAlgorithm(
            self.population_size,
            self.mutations_quantity,
            self.mutations_generations_quantity,
            completion_by_generations,
            self.completion_criteria_value,
            self.current_nodes, self.current_edges
        )
        best = algorithm.get_best_fitness()

    def stop_algorithm(self):
        pass


app = QApplication(sys.argv)
app.aboutToQuit.connect(app.deleteLater)
app.setStyle(QStyleFactory.create("gtk"))
window = GraphWidget()
window.show()
sys.exit(app.exec_())
