import math

from geneticalgorithm.individual import Individual


def calculate_fitness(ind: Individual) -> float:
    # to check if the sum of percentages is not greater than 100%
    in_percentage, out_percentage = {}, {}
    total_out_percentage, total_cars_in, total_cars_out = 0, 0, 0
    edge_cars_quantity, max_cars_in = {}, {}

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

        # cars that could enter
        cars_in = math.floor(in_edge.capacity * gen.current_percentage / 100)
        if in_edge.id in edge_cars_quantity:
            # minimum of cars that could enter and cars in the enter edge
            cars_in = min(cars_in, edge_cars_quantity.get(in_edge.id))

        if out_edge.id not in edge_cars_quantity:
            edge_cars_quantity[out_edge.id] = 0
        edge_cars_quantity[out_edge.id] += cars_in

        if not in_edge.from_node:
            edge_cars_quantity[out_edge.id] = cars_in
            total_cars_in += cars_in
            if in_edge.id not in max_cars_in:
                max_cars_in[in_edge.id] = in_edge.capacity
        if not out_edge.to_node:
            total_out_percentage += gen.current_percentage
            # total number of vehicles leaving
            total_cars_out += cars_in

    # more than 100%
    sum_of_in_values = [x for x in list(in_percentage.values()) if x > 100]
    sum_of_out_values = [x for x in list(out_percentage.values()) if x > 100]

    # more than 100% in or out or 0% cars that leave the system
    if len(sum_of_in_values) or len(sum_of_out_values) or not total_out_percentage:
        return 0

    return (total_cars_out / total_cars_in) * (total_cars_out / sum(max_cars_in.values()))
