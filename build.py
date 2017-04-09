from preprocessing import builder
from preprocessing.builder import Dataset

ds = Dataset("simple", 'data/simple/categories', 'data/simple/simple-20120104-titlecat.twr',
                              'data/simple/simple-20120104-catlinks.twr',
                              'data/simple/simple-20120104-pagetitle.twr',
                              '\t', "Articles")

ds2 = Dataset("polish", 'data/polish/pl-20170101-cattreeid.twr',
                              'data/polish/pl-20170101-titlecat.twr',
                              'data/polish/pl-20170101-catlinks.twr',
                              'data/polish/pl-20170101-pagetitle.twr',
                              ' ', "Kategorie")

builder.build_graph(builder.build_matrix(ds), ds)
# builder.build_graph(builder.build_matrix(ds2), ds2)
