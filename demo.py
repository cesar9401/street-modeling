import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication


class Node:
    def __init__(self, label, pos_x=0, pos_y=0):
        self.label = label
        self.pos_x = pos_x
        self.pos_y = pos_y


class GraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.total_nodes = 0
        self.nodes = []
        self.G = nx.DiGraph()

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

        self.canvas.mpl_connect('button_press_event', self.on_press)

    def on_press(self, event):
        print('press event', event)
        pos_x, pos_y = event.xdata, event.ydata
        print(f'pos_x: {pos_x}, pos_y: {pos_y}')
        if pos_x is not None and pos_y is not None:
            self.total_nodes += 1
            tmp_node = Node(f'{self.total_nodes}', pos_x, pos_y)
            self.nodes.append(tmp_node)
            self.G.add_node(tmp_node.label, pos=(tmp_node.pos_x, tmp_node.pos_y))
            self.draw_graph()
            print(f'total: {self.total_nodes}')

    def draw_graph(self):
        plt.clf()
        pos = nx.get_node_attributes(self.G, 'pos')
        nx.draw_networkx(self.G, pos=pos, arrows=True, node_size=2500, alpha=0.85, node_color='c', with_labels=True)
        self.canvas.draw()


app = QApplication([])
graph_widget = GraphWidget()
graph_widget.show()
app.exec_()
