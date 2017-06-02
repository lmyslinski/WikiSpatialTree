import logging, gensim
import pickle
import numpy as np

from gensim.models import Doc2Vec
from gensim.similarities import Similarity
from sklearn import manifold
from matplotlib import pyplot as plt



model = Doc2Vec.load("data/simple/models/graph_small.model")

with open('data/simple/models/graph_small.pickle', 'rb') as graph_file:
    g = pickle.load(graph_file)

titles = [g.vp.title[x] for x in g.vertices()]

# print model.docvecs.similarity(titles[0], titles[1])
# print model.docvecs.similarity(titles[1], titles[0])

print g.vp.cat2vec[0].__len__()

dimension = g.num_vertices()

similarity_array = np.zeros((dimension, dimension))

for i in range(0, dimension):
    for j in range(0, dimension):
        similarity_array[i][j] = model.docvecs.similarity(titles[i], titles[j])


# print similarity_array

mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9,
                   dissimilarity="euclidean", n_jobs=1)

pos = mds.fit(similarity_array).embedding_

(x, y) = np.hsplit(pos, 2)

xx = x.flatten()
yy = y.flatten()

print(xx)

# plt.plot(x, y)
plt.plot(xx, yy, 'ro')
for index in range(0, dimension):
    plt.annotate(
        g.vp.title[index],
        xy=(xx[index], yy[index]), xytext=(-20, 20),
        textcoords='offset points', ha='right', va='bottom',
        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
        arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))

plt.show()


# similarity_array = []
#
# for row in range(0, 29):
#     sims = []
#     for column in range (0, 29):
#         sims[column]= model.docvecs.similarity(titles[row], titles[column])

#
# print model.docvecs[g.vp.title[28]]

    # for d in g.vertices():
    #
    #     print(gensim.models.Doc2Vec.similarity(, g.vp.cat2vec[g]))
