# BrainNetworkResearch
This repository contains all of the code written and used over the course of my senior research project.  To avoid any licensing conflicts, none of the data used during the project will be uploaded to github. Instead, The dataset will be linked below. Additionally, a breif overview of each module will be given here. More information can be found in the modules themselves, which are commented extensively for clarity of use.

Data Set:
1. neurocon ==> [](https://auckland.figshare.com/articles/dataset/NeurIPS_2022_Datasets/21397377?file=37988397 )
    -- this paper also contains several other datasets, all of which should be compatible with this code.

Modules:
1. DataProcessing ==> This is a module containing a class for processing corellation matrices in .mat format. It can convert these to .json and .csv, and perform global thresholding and binarization on them.
2. GraphConstructor ==> This is a module containing a class for constructing graphs using NetworkX based on the matrices generated from the DataProcessing module.
3. GraphAnalysis ==> This is a module for analyzing the graphs created by the GraphConstructor module. Among other things, it calculates the small world coefficient of the graphs by comparing the clustering coefficients and characteristic path lengths to that of a randomly generated Erdos-Renyi graph with the same number of nodes and edges.
4. DataVisualization ==> This is a module containing a class for visualizing the data that can be generated using the previous modules. The current set up of main.py creates a final dataset of graph stats for each graph in the patient and control group, which can then be visualized using this module.
5. lin_alg_module ==> This is a module containing a class used for various Linear Algebra applications. It was written seperately from this research. However, it was used in some parts. Feel free to use it. It can be quite useful, but most of its functionality is well outside the scope of this research.

Usage Tips:
    -- main.py is currently set up to take input directory of thresholded adjacency matrices (specified on line 67) and output a csv file (specified on line 68) containing statistics about all of the graphs generated from them. If you want to use this functionality with new data, you will have to preprocess it (convert file types, split the patient and control group, perform thresholding, ...etc.) There is code to do this in main.py; it is currently commented out.
    -- If you are using this code, I am assuming you have the same research advisor that I did. If so, your advisor has my contact info. If you have truly unanswerable questions about this code, read the paper that goes along with then code, then feel free to get that info and contact me. Full disclosure, I may or may not respond (depends on how busy I am), and I am not going to be a impromptu research advisor. That being said-- good luck. I do hope you find this helpful.
