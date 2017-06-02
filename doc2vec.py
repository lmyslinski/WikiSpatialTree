import logging, gensim
from gensim.similarities import Similarity
from gensim import corpora
from collections import defaultdict
import string
import numpy as np

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

TaggedDocument = gensim.models.doc2vec.TaggedDocument


def get_children(g, vertex):
    edges = vertex.all_edges()
    return [g.vertex(x.target()) for x in filter(lambda y: y.target() != vertex, edges)]

def doc2vec(graph, with_children=False):

    docs = []

    if with_children:
        for vertex in graph.vertices():
            articles_text = ""
            for article in graph.vp.articles[vertex]:
                articles_text = articles_text + article

            docs.append(TaggedDocument(words=articles_text.split(), tags=[graph.vp.title[vertex]]))
    else:
        for vertex in graph.vertices():
            articles_text = ""
            for article in graph.vp.articles[vertex]:
                articles_text = articles_text + article
            for child in get_children(graph, vertex):
                for article in graph.vp.articles[vertex]:
                    articles_text = articles_text + article

            docs.append(TaggedDocument(words=articles_text.split(), tags=[graph.vp.title[vertex]]))

    model = gensim.models.doc2vec.Doc2Vec(docs, size=100, window=10, min_count=1, workers=8, alpha=0.025, min_alpha=0.025)

    for epoch in range(10):
        print("Training phase: %d out of %d" % (epoch,10) )
        model.train(docs, total_examples=model.corpus_count, epochs=model.iter)
        model.alpha -= 0.002
        model.min_alpha = model.alpha

    dimension = graph.num_vertices()
    similarity_array = np.zeros((dimension, dimension))

    titles = [graph.vp.title[x] for x in graph.vertices()]

    for i in range(0, dimension):
        for j in range(0, dimension):
            similarity_array[i][j] = model.docvecs.similarity(titles[i], titles[j])

    return similarity_array


def bow(graph, with_children=False):
    docs = []

    if with_children:
        for vertex in graph.vertices():
            articles_text = ""
            for article in graph.vp.articles[vertex]:
                articles_text = articles_text + article
            docs.append(articles_text.split())
    else:
        for vertex in graph.vertices():
            articles_text = ""
            for article in graph.vp.articles[vertex]:
                articles_text = articles_text + article
            for child in get_children(graph, vertex):
                for article in graph.vp.articles[vertex]:
                    articles_text = articles_text + article
            docs.append(articles_text.split())

    # # remove common words and tokenize
    stoplist = set('for a of the and to in'.split())
    texts = [[word for word in document if word not in stoplist]
             for document in docs]
    #
    # # remove words that appear only once

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

    dimension = graph.num_vertices()
    similarity_array = np.zeros((dimension, dimension))
    for i in range(0, dimension):
        similarity_array[i] = index.similarity_by_id(i)

    return similarity_array