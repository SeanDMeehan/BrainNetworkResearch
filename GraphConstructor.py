import json
import networkx as nx
import matplotlib.pyplot as plt

class GraphConstructor:
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__graph = nx.Graph()
    
    def construct_graph(self, tolerance=0.0): 
        with open(self.__file_path) as f:
            data = json.load(f)
        index_set = [str(x) for x in range(len(data['data']))]
        for x in index_set:
            self.__graph.add_node(x)
        for i in range(len(data['data'])):
            for j in range(len(data['data'])):
                if i != j:
                    if abs(data['data'][i][j]) > tolerance:
                        self.__graph.add_edge(str(i), str(j), weight=data['data'][i][j])

    def draw_graph(self, node_color="lightblue", node_size=300): 
        edges = self.__graph.edges()
        weights = [self.__graph[u][v]['weight'] for u,v in edges]
        colors = [abs(weight) for weight in weights]
        pos = nx.spring_layout(self.__graph)
        nx.draw(self.__graph, pos, with_labels=True, node_color=node_color, node_size=node_size)
        nx.draw_networkx_edges(self.__graph, pos, edgelist=edges, edge_color=colors, width=2)
        plt.title("Graph Representation of Correlation Matrix")
        plt.show()
    def get_graph(self):
        return self.__graph
