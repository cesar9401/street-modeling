import uuid
from typing import List

from model import edge


class Node:

    def __init__(self, label: str):
        self.id: str = uuid.uuid4().__str__()
        self.label: str = label
        self.in_edges: List[edge.Edge] = []
        self.out_edges: List[edge.Edge] = []
        self.pos_x: int = 0
        self.pos_y: int = 0

    def __str__(self):
        return f'{self.id}: {self.label}'
