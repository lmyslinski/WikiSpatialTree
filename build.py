import pickle
from preprocessing import builder

with open('matrix.pickle', 'rb') as handle:
    matrix = pickle.load(handle)

builder.build_graph(matrix)