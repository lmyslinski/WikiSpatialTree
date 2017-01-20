import pickle
from preprocessing import builder
from preprocessing.builder import Dataset

# with open('matrix.pickle', 'rb') as handle:
#     matrix = pickle.load(handle)

ds = Dataset("polish", 'data/polish/pl-20170101-cattreeid.twr',
             'data/polish/pl-20170101-titlecat.twr',
             'data/polish/pl-20170101-catlinks.twr',
             'data/polish/pl-20170101-pagetitle.twr', ' ')

ds2 = Dataset("simple", 'data/simple/categories', 'data/simple/simple-20120104-titlecat.twr',
              'data/simple/simple-20120104-catlinks.twr', 'data/simple/simple-20120104-pagetitle.twr', '\t')

builder.build_graph(builder.build_matrix(ds), ds)
builder.build_graph(builder.build_matrix(ds2), ds2)
