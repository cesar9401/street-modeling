import math

from geneticalgorithm.individual import Individual


def calculate_fitness(ind: Individual) -> float:
    # to check if the sum of percentages is not greater than 100%
    in_percentage, out_percentage = dict(), dict()
    total_in_percentage, total_out_percentage = 0, 0
    total_cars_in, total_cars_out = 0, 0
    edge_cars_quantity = dict()

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

        if out_edge.id in edge_cars_quantity:
            cars_in = min(
                edge_cars_quantity.get(in_edge.id),
                math.floor(out_edge.capacity * gen.current_percentage / 100)
            )
        else:
            cars_in = math.floor(in_edge.capacity * gen.current_percentage / 100)

        if out_edge.id not in edge_cars_quantity:
            edge_cars_quantity[out_edge.id] = 0
        edge_cars_quantity[out_edge.id] += cars_in

        if not in_edge.from_node:
            # print(f'in: {in_edge.label} -> {out_edge.label}: {in_edge.capacity} -> {gen.current_percentage}')
            total_in_percentage += gen.current_percentage
            edge_cars_quantity[out_edge.id] = cars_in
            total_cars_in += edge_cars_quantity[out_edge.id]
        if not out_edge.to_node:
            # print(f'out: {out_edge.label} -> {out_edge.capacity} -> {gen.current_percentage}')
            total_out_percentage += gen.current_percentage
            total_cars_out += edge_cars_quantity[in_edge.id]

    # more than 100%
    sum_of_in_values = [x for x in list(in_percentage.values()) if x > 100]
    sum_of_out_values = [x for x in list(out_percentage.values()) if x > 100]

    if len(sum_of_in_values) or len(sum_of_out_values):
        return 0

    # no out
    if not total_out_percentage:
        return 0

    return total_cars_out / total_cars_in
