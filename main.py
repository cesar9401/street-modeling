import uuid
from typing import List

import graphviz

from model.edge import Edge
from model.node import Node
from model.edge_connection import EdgeConnection
from geneticalgorithm import random_population

POPULATION_SIZE: int = 25

dot = graphviz.Digraph(comment='Sample')
dot.attr(rankdir='LR')

node_w = Node('W')
node_x = Node('X')
node_y = Node('Y')
node_z = Node('Z')

edge_a = Edge('A', None, node_w, 100)
edge_b = Edge('B', node_w, node_x, 75)
edge_c = Edge('C', node_w, node_z, 50)
edge_d = Edge('D', node_w, node_y, 60)
edge_e = Edge('E', node_x, node_z, 90)
edge_f = Edge('F', node_y, node_z, 30)
edge_g = Edge('G', node_z, None, 85)

nodes: List[Node] = [node_w, node_x, node_y, node_z]
edges: List[Edge] = [edge_a, edge_b, edge_c, edge_d, edge_e, edge_f, edge_g]
connections: List[EdgeConnection] = []

# adding in and out edges to each node
for edge in edges:
    tmp_from_node = edge.from_node
    tmp_to_node = edge.to_node

    if tmp_from_node:
        tmp_from_node.out_edges.append(edge)
    if tmp_to_node:
        tmp_to_node.in_edges.append(edge)

for node in nodes:
    for in_edge in node.in_edges:
        for out_edge in node.out_edges:
            connection = EdgeConnection(node, in_edge, out_edge)
            connections.append(connection)

# todo: create population here
population = random_population.random_population(POPULATION_SIZE, connections)
for individual in population:
    print(individual.get_population_info())
