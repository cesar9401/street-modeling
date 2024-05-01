import uuid

from model import node


class Edge:
    def __init__(self, label: str, from_node: 'node.Node | None', to_node: 'node.Node | None', capacity: int):
        self.id: str = uuid.uuid4().__str__()
        # self.id: str = label
        self.label: str = label
        self.from_node: node.Node = from_node
        self.to_node: node.Node = to_node
        self.capacity: int = capacity

    def __str__(self):
        return f"[{self.id}: {self.label}]"
