import pickle
from preprocessing import builder
from preprocessing.builder import Dataset

# with open('matrix.pickle', 'rb') as handle:
#     matrix = pickle.load(handle)

ds = Dataset("polish", 'data/polish/simple-20120104-cattreeid.twr',
             'data/polish/simple-20120104-titlecat.twr',
             'data/polish/simple-20120104-catlinks.twr',
             'data/polish/simple-20120104-pagetitle.twr', ' ')

ds2 = Dataset("simple", 'data/simple/categories', 'data/simple/simple-20120104-titlecat.twr',
              'data/simple/simple-20120104-catlinks.twr', 'data/simple/simple-20120104-pagetitle.twr', '\t')
matrix = builder.build_matrix(ds)
builder.build_graph(matrix, ds)
