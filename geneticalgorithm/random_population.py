from typing import List

from geneticalgorithm import individual, random_util, suitable_function

from model import edge_connection


def random_population(
        population_size: int,
        sample_gens: List[edge_connection.EdgeConnection],
        suitable_calc: suitable_function.calculate_fitness
) -> List[individual.Individual]:
    population: List[individual.Individual] = []
    for _ in range(population_size):
        gens: List[edge_connection.EdgeConnection] = []
        for gen in sample_gens:
            copy_gen = edge_connection.EdgeConnection.clone(gen)
            copy_gen.current_percentage = random_util.random_int(0, 100)
            gens.append(copy_gen)
        new_individual = individual.Individual(len(gens), gens)
        # evaluate individual
        new_individual.fitness = suitable_calc(new_individual)
        population.append(new_individual)
    return population
