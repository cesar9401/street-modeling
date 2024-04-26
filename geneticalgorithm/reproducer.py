from geneticalgorithm import individual, suitable_function, random_util


def reproducer(
        individual_x: individual.Individual,
        individual_y: individual.Individual,
        suitable_calc: suitable_function.calculate_fitness
) -> individual.Individual:
    size = individual_x.size
    random = random_util.random_int(0, size - 1)
    child = individual.Individual.clone(individual_x)
    for i in range(size):
        if i <= random:
            child.gens[i].current_percentage = individual_x.gens[i].current_percentage
        else:
            child.gens[i].current_percentage = individual_y.gens[i].current_percentage

    child.fitness = suitable_calc(child)
    return child
