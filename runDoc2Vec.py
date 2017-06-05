import pickle
import doc2vec

with open('data/simple/models/graph_final.pickle', 'rb') as handle:
    gf = pickle.load(handle)

# count category vectors from articles
doc2vec.doc2vec(gf)
