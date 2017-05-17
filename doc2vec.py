import logging, gensim

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

TaggedDocument = gensim.models.doc2vec.TaggedDocument


def get_children(g, vertex, edges):
    return [g.vertex(x.target()) for x in filter(lambda y: y.target() != vertex, edges)]

def count_vector(graph):

    docs = []

    for vertex in graph.vertices():
        articles_text = ""
        for article in graph.vp.articles[vertex]:
            articles_text = articles_text + article

        docs.append(TaggedDocument(words=articles_text.split(), tags=[graph.vp.title[vertex]]))

    model = gensim.models.doc2vec.Doc2Vec(docs, size=100, window=10, min_count=1, workers=11, alpha=0.025, min_alpha=0.025)

    for epoch in range(10):
        model.train(docs, total_examples=model.corpus_count, epochs=model.iter)
        model.alpha -= 0.002
        model.min_alpha = model.alpha

    model.save("doc2vec.model")

    for vertex in graph.vertices():
        graph.vp.cat2vec[vertex] = model.docvecs[graph.vp.title[vertex]]

    print (model.docvecs.most_similar('Geography'))