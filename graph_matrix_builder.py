import csv, pickle

graph_matrix = dict()

with open('simple/categories') as simple_graph:
    reader = csv.reader(simple_graph, delimiter='\t')
    for row in reader:
        row = map(int, row)
        row = filter(lambda a: a != 0, row)
        graph_matrix[row[0]] = row[1:]

with open('python_matrix.pickle', 'wb') as handle:
    pickle.dump(graph_matrix, handle)
