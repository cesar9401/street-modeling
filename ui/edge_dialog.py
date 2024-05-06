from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QLabel, QSpinBox, QPushButton, QDesktopWidget

from model.edge import Edge
from model.node import Node


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
