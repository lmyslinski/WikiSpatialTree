import pickle
import sys
import time
from graph_tool.topology import shortest_distance

from bag_of_words import bag_of_words
from graph_tool import Graph
from app import TreeReducer

import doc2vec


<<<<<<< HEAD:test.py
with open('data/simple/graph.pickle', 'rb') as handle:
    gf = pickle.load(handle)

# count bag of words category representations
bag_of_words(gf)
=======
with open('data/simple/graph_final.pickle', 'rb') as handle:
    gf = pickle.load(handle)


# count category vectors from articles
doc2vec.count_vector(gf)

# count bag of words category representations
# bag_of_words(gf)
>>>>>>> bb2cc2706018c9b1955cbd187e58485c954c1be7:runDoc2Vec.py
