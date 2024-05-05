import uuid
from typing import List

from model import edge


class Node:

    def __init__(self, label: str):
        self.id: str = uuid.uuid4().__str__()
        self.label: str = label
        self.in_edges: List[edge.Edge] = []
        self.out_edges: List[edge.Edge] = []
        self.pos_x: float = 0
        self.pos_y: float = 0
        self.color: str = '#3498DB'
        self.in_or_out: bool = False

    def __str__(self):
        return f'{self.id}: {self.label}, pos_x: {self.pos_x}, pos_y: {self.pos_y}'

    def clean_node(self):
        self.in_edges = []
        self.out_edges = []
