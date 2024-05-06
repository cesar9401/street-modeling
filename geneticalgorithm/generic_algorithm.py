import threading
from typing import List

from model.edge import Edge
from model.node import Node
from model.edge_connection import EdgeConnection
from geneticalgorithm import random_population, suitable_function, individual, reproducer, random_util, mutator
from ui import main_widget


class GenericAlgorithm:

    def __init__(self, callback):
        self.population_size: int | None = None
        self.mutations_quantity: int | None = None
        self.mutations_generations_quantity: int | None = None
        self.completion_by_generations: bool | None = None
        self.completion_criteria_value: float | None = None
        self.mutation_probably: float | None = None
        self.nodes: List[Node] = []
        self.edges: List[Edge] = []
        self.stop = False

        self.connections: List[EdgeConnection] = []
        self.best: individual.Individual | None = None

        self.window: main_widget.MainWidget | None = None
        self.callback = callback

    def __get_best_fitness(self):
        total_generations, total_mutations = 1, 0
        population = random_population.random_population(
            self.population_size, self.connections, suitable_function.calculate_fitness
        )

        self.best = population[0]

        while total_generations < self.completion_criteria_value \
                if self.completion_by_generations \
                else self.best.fitness < self.completion_criteria_value:

            if self.stop:
                print(f'stopping at generation: {total_generations}')
                break

            for ind in population:
                if self.best.fitness < ind.fitness:
                    self.best = ind

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

        print(f'Total generations: {total_generations}')
        print(f'Total mutations: {total_mutations}')
        print(f'{self.best.get_population_info()}, fitness: {self.best.fitness}')

        print('best:')
        suitable_function.calculate_fitness(self.best, True)
        self.__print_results()

    def get_best_fitness_on_second_thread(
            self,
            population_size: int,
            mutations_quantity: int,
            mutations_generations_quantity: int,
            completion_by_generations: bool,
            completion_criteria_value: float,
            nodes: List[Node], edges: List[Edge]
    ):
        self.population_size: int = population_size
        self.mutations_quantity: int = mutations_quantity
        self.mutations_generations_quantity: int = mutations_generations_quantity
        self.completion_by_generations: bool = completion_by_generations
        self.completion_criteria_value: float = completion_criteria_value
        self.nodes = nodes
        self.edges = edges
        self.stop = False

        self.best: individual.Individual | None = None

        self.mutation_probably: float = (
                (self.mutations_quantity * 100) / (self.mutations_generations_quantity * self.population_size)
        )

        self.connections: List[EdgeConnection] = []
        for node in self.nodes:
            node.clean_node()

        # check nodes and edges
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

        second_thread = threading.Thread(target=self.__get_best_fitness)
        second_thread.start()
        print('second thread started')

    def __print_results(self):
        self.callback(self.nodes, self.edges, self.best)
