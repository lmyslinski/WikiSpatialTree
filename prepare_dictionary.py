# assign articles
import pickle
from collections import defaultdict

stoplist = set('for a of the and to in is it from that this as its or by has an was with'.split())
replacelist = "\" ( ) . ".split()

with open('data/simple/articles.pickle', 'rb') as articles_file:
    articles = pickle.load(articles_file)

frequency = defaultdict(int)

for key, article in articles.iteritems():
    # Separate the title from the article
    lines = articles[key].split('\n\n')
    title = lines[0].replace('\n', '')
    # Remove quotes
    words = str.join('\n', lines[1:]).lower().translate(None, ''.join(replacelist)).split()
    # Remove common words
    words = [word for word in words if word not in stoplist]
    # Count each word occurence
    # for word in words:
    #     frequency[word] += 1
    # Save the new dict item
    articles[key] = str.join(' ', words)

# Only keep words that occur more than once
# for key, (title, article) in articles.iteritems():
#     articles[key] = (title, [word for word in article if frequency[word] > 1])

with open('data/simple/articles_parsed.pickle', 'wb') as handle:
    pickle.dump(articles, handle, protocol=pickle.HIGHEST_PROTOCOL)