from bs4 import BeautifulSoup
from os import listdir
from os.path import join
import cPickle as pickle

path = 'data/simple/articles'

articles = dict()
for f in listdir(path):
    filepath = join(path, f)
    soup = BeautifulSoup(open(filepath), 'lxml')
    docs = soup.findAll("doc")
    for doc in docs:
        content = unicode(doc.contents[0])
        articles[doc.get('title')] = content
    print ("Parsed " + filepath)

print articles.__len__()
with open('data/simple/articles.pickle', 'wb') as handle:
    pickle.dump(articles, handle, protocol=pickle.HIGHEST_PROTOCOL)