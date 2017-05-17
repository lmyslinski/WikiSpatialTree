import logging, gensim
import cPickle as pickle
from graph_tool import Graph
from gensim import corpora
from scipy.linalg import norm
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def get_children(g, vertex, edges):
    return [g.vertex(x.target()) for x in filter(lambda y: y.target() != vertex, edges)]

def bag_of_words(graph):

    docs = []

    for vertex in graph.vertices():
        articles_text = ""
        for article in graph.vp.articles[vertex]:
            articles_text = articles_text + article

        docs.append(articles_text.split())

    # # create & save a dictionary
    #
    # # remove common words and tokenize
    # stoplist = set('for a of the and to in'.split())
    # texts = [[word for word in document.words if word not in stoplist]
    #          for document in docs]
    #
    # # remove words that appear only once
    # from collections import defaultdict
    # frequency = defaultdict(int)
    # for text in texts:
    #     for token in text:
    #         frequency[token] += 1
    #
    # texts = [[token for token in text if frequency[token] > 1] for text in texts]
    #
    # dictionary = corpora.Dictionary(texts)
    # dictionary.save('/tmp/bag_of_words.dict')

    # load saved dictionary
    dictionary = corpora.Dictionary.load('/tmp/bag_of_words.dict')
    print(dictionary)

    for vertex in graph.vertices():
        graph.vp.bow[vertex] = dictionary.doc2bow(docs[int(vertex)])
        print vertex



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



