import pickle

from graph_tool.draw import graph_draw


with open('data/simple/graph_final.pickle', 'rb') as handle:
    gf = pickle.load(handle)

graph_draw(gf, vertex_text=gf.vp.title, vertex_font_size=10, output="result.png", output_size=(5000, 5000))