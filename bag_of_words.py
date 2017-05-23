import logging, gensim
import cPickle as pickle
import string
from graph_tool import Graph

import numpy as np
from gensim import corpora
from scipy.linalg import norm

from gensim.similarities import Similarity

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def get_children(g, vertex, edges):
    return [g.vertex(x.target()) for x in filter(lambda y: y.target() != vertex, edges)]



def build_bow(graph):
    docs = []

    for vertex in graph.vertices():
        articles_text = ""
        for article in graph.vp.articles[vertex]:
            articles_text = articles_text + article

        docs.append(articles_text.split())

    # create & save a dictionary

    # # remove common words and tokenize
    stoplist = set('for a of the and to in'.split())
    texts = [[word for word in document if word not in stoplist]
             for document in docs]
    #
    # # remove words that appear only once
    from collections import defaultdict
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1] for text in texts]
    dictionary = corpora.Dictionary(texts)
    for vertex in graph.vertices():
        category_articles = string.join(graph.vp.articles[vertex]).split()
        graph.vp.bow[vertex] = dictionary.doc2bow(category_articles)
    dictionary.save('/tmp/bag_of_words.dict')
    corpus = [graph.vp.bow[vertex] for vertex in graph.vertices()]
    index = Similarity('/tmp/tst', corpus=corpus, num_features=dictionary.__len__())
    with open('data/simple/graph_small.pickle', 'wb') as handle:
        pickle.dump(graph, handle)

    print graph.vp.title[10]
    similarities = np.sort(index.similarity_by_id(10))[::-1]
    for i in range(0, similarities.__len__()):
        print(graph.vp.title[i] + " " + str(similarities[i]))







def loadBow(graph):

    # load saved dictionary
    dictionary = corpora.Dictionary.load('/tmp/bag_of_words.dict')
    dictionary.compactify()

    # for c in corpus:
    #     print(c)
      # build the index
    # print(dictionary)

    # for vertex in graph.vertices():
    #     print(graph.vp.bow[vertex])
    #
    # categories = ['Geography', 'Engineering', "Computer_science", "Clothing"]
    # bows = []
    #
    # for vertex in graph.vertices():
    #     if graph.vp.title[vertex] in categories:
    #         bows.append(graph.vp.bow[vertex])
    #
    # print 'Geography - Engineering'
    # print cosine_sim(bows[0],bows[1])
    #
    # print 'Geography - Clothing'
    # print cosine_sim(bows[0],bows[3])



with open('data/simple/graph_small.pickle', 'rb') as handle:
    gf = pickle.load(handle)

    build_bow(gf)
    # loadBow(gf)

