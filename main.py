import uuid
from typing import List

import graphviz

from model.edge import Edge
from model.node import Node

dot = graphviz.Digraph(comment='Sample')
dot.attr(rankdir='LR')

nodeA = Node('A')
nodeB = Node('B')
nodeC = Node('C')
nodeD = Node('D')

edgeA = Edge('A', 10, 100, None, nodeA)
edgeAB = Edge('AB', 10, 100, nodeA, nodeB)
edgeAC = Edge('AC', 10, 100, nodeA, nodeC)
edgeBD = Edge('BD', 10, 100, nodeB, nodeD)
edgeCD = Edge('CD', 10, 100, nodeC, nodeD)
edgeD = Edge('D', 10, 100, nodeD, None)

nodes: List[Node] = [nodeA, nodeB, nodeC, nodeD]
edges: List[Edge] = [edgeA, edgeAB, edgeAC, edgeBD, edgeCD, edgeD]

# adding in and out edges to each node
for edge in edges:
    tmp_from_node = edge.from_node
    tmp_to_node = edge.to_node

    if tmp_from_node:
        tmp_from_node.out_edges.append(edge)
    if tmp_to_node:
        tmp_to_node.in_edges.append(edge)

# adding nodes to dot file
for node in nodes:
    dot.node(node.id, node.label)

# adding edges to dot file
for edge in edges:
    from_node: str = uuid.uuid4().__str__()
    to_node: str = uuid.uuid4().__str__()
    if edge.from_node:
        from_node = edge.from_node.id
    else:
        dot.node(from_node, style='invis')

    if edge.to_node:
        to_node = edge.to_node.id
    else:
        dot.node(to_node, style='invis')

    dot.edge(from_node, to_node)

# render
dot.render('dot/sample.gv', view=True, format='png')
