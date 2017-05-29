import logging, gensim
import pickle

from gensim.models import Doc2Vec
from gensim.similarities import Similarity

model = Doc2Vec.load("data/simple/models/graph_small.model")

with open('data/simple/models/graph_small.pickle', 'rb') as graph_file:
    g = pickle.load(graph_file)

for v in g.vertices():
    print(g.vp.cat2vec[v])

print model.size
    # for d in g.vertices():

        # print(gensim.models.Doc2Vec.similarity(, g.vp.cat2vec[g]))
