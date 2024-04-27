from geneticalgorithm import individual
from geneticalgorithm import random_util
from geneticalgorithm import suitable_function


def mutate(ind: individual.Individual, suitable_calc: suitable_function.calculate_fitness) -> individual.Individual:
    index = random_util.random_int(0, ind.size - 1)
    ind.gens[index].current_percentage = random_util.random_int(0, 100)
    ind.fitness = suitable_calc(ind)
    return ind
