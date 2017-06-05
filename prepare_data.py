from os.path import join

from bs4 import BeautifulSoup
from os import listdir

import cPickle as pickle

from pathlib2 import Path
# assign articles
import pickle
from collections import defaultdict

from app import TreeReducer

path = 'data/simple/articles'
articles = dict()

if Path("data/simple/models/articles.pickle").exists():
    print("Extracted articles found, skipping extraction")
else:
    for f in listdir(path):
        filepath = join(path, f)
        soup = BeautifulSoup(open(filepath), 'lxml')
        docs = soup.findAll("doc")
        for doc in docs:
            content = (unicode(doc.contents[0])).encode('utf-8')
            articles[int(doc.get('id'))] = content
        print ("Parsed " + filepath)

    print articles.__len__()
    with open('data/simple/models/articles.pickle', 'wb') as handle:
        pickle.dump(articles, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("Extracted articles")

if Path("data/simple/models/articles_parsed.pickle").exists():
    print("Parsed articles found, skipping parsing")
else:
    stoplist = set(
        "a about above after again against all am an and any are aren't as at be because been before being below between both but by can't cannot could couldn't did didn't do does doesn't doing don't down during each few for from further had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers herself him himself his how how's i i'd i'll i'm i've if in into is isn't it it's its itself let's me more most mustn't my myself no nor not of off on once only or other ought our ours ourselves out over own same shan't she she'd she'll she's should shouldn't so some such than that that's the their theirs them themselves then there there's these they they'd they'll they're they've this those through to too under until up very was wasn't we we'd we'll we're we've were weren't what what's when when's where where's which while who who's whom why why's with won't would wouldn't you you'd you'll you're you've your yours yourself yourselves".split())
    replacelist = "\" ( ) . ".split()

    with open('data/simple/models/articles.pickle', 'rb') as articles_file:
        articles = pickle.load(articles_file)

    frequency = defaultdict(int)

    for key, article in articles.iteritems():
        # Separate the title from the article
        lines = articles[key].split('\n\n')
        title = lines[0].replace('\n', '')
        # Remove quotes
        words = str.join('\n', lines[1:]).lower().translate(None, ''.join(replacelist)).split()
        # Remove common words
        words = [word for word in words if word not in stoplist]
        # Count each word occurence
        # for word in words:
        #     frequency[word] += 1
        # Save the new dict item
        articles[key] = str.join(' ', words)

    # Only keep words that occur more than once
    # for key, (title, article) in articles.iteritems():
    #     articles[key] = (title, [word for word in article if frequency[word] > 1])
    with open('data/simple/models/articles_parsed.pickle', 'wb') as handle:
        pickle.dump(articles, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("Parsed articles")

from preprocessing import builder
from preprocessing.builder import Dataset

if Path("data/simple/models/graph.pickle").exists():
    print("Base graph found, skipping building")
else:
    ds = Dataset("simple", 'data/simple/categories', 'data/simple/simple-20120104-titlecat.twr',
                 'data/simple/simple-20120104-catlinks.twr',
                 'data/simple/simple-20120104-pagetitle.twr',
                 '\t', "Articles")

    builder.build_graph(builder.build_matrix(ds), ds)
    print("Base graph built")
    # builder.build_graph(builder.build_matrix(ds2), ds2)

if Path("data/simple/models/graph_final.pickle").exists():
    print("Final graph found, skipping reduction")
else:
    tr = TreeReducer(ds)

    with open('data/simple/graph.pickle', 'rb') as handle:
        tr.g = pickle.load(handle)

    tr.remove_unconnected_categories()
    tr.reduce_to_single_parent()
    tr.remove_matched_categories()
    tr.calculate_children_count()
    tr.merge_by_criteria(5, 10)
    tr.delete_just_to_be_sure()
    print ("Reduction done")
    with open('data/simple/models/graph_final.pickle', 'wb') as handle:
        pickle.dump(tr.g, handle)
    print("Graph reduced")

if Path("data/simple/models/graph_small.pickle").exists():
    print("Small graph found, skipping copying")
else:
    import pickle
    import sys
    import time
    from graph_tool import Graph
    from graph_tool.topology import shortest_distance

    from app import TreeReducer

    import doc2vec


    def copyVertex(vertex):
        new_vertex = g2.add_vertex()
        g2.vp.title[new_vertex] = gf.vp.title[vertex]
        g2.vp.articles[new_vertex] = gf.vp.articles[vertex]
        g2.vp.cat2vec[new_vertex] = gf.vp.cat2vec[vertex]


    with open('data/simple/models/graph_final.pickle', 'rb') as handle:
        gf = pickle.load(handle)

    g2 = Graph()
    g2.vp.title = g2.new_vertex_property("string")
    g2.vp.article_count = g2.new_vertex_property("int")
    g2.vp.articles = g2.new_vertex_property("vector<string>")
    g2.vp.cat2vec = g2.new_vertex_property("vector<float>")
    g2.vp.bow = g2.new_vertex_property("object")

    categories = ['Geography', 'Engineering', "Computer_science", "Clothing"]

    for vertex in gf.vertices():
        if gf.vp.title[vertex] in categories:
            copyVertex(vertex)
            children = [gf.vertex(x.target()) for x in filter(lambda y: y.target() != vertex, vertex.all_edges())]
            for child in children:
                copyVertex(child)

    # for vertex in g2.vertices():
    #     word_count = g2.articles

    model = doc2vec.doc2vec(g2)

    print("Model trainer")

    with open('data/simple/models/graph_small.pickle', 'wb') as handle:
        pickle.dump(g2, handle)

    print("Created small graph")
