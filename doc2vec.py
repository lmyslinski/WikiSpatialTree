import logging, gensim
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

LabeledSentence = gensim.models.doc2vec.LabeledSentence

class LabeledLineSentence(object):
    def __init__(self, doc_list, labels_list):
       self.labels_list = labels_list
       self.doc_list = doc_list
    def __iter__(self):
        # for idx, doc in enumerate(self.doc_list):
        #     yield LabeledSentence(words=doc.split(), labels=[self.labels_list[idx]])
        yield LabeledSentence(words=self.doc_list,tags=self.labels_list)

def count_vector(graph):

    categories_count = graph.num_vertices()

    docLabels = []
    data = []

    # prepare labels and merge articles from vectors
    for vertex in range(categories_count):
        docLabels.append(graph.vp.title[vertex])

        articles_vec = graph.vp.articles[vertex]
        articles = ""
        for par in articles_vec:
            articles = articles + par

        data.append(articles)

    # train the model
    it = LabeledLineSentence(data, docLabels)

    model = gensim.models.Doc2Vec(size=10, window=10, min_count=1, workers=11, alpha=0.025, min_alpha=0.025)  # use fixed learning rate
    model.build_vocab(it)
    for epoch in range(10):
        model.train(it, total_examples=model.corpus_count, epochs=model.iter)
        model.alpha -= 0.002  # decrease the learning rate
        model.min_alpha = model.alpha  # fix the learning rate, no deca
        model.train(it, total_examples=model.corpus_count, epochs=model.iter)

    model.save("doc2vec.model")

    # save vectors in graph
    for vertex in range(categories_count):
        graph.vp.cat2vec[vertex] = model.docvecs[graph.vp.title[vertex]]
        # print graph.vp.cat2vec[vertex]

    print model.docvecs.most_similar('Articles')
    # print len(model.docvecs.offset2doctag)
