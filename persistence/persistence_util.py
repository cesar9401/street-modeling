import pickle
from typing import List
from model.edge import Edge
from model.node import Node


class WrapperUtil:
    def __init__(self, nodes: List[Node], edges: List[Edge]):
        self.nodes = nodes
        self.edges = edges
        for node in nodes:
            node.clean_node()


def save_to_file(nodes: List[Node], edges: List[Edge], filename: str) -> bool:
    if not len(nodes) or not len(edges):
        return False

    wrapper = WrapperUtil(nodes, edges)
    try:
        with open(filename, 'wb') as output:
            pickle.dump(wrapper, output, protocol=pickle.HIGHEST_PROTOCOL)
    except:
        return False

    return True


def load_from_file(filename: str) -> WrapperUtil:
    try:
        with open(filename, 'rb') as inpt:
            wrapper = pickle.load(inpt)
            return wrapper
    except:
        return WrapperUtil([], [])
