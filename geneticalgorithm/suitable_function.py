import math

from geneticalgorithm.individual import Individual


def calculate_fitness(ind: Individual, printing: bool = False) -> float:
    # to check if the sum of percentages is not greater than 100%
    in_percentage, out_percentage = {}, {}
    total_out_percentage, total_cars_in, total_cars_out = 0, 0, 0
    edge_cars_quantity, max_cars_in = {}, {}

    total_paths_in, total_paths_out = 0, 0

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
            cars_in = min(cars_in, out_edge.capacity)

        if out_edge.id not in edge_cars_quantity:
            edge_cars_quantity[out_edge.id] = 0
        edge_cars_quantity[out_edge.id] += cars_in

        if in_edge.from_node.in_or_out:  # not node or aux node
            edge_cars_quantity[out_edge.id] = cars_in
            total_cars_in += cars_in
            total_paths_in += 1
            if in_edge.id not in max_cars_in:
                max_cars_in[in_edge.id] = in_edge.capacity
        if out_edge.to_node.in_or_out:  # not node or aux node
            total_out_percentage += gen.current_percentage
            # total number of vehicles leaving
            total_cars_out += cars_in
            total_paths_out += 1

    for gen in gens:
        in_edge, out_edge = gen.in_edge, gen.out_edge
        gen.vehicles_could_enter = math.floor(in_edge.capacity * gen.current_percentage / 100)
        if not edge_cars_quantity.get(in_edge.id) is None:
            gen.current_vehicles_could_enter = edge_cars_quantity.get(in_edge.id)
            gen.current_vehicles_that_enter = min(gen.vehicles_could_enter, gen.current_vehicles_could_enter)
        else:
            gen.current_vehicles_could_enter = gen.vehicles_could_enter
            gen.current_vehicles_that_enter = gen.vehicles_could_enter

    # more than 100%
    sum_of_in_values = [x for x in list(in_percentage.values()) if x > 100]
    sum_of_out_values = [x for x in list(out_percentage.values()) if x > 100]

    # more than 100% in or out or 0% cars that leave the system
    if len(sum_of_in_values) or len(sum_of_out_values) or not total_out_percentage:
        return 0

    sum_max_cars_in = max(max_cars_in.values())
    if not total_cars_in or not sum_max_cars_in:
        return 0

    total_out = total_cars_out / total_paths_out
    total_in = total_cars_in / total_paths_in
    total_out_percentage = min(1.00, total_cars_out / sum_max_cars_in)
    fitness = (total_out / total_in) * total_out_percentage * 100

    if printing:
        print(f'total_out = total_cars_out / total_paths_out = {total_out} = {total_cars_out} / {total_paths_out}')
        print(f'total_in = total_cars_in / total_paths_in = {total_in} = {total_cars_in} / {total_paths_in}')
        print(
            f'used_percentage = min(1.00, total_cars_in / max_cars_in) = {total_out_percentage} = min(1.00, {total_cars_out} / {sum_max_cars_in})')
        print(f'fitness = {fitness} = {total_out} / {total_in} * {total_out_percentage} * 100')

    ind.total_in = total_in
    ind.total_out = total_out
    ind.total_out_percentage = total_out_percentage
    return round(fitness, 2)
