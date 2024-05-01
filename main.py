from typing import List

import graphviz

from model.edge import Edge
from model.node import Node
from model.edge_connection import EdgeConnection
from geneticalgorithm import random_population, suitable_function, individual, reproducer, random_util, mutator

POPULATION_SIZE: int = 100
MUTATION_PROBABLY: int = 50
TOTAL_GENERATIONS: int = 100

# dot = graphviz.Digraph(comment='Sample')
# dot.attr(rankdir='LR')

node_w = Node('W')
node_x = Node('X')
node_y = Node('Y')
node_z = Node('Z')

edge_a = Edge('A', None, node_w, 100)
edge_b = Edge('B', node_w, node_x, 75)
edge_c = Edge('C', node_w, node_z, 50)
edge_d = Edge('D', node_w, node_y, 60)
edge_e = Edge('E', node_x, node_z, 90)
edge_f = Edge('F', node_y, node_z, 30)
edge_g = Edge('G', node_z, None, 85)

nodes: List[Node] = [node_w, node_x, node_y, node_z]
edges: List[Edge] = [edge_a, edge_b, edge_c, edge_d, edge_e, edge_f, edge_g]
connections: List[EdgeConnection] = []

# adding in and out edges to each node
for edge in edges:
    tmp_from_node = edge.from_node
    tmp_to_node = edge.to_node

    if tmp_from_node:
        tmp_from_node.out_edges.append(edge)
    if tmp_to_node:
        tmp_to_node.in_edges.append(edge)

for node in nodes:
    for in_edge in node.in_edges:
        for out_edge in node.out_edges:
            connection = EdgeConnection(node, in_edge, out_edge)
            connections.append(connection)


# todo: create population here


def get_best_fitness() -> individual.Individual | None:
    total_generations, total_mutations = 1, 0
    population = random_population.random_population(POPULATION_SIZE, connections, suitable_function.calculate_fitness)

    best = population[0]
    while total_generations < TOTAL_GENERATIONS:
        for ind in population:
            if best.fitness < ind.fitness:
                best = ind

        total_generations += 1
        print(f'Generation: {total_generations}')
        new_population: list[individual.Individual] = []
        for i in range(POPULATION_SIZE):
            parent_x = random_population.select_random_individual(population)
            parent_y = random_population.select_random_individual(population)
            child_xy = reproducer.reproducer(parent_x, parent_y, suitable_function.calculate_fitness)

            if random_util.random_int(0, 100) >= MUTATION_PROBABLY:
                new_population.append(child_xy)
            else:
                new_population.append(mutator.mutate(child_xy, suitable_function.calculate_fitness))
                total_mutations += 1

        population = new_population

    print(f'Total mutations: {total_mutations}')
    print(f'{best.get_population_info()}, fitness: {best.fitness}')
    return best


best_fitness = get_best_fitness()
