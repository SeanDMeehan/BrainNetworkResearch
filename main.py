import DataProcessing
import GraphConstructor
import GraphAnalysis

def main():
   data_processing = DataProcessing.DataProcessing()
   data_processing.convert_to_json_directory('mat_files', 'json_files')
   graph_constructor = GraphConstructor.GraphConstructor("global_thresholded_correlation_matrices_neurocon/sub-control032014_AAL116_correlation_matrix.csv")
   graph_constructor.construct_graph_unweighted()
   graph_constructor.draw_graph()
   graph_analysis = GraphAnalysis.GraphAnalysis(graph_constructor.get_graph(), matrix=graph_constructor.get_adjacency_matrix())
   graph_analysis.distribution_of_degree()
   graph_analysis.small_worldness()
   graph_analysis.is_symmetric()
   graph_analysis.graph_stats()
   #graph_analysis.debug()
if __name__ == "__main__":
    main()
