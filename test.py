import pickle

import gensim

model = gensim.models.doc2vec.Doc2Vec.load("doc2vec.model")  # you can continue training with the loaded model!

with open('data/simple/graph_small.pickle', 'rb') as handle:
    g = pickle.load(handle)

print (model.docvecs.most_similar('Geography'))

for vertex in g.vertices():
    print(vertex)