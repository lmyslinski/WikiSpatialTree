import csv
import os
import pickle

from graph_tool.all import Graph


class Dataset:
    def __init__(self, name, cat_file, cat_title_file, cat_art_count_file, cat_links_file, delimiter):
        self.cat_links_file = cat_links_file
        self.cat_art_count_file = cat_art_count_file
        self.cat_title_file = cat_title_file
        self.cat_file = cat_file
        self.name = name
        self.delimiter = delimiter


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
    g.vp.merged_categories = g.new_vertex_property("vector<int>")
    g.vp.category_links = g.new_vertex_property("vector<int>")
    g.vp.article_links = g.new_vertex_property("vector<int>")
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


    # reverse the dictionary
    id_to_vertex_map = dict((v, k) for k, v in vertex_to_id_map.iteritems())

    # populate the graph with edges
    for key in graph_matrix:
        adjacency_list = graph_matrix[key]
        for edge in adjacency_list:
            g.add_edge(vertex_to_id_map[key], vertex_to_id_map[edge])

    # assign children count
    for vertex in g.vertices():
        for edge in vertex.all_edges():
            if edge.source() == vertex:
                g.vp.child_count[edge.source()] += 1

    # assign article count
    with open(dataset.cat_art_count_file) as cat_articles_file:
        reader = csv.reader(cat_articles_file, delimiter=' ')
        for row in reader:
            title_key = row[0]
            if title_key in title_to_vertex_id_map:
                art_count = int(row[1])
                vertex = title_to_vertex_id_map[title_key]
                g.vp.article_count[vertex] = art_count


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

    with open('graph.pickle', 'wb') as handle:
        pickle.dump(g, handle)