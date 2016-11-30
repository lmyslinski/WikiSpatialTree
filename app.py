from graph_tool.all import graph_draw
from preprocessing import builder
import os
import re
import pickle

pattern = re.compile('|'.join(["stub[_s \ Z]",
                               "(_-\ A)articles(_-\ Z)",
                               "template",
                               "wikipedia \ Z",
                               "(_-\ A)disambiguation(_-\ Z)",
                               "(_-\ A)(deaths-births)(_-\ Z)",
                               "(_-\ A) \ d+s?(_BC)?(_-\ Z)",
                               "years",
                               "(_-\ A)century(_-\ Z)",
                               "(_-\ A)(millennia-millennium)(_-\ Z)",
                               "(_-\ A)(unknown-uncertain)(_-\ Z)",
                               ". * _language_films. *",
                               "_by_year",
                               "_century",
                               "_shot_in",
                               "female_",
                               "male_",
                               "with_proper_names",
                               "people_who",
                               "Albums_with_cover_art_by_",
                               "speaking_countries",
                               "alumni",
                               "_screenwriters"]))

list_pattern = re.compile('|'.join([".*_by_"]))


def get_most_important_parent(vertex, parents):
    best_parent = parents[0]
    if parents.__len__() > 1:
        min_distance = 10000
        for parent in parents:
            common_links = list(set(g.vp.category_links[vertex]).intersection(g.vp.category_links[parent]))
            distance = common_links.__len__()
            if distance < min_distance:
                min_distance = distance
                best_parent = parent
    return best_parent


def filter_by_name(title):
    return re.search(pattern, title) is not None


def filter_by_list_pattern(title):
    return re.search(list_pattern, title) is not None


def get_parents_children(vertex, edges):
    parents = [g.vertex(x.source()) for x in filter(lambda y: y.target() == vertex, edges)]
    children = [g.vertex(x.target()) for x in filter(lambda y: y.target() != vertex, edges)]
    return parents, children


# filter parents to exclude parent-child cycles
def get_parents_without_cycles(vertex, edges):
    return [x for x in filter(lambda p: p not in children, parents)]


def get_leftover_edges(vertex, edges, parent):
    return [x for x in filter(lambda y: y.target() == vertex and y.source() != parent, edges)]


def merge_vertex(vertex, edges, parents, children):
    deletion_list.append(vertex)
    parent = get_most_important_parent(vertex, parents)
    g.vp.merged_categories[parent].append(vertex)
    g.vp.article_count[parent] += g.vp.article_count[vertex]
    for child in children:
        if g.edge(parent, child) is None:
            g.add_edge(parent, child, add_missing=True)
    for edge in edges:
        g.remove_edge(edge)


def match_criteria(vertex):
    return g.vp.child_count[vertex] < 10 or g.vp.article_count[vertex] < 5 or filter_by_name(g.vp.title[vertex])


def match_list(vertex):
    return filter_by_list_pattern(g.vp.title[vertex])


if not os.path.exists('graph.pickle'):
    print "Graph not found, generating..."
    matrix = builder.build_matrix()
    builder.build_graph(matrix)
    print "Done"

with open('graph.pickle', 'rb') as handle:
    g = pickle.load(handle)
    print "Graph loaded"

# merge categories with less than 5 subcategories with their parents
deletion_list = []
for vertex in g.vertices():
    edges = list(vertex.all_edges())
    parents, children = get_parents_children(vertex, edges)
    if parents.__len__() != 0 and match_criteria(vertex):
        merge_vertex(vertex, edges, parents, children)

# if more than 1 parent, choose the more important
for vertex in g.vertices():
    edges = list(vertex.all_edges())
    parents, children = get_parents_children(vertex, edges)
    parents_without_children = get_parents_without_cycles(parents, children)
    if parents.__len__() > 1:
        best_parent = get_most_important_parent(vertex, parents_without_children)
        leftover_parent_edges = get_leftover_edges(vertex, edges, best_parent)
        map(g.remove_edge, leftover_parent_edges)

# create category "Lists" as a parent for all lists
lists = g.add_vertex()
g.vp.title[lists] = "LISTS"
for vertex in g.vertices():
    if match_list(vertex):
        g.add_edge(lists, vertex)

# remove orphaned categories
for v in reversed(sorted(deletion_list)):
    g.remove_vertex(v)


print "Finished processing"
print "Generating graph..."
graph_draw(g, vertex_text=g.vp.title, vertex_font_size=10, output="result.png", output_size=(5000, 5000))
print "Done"
