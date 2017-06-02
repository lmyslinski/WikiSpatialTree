import pickle
from graph_tool import Graph
from sklearn import manifold
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

import doc2vec

def copyVertex(vertex):
    new_vertex = g.add_vertex()
    g.vp.title[new_vertex] = gf.vp.title[vertex]
    g.vp.articles[new_vertex] = gf.vp.articles[vertex]
    g.vp.cat2vec[new_vertex] = gf.vp.cat2vec[vertex]

def plot(similarity_array, title):
    pos = mds.fit(similarity_array).embedding_
    (x, y) = np.hsplit(pos, 2)
    x = x.flatten()
    y = y.flatten()
    df = pd.DataFrame(dict(x=x, y=y, label=parent_titles))
    groups = df.groupby('label')
    fig, ax = plt.subplots()
    ax.margins(0.05)  # Optional, just adds 5% padding to the autoscaling
    plt.title(title)
    for name, group in groups:
        ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, label=name)

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), numpoints=1)


with open('data/simple/graph_final.pickle', 'rb') as handle:
    gf = pickle.load(handle)

g = Graph()
g.vp.title = g.new_vertex_property("string")
g.vp.article_count = g.new_vertex_property("int")
g.vp.articles = g.new_vertex_property("vector<string>")
g.vp.cat2vec = g.new_vertex_property("vector<float>")
g.vp.bow = g.new_vertex_property("object")

categories = ['Education', 'Everyday_life', "Geography", "History", "Literature", "People", "Religion", "Science"]
categories_map = dict()

for vertex in gf.vertices():
    if gf.vp.title[vertex] in categories:
        copyVertex(vertex)
        categories_map[gf.vp.title[vertex]] = gf.vp.title[vertex]
        children = [gf.vertex(x.target()) for x in filter(lambda y: y.target() != vertex, vertex.all_edges())]
        for child in children:
            categories_map[gf.vp.title[child]] = gf.vp.title[vertex]
            copyVertex(child)

parent_titles = [categories_map[g.vp.title[x]] for x in g.vertices()]
mds = manifold.MDS(n_components=2, n_init=100, max_iter=3000, eps=1e-9, dissimilarity="euclidean", n_jobs=-1)


print("Category count: %d" % g.num_vertices())
print("Article count: %d" % np.sum([g.vp.articles[vertex].__len__() for vertex in g.vertices()]))

#Doc2Vec
plot(doc2vec.doc2vec(g, True), "Doc2Vec recursive")
plot(doc2vec.doc2vec(g, False), "Doc2Vec non-recursive")

#Bow
plot(doc2vec.bow(g, True), "Bow recursive")
plot(doc2vec.bow(g, False), "Bow non-recursive")

#Show plots
plt.show()