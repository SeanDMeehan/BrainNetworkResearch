import networkx as nx
import lin_alg_module
import random
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
import lin_alg_module


class GraphAnalysis():
    def __init__(self, graph, matrix=[]):
        self.__graph = graph
        self.__operator = lin_alg_module.lin_alg()
        self.__adjacency_matrix = matrix
        self.__random_graph = None
        self.__weight_list = [weight_dict['weight'] for _, _, weight_dict in self.__graph.edges(data=True)]
        self.__sorted_weight_list = []
        self.__weight_mean = 0
        self.__weight_standard_deviation = 0
        self.__gaussian_outputs = []
        self.__small_world_coefficient = 0

    def distribution_of_weights(self, show=False, random=False):
        self.__weight_mean = sum(self.__weight_list)/len(self.__weight_list)
        self.__weight_standard_deviation = (sum([(x - self.__weight_mean)**2 for x in self.__weight_list])/len(self.__weight_list))**0.5
        self.__gaussian_outputs = [(1/(self.__weight_standard_deviation*np.sqrt(2*np.pi)))*np.exp(-0.5*((x-self.__weight_mean)/self.__weight_standard_deviation)**2) for x in self.__weight_list]
        self.__sorted_weight_list, self.__gaussian_outputs = zip(*sorted(zip(self.__weight_list, self.__gaussian_outputs)))
        if show:
            plt.hist(self.__weight_list, bins=50, density=True, alpha=0.6, color='g')
            plt.plot(self.__sorted_weight_list, self.__gaussian_outputs, color='r')
            plt.title('Distribution of Weights')
            plt.show()
    
    def generate_random_graph_weighted(self, tolerance=0, show=False):
        def random_weight():
#------------------------------------------------------------------------------------------------------------------------------------------------------------#
#this is place holder code until a more sophisticated method for generating these random values is found
            return abs(random.gauss(self.__weight_mean, self.__weight_standard_deviation))
#------------------------------------------------------------------------------------------------------------------------------------------------------------#
        random_graph = nx.Graph()
        rand_weight =0
        for i in range(len(self.__graph.nodes())):
            random_graph.add_node(i)
        for i in range(len(self.__graph.nodes())):
            for j in range(len(self.__graph.nodes())):
                if i != j:
                    rand_weight = random_weight()
                    if abs(rand_weight) > tolerance:
                        random_graph.add_edge(i, j, weight=rand_weight)
        self.__random_graph = random_graph
        if show:
            edges = random_graph.edges()
            weights = [random_graph[u][v]['weight'] for u,v in edges]
            colors = [abs(weight) for weight in weights]
            pos = nx.spring_layout(random_graph)
            nx.draw(random_graph, pos, with_labels=True, node_color='lightblue', node_size=300)
            nx.draw_networkx_edges(random_graph, pos, edgelist=edges, edge_color=colors, width=2)
            plt.title("Graph Representation of Random Graph")
            plt.show()
            
    def distribution_of_degree(self):
        degree_sequence = [degree for node, degree in self.__graph.degree()]
        plt.hist(degree_sequence, bins=range(min(degree_sequence), max(degree_sequence) + 1), align='left', rwidth=0.8)
        plt.title('Degree Distribution')
        plt.xlabel('Degree')
        plt.ylabel('Frequency')
        plt.show()
      
    def is_symmetric(self):
        if self.__operator.is_symmetric(self.__adjacency_matrix):
            print("The adjacency matrix is symmetric.")
        else:
            print("The adjacency matrix is not symmetric.")
    
    def print_adjacency_matrix(self):
        self.__operator.print_matrix(self.__adjacency_matrix)

    def __generate_random_graph_unweighed(self, show=False):
            num_edges = 0
            num_nodes = 0
            for row in self.__adjacency_matrix:
                num_nodes+=1
                for entry in row:
                    num_edges += entry
            self.__random_graph = nx.gnm_random_graph(num_nodes, num_edges)
            if show:
                pos = nx.circular_layout(self.__random_graph)
                nx.draw(self.__random_graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=300)
                plt.title("Graph Representation of Random Graph")
                plt.show()
    
    def clustering_coefficint(self, graph):
        path_lengths_two = 0
        for node in self.__graph.nodes():
            for neighbor in graph.neighbors(node):
                if neighbor == node:
                    continue
                for neighbor2 in graph.neighbors(neighbor):
                    if neighbor2 != node and neighbor2 != neighbor:
                        path_lengths_two += 1
        triangles = sum(nx.triangles(graph).values())
        return triangles / path_lengths_two if path_lengths_two > 0 else 0
    
    def charcacteristic_path_length(self, graph):
        path_lengths = []
        for component in nx.connected_components(graph):
            subgraph = graph.subgraph(component)
            if nx.average_shortest_path_length(subgraph) > 1:
                path_lengths.append(nx.average_shortest_path_length(subgraph))
        return sum(path_lengths) / len(path_lengths)

    def small_worldness(self):
        self.__generate_random_graph_unweighed(show=True)
        CCrand = nx.average_clustering(self.__random_graph)
        CCreal = nx.average_clustering(self.__graph)
        try:
            CPLrand = nx.average_shortest_path_length(self.__random_graph)
        except nx.NetworkXError:
            CPLrand = self.charcacteristic_path_length(self.__random_graph)
        try:
            CPLreal = nx.average_shortest_path_length(self.__graph)
        except nx.NetworkXError:
            CPLreal = self.charcacteristic_path_length(self.__graph)
        self.__small_world_coefficient = (CCreal/CCrand)/(CPLreal/CPLrand)
        print(f"Clustering Coefficient of Random Graph: {CCrand}")
        print(f"Clustering Coefficient of Original Graph: {CCreal}")
        print(f"Characteristic Path Length of Random Graph: {CPLrand}")
        print(f"Characteristic Path Length of Original Graph: {CPLreal}")
        print(f"Small World Coefficient: {self.__small_world_coefficient}")
    
    def graph_stats(self):
        print(f"Number of nodes: {self.__graph.number_of_nodes()}")
        print(f"Number of edges: {self.__graph.number_of_edges()}")
        print(f"Possible edges: {self.__graph.number_of_nodes()*(self.__graph.number_of_nodes()-1)/2}")
        print(f"Density: {nx.density(self.__graph)}")
        print(f"Average Degree: {sum(dict(self.__graph.degree()).values())/self.__graph.number_of_nodes()}")
        
    def debug(self):
        self.__generate_random_graph_unweighed(show=True)
        for node, degree in self.__random_graph.degree():
            print(f"Node {node} has degree {degree}")
        triangles =  sum(nx.triangles(self.__random_graph).values())//3
        print(f"Number of triangles: {triangles}")
