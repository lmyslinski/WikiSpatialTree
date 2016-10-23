from graph_tool.all import graph_draw
import pickle

with open('graph.pickle', 'rb') as handle:
    g = pickle.load(handle)

graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=6, output="test.png", output_size=(5000,5000))