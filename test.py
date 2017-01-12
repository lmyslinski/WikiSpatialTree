import pickle
import sys
import time
from graph_tool.topology import shortest_distance

# with open('data/simple/graph.pickle', 'rb') as handle:
#     g = pickle.load(handle)

with open('data/simple/graph_final.pickle', 'rb') as handle:
    g= pickle.load(handle)

ix = 0
glen = list(g.vertices()).__len__()

for vertex in g.vertices():
    sd = shortest_distance(g, source=vertex, directed=False)
    p = [x for x in filter(lambda p: p != 2147483647, sd)]
    sump = sum(p)
    g.vp.harmonic_centrality[vertex] = 1 / float(sump) if sump != 0 else 0
    print(str(ix) + "/" + str(glen))
    ix += 1


for vertex in g.vertices():
    print str(vertex) + " " + g.vp.title[vertex] + " " + str(g.vp.harmonic_centrality[vertex])

# c_gf = [(gf.vp.harmonic_centrality[x], x) for x in gf.vertices()]
# c_g = [(g.vp.harmonic_centrality[x], x) for x in g.vertices()]




#
#
with open('data/simple/graph_final.pickle', 'wb') as handle:
    pickle.dump(g, handle)


# with open('data/polish/graph_final.pickle', 'rb') as handle:
#     g = pickle.load(handle)
#
# ix=0
# glen = list(g.vertices()).__len__()
#
# for vertex in g.vertices():
#     sd = shortest_distance(g, source=vertex, directed=False)
#     p = [x for x in filter(lambda p: p != 2147483647, sd)]
#     sump = sum(p)
#     g.vp.harmonic_centrality[vertex] = 1 / float(sump) if sump != 0 else 0
#     print(str(ix) + "/" + str(glen))
#     ix += 1
#
# with open('data/polish/graph_final.pickle', 'wb') as handle:
#     pickle.dump(g, handle)