import csv, pickle
import os

from graph_tool.all import Graph


def build_matrix():
    graph_matrix = dict()
    print os.getcwd()
    with open('data/simple/categories') as simple_graph:
        reader = csv.reader(simple_graph, delimiter='\t')
        for row in reader:
            row = map(int, row)
            row = filter(lambda a: a != 0, row)
            graph_matrix[row[0]] = row[1:]
    return graph_matrix


def build_graph(graph_matrix):
    g = Graph()
    g.vp.child_count = g.new_vertex_property("int")
    g.vp.article_count = g.new_vertex_property("int")
    g.vp.merged_categories = g.new_vertex_property("vector<int>")
    vertex_to_id_map = dict()

    # generate all the vertex and map them
    for key in graph_matrix:
        v = g.add_vertex()
        vertex_to_id_map[key] = v

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

    with open('graph.pickle', 'wb') as handle:
        pickle.dump(g, handle)
