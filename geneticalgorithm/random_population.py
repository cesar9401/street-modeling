import math
from functools import reduce
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
            in_capacity = gen.in_edge.capacity
            out_capacity = gen.out_edge.capacity
            high = min(100, int(in_capacity / out_capacity * 100))
            copy_gen = edge_connection.EdgeConnection.clone(gen)
            copy_gen.current_percentage = random_util.random_int(0, high)
            gens.append(copy_gen)
        new_individual = individual.Individual(len(gens), gens)
        # evaluate individual
        new_individual.fitness = suitable_calc(new_individual)
        population.append(new_individual)
    return population


def select_random_individual(population: List[individual.Individual]) -> individual.Individual:
    size: int = len(population)
    totals: list[int] = []
    total: int = 0
    for i in range(size):
        total += math.ceil(population[i].fitness)
        totals.append(total)

    random_until_total_suitable: int = random_util.random_int(0, total - 1)
    for i in range(size):
        if random_until_total_suitable < totals[i]:
            return population[i]
    return population[size - 1]
