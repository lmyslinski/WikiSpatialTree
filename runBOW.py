import pickle
import sys
import time
from graph_tool.topology import shortest_distance

from bag_of_words import bag_of_words
from app import TreeReducer


with open('data/simple/graph.pickle', 'rb') as handle:
    gf = pickle.load(handle)

# count bag of words category representations
bag_of_words(gf)