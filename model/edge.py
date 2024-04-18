import uuid

from model import node


class Edge:
    def __init__(
            self, label: str, minimum_percentage: float, maximum_percentage: float,
            from_node: node.Node | None, to_node: node.Node | None
    ):
        self.id: str = uuid.uuid4().__str__()
        self.label: str = label
        self.minimum_percentage: float = minimum_percentage
        self.maximum_percentage: float = maximum_percentage
        self.from_node: node.Node = from_node
        self.to_node: node.Node = to_node
        self.current_percentage: float = 0

    def __str__(self):
        return f"[{self.id}: {self.label}]"
