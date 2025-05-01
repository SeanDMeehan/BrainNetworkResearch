'''This is a module for processing fMRI based BOLD signal time sequence correlation data. It includes the following class: DataProcessing.'''
from scipy.io import loadmat
import numpy as np
import json
import os 
import time
import csv
from typing import Literal
from scipy.stats import norm
import subprocess

class DataProcessing:
    '''This is a class for processing .mat data. It includes methods for converting data to JSON and CSV formats,
    creating a master edge list, and performing global thresholding on the data.'''
    def __init__(self):
        self.__start = float
        self.__counter = int
        self.__total = int
        pass

    def __start_process_tracker(self, total):
        self.__total = total
        self.__start = time.time()
        self.__counter = 0

    def __process_tracker(self):
        self.__counter += 1
        print(f'{round((self.__counter/((self.__total)-1)*100), 2)}% done')
        time_remaining = round(((self.__total)-1)*((time.time()-self.__start)/self.__counter) - (time.time()-self.__start), 2)
        print(f'{time_remaining} seconds remaining')

    def __convert_to_json_compatible(self, matrix):
        for key in matrix.keys():
            if isinstance(matrix[key], np.ndarray):
                matrix[key] = [[float(y) for y in x] for x in matrix[key]]
            if isinstance(matrix[key], bytes):
                matrix[key] = matrix[key].decode('utf-8')
        return matrix

    def convert_to_json_directory(self, input_folder_name: str, output_folder_name: str):
        '''This method converts the .mat files in a directory to JSON format. It creates a new directory for the JSON files.\n
        inputs:\n
            input_folder_name: str - the name of the folder containing the .mat files\n
            output_folder_name: str - the name of the folder to save the JSON files'''
        if not os.path.exists(output_folder_name):
            os.makedirs(output_folder_name)
            print(f"Directory '{output_folder_name}' created")
        files = os.listdir(input_folder_name)
        self.__start_process_tracker(len(files)-1)
        matrix = {}
        for outer_file in files:
            if outer_file == '.DS_Store':
                continue
            inner_files = os.listdir(input_folder_name+'/'+outer_file)
            for inner_file in inner_files:
                if inner_file.endswith('AAL116_correlation_matrix.mat'):
                    matrix = loadmat(os.path.join(input_folder_name, outer_file, inner_file))
                    with open(output_folder_name+'/'+inner_file[:-4]+'.json', 'w') as f:
                        json.dump(self.__convert_to_json_compatible(matrix), f, indent=2)
                    self.__process_tracker()
        print('done')
    
    def convert_to_csv_directory(self, input_folder_name: str, output_folder_name: str):
        '''This method converts .json that were converted from .mat files to CSV format. It creates a new directory for the CSV files.\n
        inputs:\n
            input_folder_name: str - the name of the folder containing the .json files\n
            output_folder_name: str - the name of the folder to save the CSV files'''
        files = os.listdir(input_folder_name)
        if not os.path.exists(output_folder_name):
            os.makedirs(output_folder_name)
            print(f"Directory '{output_folder_name}' created")
        self.__start_process_tracker(len(files)-1)
        for file in files:
            if file.endswith('.json'):
                with open(input_folder_name+'/'+file, 'r') as f:
                    data = json.load(f)
                with open(output_folder_name+'/'+file[:-5]+'.csv', 'w') as f:
                    writer = csv.writer(f)
                    writer.writerows(data['data'])
                self.__process_tracker()
        print('done')

    def __global_thresholding_prep(self, input_folder_name: str, master_edge_list_name: str):
        if os.path.exists(input_folder_name+'/'+master_edge_list_name+'.csv'):
            os.remove(input_folder_name+'/'+master_edge_list_name+'.csv')
        files = os.listdir(input_folder_name)
        edge_sum = 0
        edge_n = 0
        with open(input_folder_name+'/'+master_edge_list_name+'.csv', 'w') as f:
            writer = csv.writer(f)
            self.__start_process_tracker(len(files))
            for file in files:
                if file.endswith('.csv'):
                    with open(input_folder_name+'/'+file, 'r') as f1:
                        reader = csv.reader(f1)
                        for row in reader:
                            writer.writerow(row)
                            edge_n += len(row)
                            edge_sum += sum([abs(float(x)) for x in row])
                self.__process_tracker()
            print('master edge list created')
            return edge_n, edge_sum
        
    def global_thresholding(self,input_folder_name: str, master_edge_list_name: str, output_folder_name: str, alpha: float, remove_folder: bool = True):
        '''This method performs global thresholding on the data. It creates a new directory for the thresholded files.
        It uses a distribution of all of the weights in the entire data set to perform a Z-value signifigance test for every weight in a given graph. If the p value is less
        than the alpha value the weight becomes 1. Otherwise, the weight becomes 0.\n
        inputs:\n
            input_folder_name: str - the name of the folder containing the .csv files\n
            master_edge_list_name: str - the name of the master edge list file. This list will be created.\n
            output_folder_name: str - the name of the folder to save the thresholded files\n
            alpha: float - the significance level for the thresholding\n
            remove_folder: bool - whether to remove the output folder if it exists. Default is True.'''
        if remove_folder:
            if os.path.exists(output_folder_name):
                os.listdir(output_folder_name)
                for file in os.listdir(output_folder_name):
                    os.remove(output_folder_name+'/'+file)
                os.rmdir(output_folder_name)
            os.makedirs(output_folder_name)
        print(f"Directory '{output_folder_name}' created")
        edge_n, edge_sum = self.__global_thresholding_prep(input_folder_name, master_edge_list_name)
        edge_mean = edge_sum/edge_n
        edge_sd = 0
        with open(input_folder_name+'/'+master_edge_list_name+'.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                for entry in row:
                    edge_sd += (abs(float(entry)) - edge_mean)**2
        edge_sd = (edge_sd/(edge_n-1))**0.5
        files = os.listdir(input_folder_name)
        self.__start_process_tracker(len(files))
        for file in files:
            if file.endswith('.csv') and file != master_edge_list_name+'.csv':
                with open(input_folder_name+'/'+file, 'r') as f:
                    reader=csv.reader(f)
                    with open(output_folder_name+'/'+file, 'w') as f1:
                        writer = csv.writer(f1)
                        new_row = []
                        for row in reader:
                            for entry in row:
                                z = (abs(float(entry)) - edge_mean)/edge_sd
                                p = 1 - norm.cdf(z)
                                if p < alpha:
                                    new_row.append(1)
                                else:
                                    new_row.append(0)
                            writer.writerow(new_row)
                            new_row = []
                self.__process_tracker()

    def split_patient_control(self, input_folder: str, output_folder_patient: str, output_folder_control: str):
        '''This method splits the data into patient and control groups. It creates a new directory for the split files.\n
        inputs:\n
            input_folder_name: str - the name of the folder containing the .mat files\n
            output_folder_name: str - the name of the folder to save the split files\n
            patient_control: str - 'patient' or 'control' to specify which group to split by'''
        if os.path.exists(input_folder):
            for file in os.listdir(input_folder):
                if file != '.DS_Store':
                    for inner_file in os.listdir(os.path.join(input_folder, file)):
                        if inner_file.endswith('AAL116_correlation_matrix.mat'):
                            print(f"Processing file: {inner_file}")
                            if 'patient' in file:
                                if not os.path.exists(output_folder_patient):
                                    os.makedirs(output_folder_patient)
                                    print(f"Directory '{output_folder_patient}' created")
                                elif not os.path.exists(os.path.join(output_folder_patient, file)):
                                    os.makedirs(os.path.join(output_folder_patient, file))
                                    print(f"Directory '{output_folder_patient}/{file}' created")
                                subprocess.run(['cp', os.path.join(input_folder, file, inner_file), os.path.join(output_folder_patient, file, inner_file)])
                            elif 'control' in file:
                                if not os.path.exists(output_folder_control):
                                    os.makedirs(output_folder_control)
                                    print(f"Directory '{output_folder_control}' created")
                                elif not os.path.exists(os.path.join(output_folder_patient, file)):
                                    os.makedirs(os.path.join(output_folder_control, file))
                                    print(f"Directory '{output_folder_control}/{file}' created")
                                subprocess.run(['cp', os.path.join(input_folder, file, inner_file), os.path.join(output_folder_control, file, inner_file)])
                            else:
                                print(f"File: '{file}' not copied. No patient or control in file name.")
        else:
            print(f"Directory '{input_folder}' does not exist.")
        print('done')
