from typing import List

from geneticalgorithm import individual
from geneticalgorithm import random_util
from model import edge_connection


def random_population(
        population_size: int,
        sample_gens: List[edge_connection.EdgeConnection]
) -> List[individual.Individual]:
    population: List[individual.Individual] = []
    for _ in range(population_size):
        gens: List[edge_connection.EdgeConnection] = []
        for gen in sample_gens:
            copy_gen = edge_connection.EdgeConnection.clone(gen)
            copy_gen.current_percentage = random_util.random_int(0, 100)
            gens.append(copy_gen)
        # TODO: evaluate individual
        new_individual = individual.Individual(len(gens), gens)
        population.append(new_individual)
    return population
