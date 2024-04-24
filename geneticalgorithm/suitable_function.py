from geneticalgorithm.individual import Individual


def calculate_fitness(ind: Individual) -> int:
    in_percentage, out_percentage = {}, {}
    total_in, total_out = 0, 0

    gens = ind.gens
    for gen in gens:
        in_edge, out_edge = gen.in_edge, gen.out_edge
        if in_edge not in in_percentage:
            in_percentage[in_edge.id] = 0
        if out_edge not in out_percentage:
            out_percentage[out_edge.id] = 0

        # add percentage
        in_percentage[in_edge.id] += gen.current_percentage
        out_percentage[out_edge.id] += gen.current_percentage

    return 1
