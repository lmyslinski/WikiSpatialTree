from graph_tool.all import *
import pickle

with open('python_matrix.pickle', 'rb') as handle:
    graph_matrix = pickle.load(handle)


Graph g = new Graph()

for key, value_list in graph_matrix:
