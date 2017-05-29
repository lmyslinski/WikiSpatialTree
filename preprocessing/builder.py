import csv
import os
import pickle

from graph_tool.all import Graph

import doc2vec

class Dataset:
    def __init__(self, name, cat_file, cat_title_file, cat_links_file, page_title_file, delimiter, root_title):
        self.cat_links_file = cat_links_file
        self.cat_title_file = cat_title_file
        self.cat_file = cat_file
        self.page_title_file = page_title_file
        self.name = name
        self.delimiter = delimiter
        self.root_title = root_title


def build_matrix(dataset):
    graph_matrix = dict()
    print os.getcwd()
    with open(dataset.cat_file) as simple_graph:
        reader = csv.reader(simple_graph, delimiter=dataset.delimiter)
        for row in reader:
            row = map(int, row)
            row = filter(lambda a: a != 0, row)
            graph_matrix[row[0]] = row[1:]
    return graph_matrix


def build_graph(graph_matrix, dataset):
    g = Graph()
    g.vp.child_count = g.new_vertex_property("int")
    g.vp.title = g.new_vertex_property("string")
    g.vp.article_count = g.new_vertex_property("int")
    g.vp.merged_categories = g.new_vertex_property("vector<string>")
    g.vp.rejected_parents = g.new_vertex_property("vector<string>")
    g.vp.category_links = g.new_vertex_property("vector<int>")
    g.vp.articles = g.new_vertex_property("vector<string>")
    g.vp.cat2vec = g.new_vertex_property("vector<float>")
    g.vp.harmonic_centrality = g.new_vertex_property("float")
    g.vp.bow = g.new_vertex_property("object")
    vertex_to_id_map = dict()
    title_to_vertex_id_map = dict()

    # generate all vertex
    with open(dataset.cat_title_file) as titlecat_file:
        reader = csv.reader(titlecat_file, delimiter=' ')
        for row in reader:
            key = int(row[1])
            vertex = g.add_vertex()
            vertex_to_id_map[key] = vertex
            title = row[0]
            title_to_vertex_id_map[title] = vertex
            g.vp.title[vertex] = title

    #populate the graph with edges
    for key in graph_matrix:
        adjacency_list = graph_matrix[key]
        for edge in adjacency_list:
            g.add_edge(vertex_to_id_map[key], vertex_to_id_map[edge])

    all_articles_map = dict()
    with open(dataset.page_title_file) as page_title_file:
        reader = csv.reader(page_title_file, delimiter=' ')
        for row in reader:
            all_articles_map[int(row[0])] = row[1]

    # assign articles
    with open('data/simple/models/articles_parsed.pickle', 'rb') as articles_file:
        articles = pickle.load(articles_file)
        with open(dataset.cat_links_file) as cat_links_file:
            reader = csv.reader(cat_links_file, delimiter=' ')
            for row in reader:
                key = int(row[0])
                vertex = g.vertex(vertex_to_id_map[key])
                if key in vertex_to_id_map:
                    for i in range(1, row.__len__()):
                        article_key = int(row[i])
                        if article_key in articles:
                            article = articles[int(row[i])]
                            g.vp.articles[vertex].append(article)


    # assign category links
    with open(dataset.cat_links_file) as cat_links_file:
        reader = csv.reader(cat_links_file, delimiter=' ')
        for row in reader:
            key = int(row[0])
            if key in vertex_to_id_map:
                vertex = g.vertex(vertex_to_id_map[key])
                g.vp.category_links[vertex] = row[1:]

    # assign children count
    for vertex in g.vertices():
        for edge in vertex.all_edges():
            if edge.source() == vertex:
                g.vp.child_count[edge.source()] += 1

    with open('data/' + dataset.name + '/graph.pickle', 'wb') as handle:
        pickle.dump(g, handle)