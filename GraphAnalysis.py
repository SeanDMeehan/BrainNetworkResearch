import networkx as nx
import lin_alg_module
class GraphAnalysis():
    def __init__(self, graph):
        self.__graph = graph
        self.__Operator = lin_alg_module.lin_alg()
    def print_graph_properties(self):
        print(f'Number of nodes: {self.__graph.number_of_nodes()}')
        print(f'Number of edges: {self.__graph.number_of_edges()}')
        try:
            print(f'Average clustering coefficient: {nx.average_clustering(self.__graph)}')
        except:
            print('Average clustering coefficient: Calcukation failed')
        try:
            print('Average clustering coefficient: Graph is not fully connected')
        except:
            print('Average clustering coefficient: Calculation failed')
        try:
            print(f'Average shortest path length: {nx.average_shortest_path_length(self.__graph)}')
        except:
            print('Average shortest path length: Calculation failed')
        try:
            print(f'Diameter: {nx.diameter(self.__graph)}')
        except:
            print('Diameter: Calculation failed')
        try:
            print(f'Density: {nx.density(self.__graph)}')
        except:
            print('Density: Calculation failed')
        try:
            print(f'Global efficiency: {nx.global_efficiency(self.__graph)}')
        except:
            print('Global efficiency: Calculation failed')
        try:
            print(f'Local efficiency: {nx.local_efficiency(self.__graph)}')
        except:
            print('Local efficiency: Calculation failed')
        try:
            print(f'Transitivity: {nx.transitivity(self.__graph)}')
        except:
            print('Transitivity: Calculation failed')
        try:
            print(f'Assortativity: {nx.degree_assortativity_coefficient(self.__graph)}')
        except:
            print('Assortativity: Calculation failed')
        try:
            print(f'Average degree connectivity: {nx.average_degree_connectivity(self.__graph)}')  
        except:
            print('Average degree connectivity: Calculation failed')
        try:
            print(f'Average node connectivity: {nx.average_node_connectivity(self.__graph)}')
        except:
            print('Average node connectivity: Calculation failed')
        try:
            print(f'Average nearest neighbors degree: {nx.average_neighbor_degree(self.__graph)}')
        except:
            print('Average nearest neighbors degree: Calculation failed')
        try:
            print(f'Average clustering: {nx.average_clustering(self.__graph)}')
        except:
            print('Average clustering: Calculation failed')
        try:
            print(f'Average node connectivity: {nx.average_node_connectivity(self.__graph)}')
        except:
            print('Average node connectivity: Calculation failed')
        try:
            print(f'Average shortest path length: {nx.average_shortest_path_length(self.__graph)}')
        except:
            print('Average shortest path length: Calculation failed')
        try:
            print(f'Average betweenness centrality: {nx.betweenness_centrality(self.__graph)}')
        except:
            print('Average betweenness centrality: Calculation failed')
        try:
            print(f'Average closeness centrality: {nx.closeness_centrality(self.__graph)}')
        except:
            print('Average closeness centrality: Calculation failed')
        try:
            print(f'Average eigenvector centrality: {nx.eigenvector_centrality(self.__graph)}')
        except:
            print('Average eigenvector centrality: Calculation failed')
        try:
            print(f'Average degree centrality: {nx.degree_centrality(self.__graph)}')
        except:
            print('Average degree centrality: Calculation failed')
        try:
            print(f'Average communicability: {nx.communicability(self.__graph)}')
        except:
            print('Average communicability: Calculation failed')
        try:
            print(f'Average communicability betweenness centrality: {nx.communicability_betweenness_centrality(self.__graph)}')
        except:
            print('Average communicability betweenness centrality: Calculation failed')
        try:
            print(f'Average current flow closeness centrality: {nx.current_flow_closeness_centrality(self.__graph)}')
        except:
            print('Average current flow closeness centrality: Calculation failed')
        try:
            print(f'Average current flow betweenness centrality: {nx.current_flow_betweenness_centrality(self.__graph)}')
        except:
            print('Average current flow betweenness centrality: Calculation failed')
        try:
            print(f'Average edge betweenness centrality: {nx.edge_betweenness_centrality(self.__graph)}')
        except:
            print('Average edge betweenness centrality: Calculation failed')
        try:
            print(f'Average edge load centrality: {nx.edge_load_centrality(self.__graph)}')
        except:
            print('Average edge load centrality: Calculation failed')
        try:
            print(f'Average load centrality: {nx.load_centrality(self.__graph)}')
        except:
            print('Average load centrality: Calculation failed')
        try:
            print(f'Average communicability centrality: {nx.communicability_centrality(self.__graph)}')
        except:
            print('Average communicability centrality: Calculation failed')
        try:
            print(f'Average subgraph centrality: {nx.subgraph_centrality(self.__graph)}')
        except:
            print('Average subgraph centrality: Calculation failed')
        try:
            print(f'Average second order centrality: {nx.second_order_centrality(self.__graph)}')
        except:
            print('Average second order centrality: Calculation failed')
        try:
            print(f'Average percolation centrality: {nx.percolation_centrality(self.__graph)}')
        except:
            print('Average percolation centrality: Calculation failed')
        try:
            print(f'Average information centrality: {nx.information_centrality(self.__graph)}')
        except:
            print('Average information centrality: Calculation failed')
        try:
            print(f'Average harmonic centrality: {nx.harmonic_centrality(self.__graph)}')
        except:
            print('Average harmonic centrality: Calculation failed')
        try:
            print(f'Average closeness vitality: {nx.closeness_vitality(self.__graph)}')
        except:
            print('Average closeness vitality: Calculation failed')
        try:
            print(f'Average betweenness vitality: {nx.betweenness_vitality(self.__graph)}')
        except:
            print('Average betweenness vitality: Calculation failed')
        try:
            print(f'Average degree vitality: {nx.degree_vitality(self.__graph)}')
        except:
            print('Average degree vitality: Calculation failed')
        try:
            print(f'Average eigenvector vitality: {nx.eigenvector_vitality(self.__graph)}')
        except:
            print('Average eigenvector vitality: Calculation failed')
        try:
            print(f'Average subgraph vitality: {nx.subgraph_vitality(self.__graph)}')
        except:
            print('Average subgraph vitality: Calculation failed')
        try:
            print(f'Average second order vitality: {nx.second_order_vitality(self.__graph)}')
        except:
            print('Average second order vitality: Calculation failed')
        try:
            print(f'Average percolation vitality: {nx.percolation_vitality(self.__graph)}')
        except:
            print('Average percolation vitality: Calculation failed')
        try:
            print(f'Average information vitality: {nx.information_vitality(self.__graph)}')
        except:
            print('Average information vitality: Calculation failed')
        try:
            print(f'Average harmonic vitality: {nx.harmonic_vitality(self.__graph)}')
        except:
            print('Average harmonic vitality: Calculation failed')
        try:    
            print(f'Average communicability vitality: {nx.communicability_vitality(self.__graph)}')
        except:
            print('Average communicability vitality: Calculation failed')
        try:
            print(f'Average current flow closeness vitality: {nx.current_flow_closeness_vitality(self.__graph)}')
        except:
            print('Average current flow closeness vitality: Calculation failed')
        try:
            print(f'Average current flow betweenness vitality: {nx.current_flow_betweenness_vitality(self.__graph)}')
        except:
            print('Average current flow betweenness vitality: Calculation failed')
        try:
            print(f'Average edge betweenness vitality: {nx.edge_betweenness_vitality(self.__graph)}')
        except:
            print('Average edge betweenness vitality: Calculation failed')
        try:
            print(f'Average edge load vitality: {nx.edge_load_vitality(self.__graph)}')
        except:
            print('Average edge load vitality: Calculation failed')
        try:
            print(f'Average load vitality: {nx.load_vitality(self.__graph)}')
        except:
            print('Average load vitality: Calculation failed')

    def is_symmetric(self):
        return self.__Operator.is_symmetric(self.__graph)
