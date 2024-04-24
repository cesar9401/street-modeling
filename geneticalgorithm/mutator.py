from geneticalgorithm import individual
from geneticalgorithm import random_util


def mutate(ind: individual.Individual) -> individual.Individual:
    new_individual = individual.Individual.clone(ind)
    index = random_util.random_int(0, ind.size)
    new_individual.gens[index].current_percentage = random_util.random_int(0, 100)
    return new_individual
