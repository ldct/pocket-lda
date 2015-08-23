import logging
from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint
from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import lemmatize
import random
from itertools import chain
import cPickle

NUM_TOPICS = 10

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def is_real_word(word):
    if word in STOPWORDS: return False
    if '\n' in word: return False
    if word in ['--']: return False
    return True

def flatten(l):
    return list(chain.from_iterable(l))

def run_lda(documents):

    # texts = []
    # for i, document in enumerate(documents):
    #     if (i % 10 == 0): print i
    #     texts += [flatten([lemmatize(word) for word in document.lower().split() if is_real_word(word)])]

    with open('lemmatized_texts.pkl', 'rb') as f:
        texts = cPickle.load(f)

    dictionary = corpora.Dictionary(texts)
    dictionary.filter_extremes(no_below=20, no_above=0.1)
    corpus = [dictionary.doc2bow(text) for text in texts]
    lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=NUM_TOPICS, update_every=0, chunksize=10, passes=20)

    return lda

if __name__ == '__main__':
    run_lda(["Human machine interface for lab abc computer applications",
             "A survey of user opinion of computer system response time",
             "The EPS user interface management system",
             "System and human system engineering testing of EPS",
             "Relation of user perceived response time to error measurement",
             "The generation of random binary unordered trees",
             "The intersection graph of paths in trees",
             "Graph minors IV Widths of trees and well quasi ordering",
             "Graph minors A survey"])