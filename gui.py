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

        g = make_network()
        node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in g.nodes(data=True)}
        edge_col = [e[2]['attr_dict']['color'] for e in g.edges(data=True)]
        nx.draw_networkx(g, pos=node_pos, arrows=True, edge_color=edge_col, node_size=2200, alpha=.85, node_color='c',
                         with_labels=True)
        labels = nx.get_edge_attributes(g, 'num_connections')
        nx.draw_networkx_edge_labels(g, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
        plt.title('Matt\'s Life', size=15)
        plt.axis("off")


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


def make_network():
    # Load Data
    df = pd.read_csv("matt_test_network.csv")
    # automate using predictions for full scale version
    color = pd.DataFrame(
        data=['silver'] * len(df.index))
    df['color'] = color
    g = nx.DiGraph()

    # Add edges into network
    for i, elrow in df.iterrows():
        g.add_edge(elrow.iloc[0], elrow.iloc[1], attr_dict=elrow[2:].to_dict(), weight=1 / elrow['num_connections'])

    # Manually add X and Y coords of nodes
    nodeList = {'NodeName': ['home', 'ht', 'work', 'daycare', 'coffee'], 'X': [70, 405, 835, 300, 750],
                'Y': [250, 300, 240, 450, 510]}
    nodeFrame = pd.DataFrame(data=nodeList)
    # add node properties
    for i, nlrow in nodeFrame.iterrows():
        g._node[nlrow.iloc[0]] = nlrow[1:].to_dict()

    return g


app = QApplication(sys.argv)
app.aboutToQuit.connect(app.deleteLater)
app.setStyle(QStyleFactory.create("gtk"))

window = GraphWidget()
window.show()

sys.exit(app.exec_())
