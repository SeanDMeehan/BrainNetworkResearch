import DataProcessing
import GraphConstructor
import GraphAnalysis
import lin_alg_module
import json

def main():
    graph_file = "json_correlation_matrices_neurocon/sub-control032014_AAL116_correlation_matrix.json"
    graph = GraphConstructor.GraphConstructor(graph_file)
    graph.construct_graph(tolerance=0.0)
    #graph.draw_graph()
    graph_analysis = GraphAnalysis.GraphAnalysis(graph.get_graph())
    graph_analysis.print_graph_properties()

if __name__ == "__main__":
    main()