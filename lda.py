from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
import pandas as pd
import nltk
import gensim
from gensim import corpora
stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

#1=title 2=date 3=link 6=initCrime 7=text 8=lat 9=long
print('Reading')
#data = pd.read_csv("DataHinduCleanedLevel1.csv", header=None,skiprows=1, nrows=1)
data_text = input("Enter News Data:")
print(data_text)
doc_clean = [clean(doc).split() for doc in data_text]
print(doc_clean)
dictionary = corpora.Dictionary(doc_clean)
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
# print(doc_term_matrix)
Lda = gensim.models.ldamodel.LdaModel
ldamodel = Lda(doc_term_matrix, num_topics=3, id2word = dictionary, passes=50)
print(ldamodel.print_topics(num_topics=2, num_words=3))