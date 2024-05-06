import sys

import graphviz
from PyQt5.QtWidgets import QApplication, QStyleFactory
from geneticalgorithm import generic_algorithm
from ui import main_widget

from model import summary


def print_results(summary1: summary.Summary):
    dot = graphviz.Digraph(comment='Simple Genetic Algorithm')
    dot.attr(rankdir='LR')
    nodes = summary1.nodes
    edges = summary1.edges
    best = summary1.best

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
    label = '\nSimple Genetic Algorithm\n'
    label += f'Fitness: {best.fitness}% ({best.total_out} / {best.total_in} * {best.total_out_percentage} * 100)\n'

    for gen in best.gens:
        in_edge = gen.in_edge
        out_edge = gen.out_edge
        _from = f'{in_edge.from_node.label}{in_edge.to_node.label}'
        _to = f'{out_edge.from_node.label}{out_edge.to_node.label}'
        label += f'{_from} -> {_to} = {gen.current_percentage}%'
        label += f' (max: {gen.vehicles_could_enter}, current: {gen.current_vehicles_could_enter}, enter: {gen.current_vehicles_that_enter})\n'

    label += f'Total generations: {summary1.total_generations}\n'
    label += f'Population size: {summary1.population_size}\n'
    label += f'Total individuals: {summary1.total_individuals}\n'
    label += f'Total mutations: {summary1.total_mutations}\n'
    dot.attr(label=label)
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
