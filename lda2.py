import re
import numpy as np
import pandas as pd
from pprint import pprint

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# spacy for lemmatization
import spacy

# Plotting tools
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt
# matplotlib inline

# Enable logging for gensim - optional
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

import warnings
import nltk
warnings.filterwarnings("ignore",category=DeprecationWarning)
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
stop_words = stopwords.words('english')
count = 0
def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

# Define functions for stopwords, bigrams, trigrams and lemmatization
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out
pd.set_option('display.expand_frame_repr', True)
pd.set_option('display.max_rows', 1700000)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', -1)
data = pd.read_csv("DataSourceHindu.csv", header=None, skiprows=18300,nrows=100,encoding='latin-1')
print(data)
data_text = data
print(type(data_text))
lda_list = []
for d in data_text:
    data_sentences = []
    # break whole text into sentences for each entry in data_text and save to data_sentences
    #each record in data_sentences corressponds to individual article and has segregated sentences
    b = pd.Series(d)
    for text in b:
        data_sentences.append(sent_tokenize(str(text)))
    # convert the sentences of each articles into words. each entry in data_words has words as a list in an article
    data_words = list(sent_to_words(data_sentences))
    # print(data_words)

    # Build the bigram and trigram models
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100)  

    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)

    # Remove Stop Words
    data_words_nostops = remove_stopwords(data_words)

    # Form Bigrams
    data_words_bigrams = make_bigrams(data_words_nostops)

    # Initialize spacy 'en' model, keeping only tagger component (for efficiency)
    # python3 -m spacy download en
    nlp = spacy.load('en', disable=['parser', 'ner'])

    # Do lemmatization keeping only noun, adj, vb, adv
    data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

    # Create Dictionary
    id2word = corpora.Dictionary(data_lemmatized)
    # Create Corpus
    texts = data_lemmatized
    print(texts)
    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]

    # View

    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,id2word=id2word,num_topics=1,random_state=100, update_every=1,chunksize=100,passes=50,alpha='auto',per_word_topics=True)

    # pprint(lda_model.print_topics())
    topics = lda_model.show_topics(num_words=5,formatted=False)
    count += 1
    print(count)
    string = ''
    for i in range(5):
        string += topics[0][1][i][0] + ', '
    lda_list.append(string)

pd.DataFrame({
    "Title": data[1],
    "Date": data[2],
    "Link": data[3],
    "Init Crime": data[4],
    "lat": data[5],
    "long":data[6],
    "LDA Topics": lda_list
}).to_csv('DataHinduLDA1.csv', columns=['Title', 'Date', 'Link', 'Init Crime', 'lat', 'long','LDA Topics'], encoding='utf-8')
