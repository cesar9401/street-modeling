from typing import List

from geneticalgorithm import individual
from model import node
from model import edge


class Summary:
    def __init__(
            self,
            total_generations,
            total_mutations,
            population_size,
            best: individual.Individual,
            nodes: List[node.Node],
            edges: List[edge.Edge]
    ):
        self.total_generations = total_generations
        self.total_mutations = total_mutations
        self.population_size = population_size
        self.total_individuals = total_generations * population_size
        self.nodes: List[node.Node] = nodes
        self.edges: List[edge.Edge] = edges
        self.best: individual.Individual = best
