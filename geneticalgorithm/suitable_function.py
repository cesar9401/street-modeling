from geneticalgorithm.individual import Individual


def calculate_fitness(ind: Individual) -> float:
    in_percentage, out_percentage = dict(), dict()
    total_in_percentage, total_out_percentage = 0, 0

    gens = ind.gens
    for gen in gens:
        in_edge, out_edge = gen.in_edge, gen.out_edge
        if in_edge.id not in in_percentage:
            in_percentage[in_edge.id] = 0
        if out_edge.id not in out_percentage:
            out_percentage[out_edge.id] = 0

        # add percentage
        in_percentage[in_edge.id] += gen.current_percentage
        out_percentage[out_edge.id] += gen.current_percentage

        if not in_edge.from_node:
            total_in_percentage += gen.current_percentage
        if not out_edge.to_node:
            total_out_percentage += gen.current_percentage

    # more than 100%
    sum_of_in_values = [x for x in list(in_percentage.values()) if x > 100]
    sum_of_out_values = [x for x in list(out_percentage.values()) if x > 100]
    if len(sum_of_in_values) or len(sum_of_out_values):
        return 0

    # no out
    if not total_out_percentage:
        return 0

    return total_out_percentage / total_in_percentage
