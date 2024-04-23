from model import node
from model import edge


class EdgeConnection:
    def __init__(self, connection_node: node.Node, in_edge: edge.Edge, out_edge: edge.Edge):
        self.connection_node3: node.Node = connection_node
        self.in_edge: edge.Edge = in_edge
        self.out_edge: edge.Edge = out_edge
        self.min_percentage: float = 0
        self.max_percentage: float = 0
        self.current_percentage: float = 0
