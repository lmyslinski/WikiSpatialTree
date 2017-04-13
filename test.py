import pickle
import sys
import time
from graph_tool.topology import shortest_distance

from app import TreeReducer

import doc2vec


with open('data/simple/graph_final.pickle', 'rb') as handle:
    gf = pickle.load(handle)


# count category vectors from articles
    doc2vec.count_vector(gf)

