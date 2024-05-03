from typing import List

from model.edge import Edge
from model.node import Node
from model.edge_connection import EdgeConnection
from geneticalgorithm import random_population, suitable_function, individual, reproducer, random_util, mutator


class GeneticAlgorithm:

    def __init__(self, nodes: List[Node], edges: List[Edge]):
        self.population_size: int = 100
        self.mutation_probably: int = 50
        self.total_generations: int = 100
        self.nodes = nodes
        self.edges = edges
        self.connections: List[EdgeConnection] = []

        # TODO: check nodes and edges
        for edge in self.edges:
            tmp_from_node = edge.from_node
            tmp_to_node = edge.to_node

            if tmp_from_node and not tmp_from_node.in_or_out:
                tmp_from_node.out_edges.append(edge)
            if tmp_to_node and not tmp_to_node.in_or_out:
                tmp_to_node.in_edges.append(edge)

        for node in self.nodes:
            if not len(node.in_edges) or not len(node.out_edges):
                print(f'Node {node} has no edges')

            if node.in_or_out:  # ignore in_or_out node
                continue

            # create connections here
            for in_edge in node.in_edges:
                for out_edge in node.out_edges:
                    connection = EdgeConnection(node, in_edge, out_edge)
                    self.connections.append(connection)

        for connection in self.connections:
            print(connection)

    def get_best_fitness(self) -> individual.Individual | None:
        total_generations, total_mutations = 1, 0
        population = random_population.random_population(
            self.population_size, self.connections, suitable_function.calculate_fitness
        )

        best = population[0]
        while total_generations < self.total_generations:
            for ind in population:
                if best.fitness < ind.fitness:
                    best = ind

            total_generations += 1
            print(f'Generation: {total_generations}')
            new_population: list[individual.Individual] = []
            for i in range(self.population_size):
                parent_x = random_population.select_random_individual(population)
                parent_y = random_population.select_random_individual(population)
                child_xy = reproducer.reproducer(parent_x, parent_y, suitable_function.calculate_fitness)

                if random_util.random_int(0, 100) >= self.mutation_probably:
                    new_population.append(child_xy)
                else:
                    new_population.append(mutator.mutate(child_xy, suitable_function.calculate_fitness))
                    total_mutations += 1

            population = new_population

        print(f'Total mutations: {total_mutations}')
        print(f'{best.get_population_info()}, fitness: {best.fitness}')
        return best
