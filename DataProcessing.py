from scipy.io import loadmat
import numpy as np
import json
import os 
import time

class DataProcessing:
    def __init__(self):
        self.__start = float
        self.__counter = int
        self.__total = int
        pass

    def start_process_tracker(self, total):
        self.__total = total
        self.__start = time.time()
        self.__counter = 0

    def process_tracker(self):
        self.__counter += 1
        print(f'{round((self.__counter/(len(self.__total)-1)*100), 2)}% done')
        time_remaining = round((len(self.__total)-1)*((time.time()-self.__start)/self.__counter) - (time.time()-self.__start), 2)
        print(f'{time_remaining} seconds remaining')

    def convert_to_json_compatible(self, matrix):
        for key in matrix.keys():
            if isinstance(matrix[key], np.ndarray):
                matrix[key] = [[float(y) for y in x] for x in matrix[key]]
            if isinstance(matrix[key], bytes):
                matrix[key] = matrix[key].decode('utf-8')
        return matrix

    def convert_to_json_directory(self, input_folder_name, output_folder_name):
        files = os.listdir(input_folder_name)
        self.start_process_tracker(len(files)-1)
        matrix = {}
        counter = 0
        for outer_file in files:
            if outer_file == '.DS_Store':
                continue
            counter += 1
            inner_files = os.listdir(input_folder_name+'/'+outer_file)
            for inner_file in inner_files:
                if inner_file.endswith('AAL116_correlation_matrix.mat'):
                    matrix = loadmat(os.path.join(input_folder_name, outer_file, inner_file))
                    with open(output_folder_name+'/'+inner_file[:-4]+'.json', 'w') as f:
                        json.dump(self.convert_to_json_compatible(matrix), f, indent=2)
                    self.process_tracker()
        print('done')