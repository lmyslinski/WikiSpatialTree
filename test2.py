import pickle
import sys
import time

from gensim.models import Word2Vec
from graph_tool.topology import shortest_distance

from app import TreeReducer

import doc2vec




# count category vectors from articles
# print

with open('data/simple/graph_final.pickle', 'rb') as handle:
    g = pickle.load(handle)

for vertex in g.vertices():
    edges = vertex.all_edges()
    for e in edges:
        # print e
        g.remove_edge(e)


model = Word2Vec.load("doc2vec.model")


vertex_to_id_map = dict()
title_to_vertex_id_map = dict()
g.ep.weight = g.new_edge_property("double")

for vertex in g.vertices():
    title_to_vertex_id_map[g.vp.title[vertex]] = vertex
    vertex_to_id_map[vertex] = g.vp.title[vertex]

for vertex in g.vertices():
    d = model.docvecs.most_similar(g.vp.title[vertex])
    vertitle = g.vp.title[vertex]
    art1 = g.vp.articles[vertex]
    for tuple in d:
        art2 = g.vp.articles[title_to_vertex_id_map[tuple[0]]]
        title = tuple[0]
        similarity = tuple[1]
        if title in title_to_vertex_id_map:
            edge = g.add_edge(vertex, title_to_vertex_id_map[title])
            g.ep.weight[edge] = similarity

exit
# delete all the edges

# add nearest