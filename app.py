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
                               "_shot_in",
                               "female_",
                               "male_",
                               "with_proper_names",
                               "people_who",
                               "Albums_with_cover_art_by_",
                               "speaking_countries",
                               "alumni",
                               "_screenwriters"]))


def get_most_important_parent(parents):
    # TODO:
    # calculate semantic distance between articles in each parent and articles in this node
    return max(map(lambda x: (g.vp.article_count[x], x), parents), key=lambda x: x[0])[1]


def filter_by_name(title):
    return re.search(pattern, title) is not None


def get_parents_children(vertex, edges):
    parents = [g.vertex(x.source()) for x in filter(lambda y: y.target() == vertex, edges)]
    children = [g.vertex(x.target()) for x in filter(lambda y: y.target() != vertex, edges)]
    return parents, children


def merge_vertex(vertex, edges, parents, children):
    deletion_list.append(vertex)
    parent = get_most_important_parent(parents)
    g.vp.merged_categories[parent].append(vertex)
    g.vp.article_count[parent] += g.vp.article_count[vertex]
    for child in children:
        if g.edge(parent, child) is None:
            g.add_edge(parent, child, add_missing=True)
    for edge in edges:
        g.remove_edge(edge)


def match_criteria(vertex):
    return g.vp.child_count[vertex] < 10 or g.vp.article_count[vertex] < 5 or filter_by_name(g.vp.title[vertex])

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

# remove orphaned categories
for v in reversed(sorted(deletion_list)):
    g.remove_vertex(v)

print "Finished processing"
print "Generating graph..."
graph_draw(g, vertex_text=g.vp.title, vertex_font_size=10, output="test3.png", output_size=(5000, 5000))
print "Done"
