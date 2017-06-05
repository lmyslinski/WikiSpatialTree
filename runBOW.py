import pickle
import sys
import time
from graph_tool.topology import shortest_distance

from bag_of_words import get_bow
from app import TreeReducer


with open('data/simple/graph.pickle', 'rb') as handle:
    gf = pickle.load(handle)

# count bag of words category representations
get_bow(gf)