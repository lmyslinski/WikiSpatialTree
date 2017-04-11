import pickle
import sys
import time
from graph_tool.topology import shortest_distance

from app import TreeReducer

import doc2vec

def get_children(g, vertex):
    return sorted([g.vertex(x.target()) for x in filter(lambda y: y.target() != vertex, list(vertex.all_edges()))],key=lambda z: g.vp.title[z], reverse=True)

with open('data/simple/graph_final.pickle', 'rb') as handle:
    gf = pickle.load(handle)


# count category vectors from articles
    doc2vec.count_vector(gf)

