import pickle
import sys
import time
from graph_tool.topology import shortest_distance

from app import TreeReducer


def get_children(g, vertex):
    return sorted([g.vertex(x.target()) for x in filter(lambda y: y.target() != vertex, list(vertex.all_edges()))],key=lambda z: g.vp.title[z], reverse=True)

with open('data/polish/graph.pickle', 'rb') as handle:
    gf = pickle.load(handle)


tr = TreeReducer("")
tr.g = gf
# tr.mark_categories_for_deletion()
# tr.delete_categories()
tr.reduce_to_single_parent()
tr.extract_lists()
tr.calculate_children_count()
tr.merge_by_criteria(5, 10)
# tr.delete_categories()
# tr.calculate_centrality()

with open('data/polish/graph_final.pickle', 'wb') as handle:
    pickle.dump(gf, handle)
