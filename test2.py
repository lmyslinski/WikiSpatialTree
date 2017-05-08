import pickle
import sys
import time

from gensim.models import Word2Vec
from graph_tool.topology import shortest_distance, min_spanning_tree

from graph_tool.draw import graph_draw, radial_tree_layout, arf_layout, fruchterman_reingold_layout, planar_layout, \
    sfdp_layout
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
g.ep.visible = g.new_edge_property("bool")

for vertex in g.vertices():
    title_to_vertex_id_map[g.vp.title[vertex]] = vertex
    vertex_to_id_map[vertex] = g.vp.title[vertex]

for vertex in g.vertices():
    d = model.docvecs.most_similar(g.vp.title[vertex], topn=3)
    vertitle = g.vp.title[vertex]
    art1 = g.vp.articles[vertex]
    for tuple in d:
        art2 = g.vp.articles[title_to_vertex_id_map[tuple[0]]]
        title = tuple[0]
        similarity = tuple[1]
        if title in title_to_vertex_id_map:
            edge = g.add_edge(vertex, title_to_vertex_id_map[title])
            g.ep.weight[edge] = similarity
            # g.ep.visible[edge] = True if (similarity > 0.9) else False

print("Drawing...")
# tree = min_spanning_tree(g)

# g.set_edge_filter(g.ep.visible)
pos = sfdp_layout(g)
graph_draw(g, vertex_text=g.vp.title, pos=pos, vertex_font_size=8,  output="3nodes.png", output_size=(5000, 5000))
