import logging, gensim
from gensim import corpora
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def get_children(g, vertex, edges):
    return [g.vertex(x.target()) for x in filter(lambda y: y.target() != vertex, edges)]

def getAllChildArticles(g, vertex):
    articles = g.vp.articles[vertex]
    children = get_children(g, vertex, list(vertex.all_edges()))
    for child in children:
        articles.extend(getAllChildArticles(g, child))
    return articles

def bag_of_words(graph):

    docLabels = []
    documents = []

    # prepare labels and merge articles from vectors
    for vertex in graph.vertices():
        docLabels.append(graph.vp.title[vertex])

        articles_vec = getAllChildArticles(graph, vertex)

        articles = ""
        for par in articles_vec:
            articles = articles + par

        documents.append(articles)

    # create & save a dictionary

    # remove common words and tokenize
    # stoplist = set('for a of the and to in'.split())
    # texts = [[word for word in document.lower().split() if word not in stoplist]
    #          for document in documents]
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

    # for vertex in graph.vertices():
        # graph.vp.bow[vertex] = dictionary.doc2bow(documents[vertex].lower().split())



