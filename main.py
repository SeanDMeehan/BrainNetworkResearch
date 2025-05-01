import DataProcessing
import GraphConstructor
import GraphAnalysis
import os
import time
import re
import csv

def main(file, writer):
   #this is the main function that will take in a thresholded graph file and then perform graph analysis on it
   # the graph analysis will include small worldness, degree distribution, and other graph metrics
   # the results will be saved to a csv file
   graph_constructor = GraphConstructor.GraphConstructor("global_thresholded_correlation_matrices_neurocon/" + file)
   graph_constructor.construct_graph_unweighted()
   graph_analysis = GraphAnalysis.GraphAnalysis(graph_constructor.get_graph(), graph_constructor.get_adjacency_matrix())
   small_world_stats = graph_analysis.small_worldness(return_stats=True)
   symmetric = graph_analysis.is_symmetric(return_value=True)
   graph_stats = graph_analysis.graph_stats(return_stats=True)
   cpl_stats = graph_analysis.characteristic_path_length_2(graph_constructor.get_graph(), return_stats=True)
   control_or_patient = ''
   if 'control' in file:
      control_or_patient = 'control'
   else:
      control_or_patient = 'patient'
   match = re.search(r'\d{6}', file)
   if match:
      subject_id = match.group()
   else:
      subject_id = "unknown"
   row = [subject_id, 
         control_or_patient,
         graph_stats['nodes'],
         graph_stats['edges'],
         graph_stats['possible_edges'],
         graph_stats['density'],
         graph_stats['average_degree'],
         symmetric,
         small_world_stats['CCrand'],
         small_world_stats['CCreal'],
         small_world_stats['CPLrand'],
         small_world_stats['CPLreal'],
         small_world_stats['CCrand'] - small_world_stats['CCreal'],
         small_world_stats['CPLrand'] - small_world_stats['CPLreal'],
         small_world_stats['small_world_coefficient'],
         cpl_stats['num_subgraphs'],
         cpl_stats['nodes'],
         cpl_stats['edges']
         ]
   writer.writerow(row)

'''
   # this is the main function that will split the data set into control and patient groups and then perfrom thresholding on both sets independently after 
   # converting the data to json and then to csv
   data_processing = DataProcessing.DataProcessing()
   data_processing.split_patient_control("neurocon", "neurocon_patient", "neurocon_control")
   data_processing.convert_to_json_directory("neurocon_control", "neurocon_control_json")
   data_processing.convert_to_json_directory("neurocon_patient", "neurocon_patient_json")
   data_processing.convert_to_csv_directory("neurocon_control_json", "neurocon_control_csv")
   data_processing.convert_to_csv_directory("neurocon_patient_json", "neurocon_patient_csv")
   data_processing.global_thresholding("neurocon_control_csv", "master_edge_list_control", "global_thresholded_correlation_matrices_neurocon_control_patient", 0.05)
   data_processing.global_thresholding("neurocon_patient_csv", "master_edge_list_patient", "global_thresholded_correlation_matrices_neurocon_control_patient", 0.05, remove_folder=False)
   '''
   
if __name__ == "__main__":
   #This loop will take in a directory of thresholded graphs and then perform graph analysis on each graph
   # the results will be saved to a csv file
   input_directory = "global_thresholded_correlation_matrices_neurocon_control_patient"
   output_file = "neurocon_results_patient_control.csv"
   if not os.path.exists(output_file):
      raise FileNotFoundError(f"Output file {output_file} does not exist.")
   data_processing = DataProcessing.DataProcessing()
   files = os.listdir(input_directory)
   with open(output_file, 'w', newline='') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(['subject_id',
                     'control_or_patient',
                     'nodes',
                     'edges',
                     'possible_edges',
                     'density',
                     'average_degree',
                     'symmetric',
                     'CCrand',
                     'CCreal',
                     'CPLrand',
                     'CPLreal',
                     'CCdiff',
                     'CPLdiff',
                     'small_world_coefficient',
                     'number_of_subgraphs',
                     'biggest_subgraph_nodes',
                     'biggest_subgraph_edges',
                  ])
      length = len(files)
      counter = 0
      for file in files:
         if file.endswith(".csv"):
            print(f"-------------------------------{file}--------------------------------")
            main(file, writer)
            counter += 1
         print(f"{counter/length*100:.2f}% done")

   '''
   #This runs main with no parameters. For splitting control and patient groups, thresholding, and converting to csv
   main(None, None)
   '''