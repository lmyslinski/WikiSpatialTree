from graph_tool.all import Graph
import pickle

with open('python_matrix.pickle', 'rb') as handle:
    graph_matrix = pickle.load(handle)

g = Graph()
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

with open('graph.pickle', 'wb') as handle:
    pickle.dump(g, handle)
