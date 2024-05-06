import sys
from typing import List

import graphviz
from PyQt5.QtWidgets import QApplication, QStyleFactory
from geneticalgorithm import generic_algorithm
from ui import main_widget

from model import node
from model import edge
from geneticalgorithm import individual


def print_results(nodes: List[node.Node], edges: List[edge.Edge], best: individual.Individual):
    dot = graphviz.Digraph(comment='Simple Genetic Algorithm')
    dot.attr(rankdir='LR')

    # add nodes to dot
    for tmp_node in nodes:
        if tmp_node.in_or_out:
            dot.node(tmp_node.id, tmp_node.label, pos=f'{tmp_node.pos_x * 10},{tmp_node.pos_y * 10}!', style='invis')
        else:
            dot.node(tmp_node.id, tmp_node.label, pos=f'{tmp_node.pos_x * 10},{tmp_node.pos_y * 10}!')

    for tmp_edge in edges:
        dot.edge(
            tmp_edge.from_node.id,
            tmp_edge.to_node.id,
            label=f'{tmp_edge.from_node.label}{tmp_edge.to_node.label}({tmp_edge.capacity})'
        )

    # TODO: add labels here
    dot.render('dot/sample.gv', engine='neato', view=True, format='png')


if __name__ == '__main__':
    print('hello there')
    # algorithm
    algorithm = generic_algorithm.GenericAlgorithm(print_results)

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    app.setStyle(QStyleFactory.create('gtk'))
    window = main_widget.MainWidget(algorithm)
    algorithm.window = window
    window.show()
    sys.exit(app.exec_())
