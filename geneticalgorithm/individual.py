import copy
from typing import List

from model import edge_connection


class Individual:

    def __init__(self, size: int, gens: List[edge_connection.EdgeConnection]):
        self.size: int = size
        self.gens: List[edge_connection.EdgeConnection] = gens
        self.fitness: float = 0
        self.total_in: float = 0
        self.total_out: float = 0
        self.total_out_percentage: float = 0

    def get_population_info(self) -> str:
        return str.join(', ', list(map(lambda x: x.get_percentage_info(), self.gens)))

    @staticmethod
    def clone(individual: 'Individual') -> 'Individual':
        size = individual.size
        gens: List[edge_connection.EdgeConnection] = copy.deepcopy(individual.gens)
        return Individual(size, gens)
