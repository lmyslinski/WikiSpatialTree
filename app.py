import os
from graph_tool.all import graph_draw
from preprocessing import builder
import pickle


def get_parent_children(vertex, edges):
    parents = [g.vertex(x.source()) for x in filter(lambda y: y.target() == vertex, edges)]
    children = [g.vertex(x.target()) for x in filter(lambda y: y.target() != vertex, edges)]
    return parents, children


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
    parents, children = get_parent_children(vertex, edges)
    if g.vp.child_count[vertex] < 5 and parents is not None:
        # TODO how to handle many parents?
        if children is None:
            g.vp.merged_categories[parents[0]].append(vertex)
            g.remove_edge(edges[0])
            deletion_list.append(vertex)
            # do sth with children

# remove orphaned categories
for v in reversed(sorted(deletion_list)):
    g.remove_vertex(v)

print "Finished processing"
print "Generating graph..."
graph_draw(g, vertex_text=g.vp.child_count, vertex_font_size=10, output="test2.png", output_size=(5000, 5000))
print "Done"
