import sys
from pymongo import MongoClient
import simple_lda
from os import path
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import copy

with open('MONGOLAB_PASSWORD') as f:
    MONGOLAB_PASSWORD = f.readlines()[0]

connection = MongoClient("ds033153.mongolab.com", 33153)
db = connection["pocket-dla"]
db.authenticate("xuanji", MONGOLAB_PASSWORD)

mongo_texts = db.texts

# all_documents = list(mongo_texts.find({
#     'article': { '$exists': True }
# }, limit=5000))

# non_empty_documents = [document['article'] for document in all_documents if len(document['article']) > 1000]

lda = simple_lda.run_lda('non_empty_documents')

def terms_to_wordcounts(terms, multiplier=10000):
    return  " ".join([" ".join(int(multiplier*i[1]) * [i[0]]) for i in terms])

def make_image(terms, image_name):

    freqs = []
    for score, word in terms:
        freqs.append((word.split('/')[0], score))

    text = terms_to_wordcounts(freqs)

    wordcloud = WordCloud().generate(text)
    plt.imshow(wordcloud)
    plt.axis("off")

    wordcloud = WordCloud(max_font_size=40).generate(text)
    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig(image_name)

for i, topic in enumerate(lda.show_topics(num_topics=10, num_words=20)):
    print(topic)
    make_image(topic, 'topic' + str(i) + '.png')