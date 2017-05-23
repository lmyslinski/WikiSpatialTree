import pickle
import sys
import time
from graph_tool import Graph
from graph_tool.topology import shortest_distance

from app import TreeReducer

import doc2vec

def copyVertex(vertex):
    new_vertex = g2.add_vertex()
    g2.vp.title[new_vertex] = gf.vp.title[vertex]
    g2.vp.articles[new_vertex] = gf.vp.articles[vertex]
    g2.vp.cat2vec[new_vertex] = gf.vp.cat2vec[vertex]

with open('data/simple/graph_final.pickle', 'rb') as handle:
    gf = pickle.load(handle)

g2 = Graph()
g2.vp.title = g2.new_vertex_property("string")
g2.vp.article_count = g2.new_vertex_property("int")
g2.vp.articles = g2.new_vertex_property("vector<string>")
g2.vp.cat2vec = g2.new_vertex_property("vector<float>")
g2.vp.bow = g2.new_vertex_property("object")

categories = ['Geography', 'Engineering', "Computer_science", "Clothing"]

for vertex in gf.vertices():
    if gf.vp.title[vertex] in categories:
        copyVertex(vertex)
        children = [gf.vertex(x.target()) for x in filter(lambda y: y.target() != vertex, vertex.all_edges())]
        for child in children:
            copyVertex(child)


# for vertex in g2.vertices():
#     word_count = g2.articles

model = doc2vec.count_vector(g2)

with open('data/simple/graph_small.pickle', 'wb') as handle:
    pickle.dump(g2, handle)

