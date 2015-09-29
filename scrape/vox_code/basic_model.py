from vox_articles_to_db import create_db 

from numpy.random import rand, RandomState
from numpy import array, matrix, linalg
from scipy.spatial.distance import pdist, squareform
from scipy import spatial
import pandas as pd
import numpy as np
import math

from sklearn.decomposition import TruncatedSVD, NMF

#Stemming and Lemmatizing packages
from nltk.stem import WordNetLemmatizer 
from nltk import word_tokenize   
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from nltk.stem.snowball import SnowballStemmer
import Stemmer
 

class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(TfidfVectorizer, self).build_analyzer()
        return lambda doc: english_stemmer.stemWords(analyzer(doc))



#Functions for convert db to matrix, initializiing nmf, and describing results

def reconst_mse(target, left, right):
    return (array(target - left.dot(right))**2).mean()

def describe_nmf_results(document_term_mat, W, H, n_top_words = 20):
    
    print("Reconstruction error: %f") %(reconst_mse(document_term_mat, W, H))
    topics = []
    for topic_num, topic in enumerate(H):
        curr_topic = [feature_words[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
        topics.append(curr_topic)
        print("Topic %d:" % topic_num)
        print(" ".join(curr_topic))   
    return topics

def convert_corpus_to_matrix(doc_bodies, n_features = 5000):
    vectorizer = StemmedTfidfVectorizer(max_features=n_features, stop_words='english', analyzer='word', ngram_range=(1,1))
    document_term_mat = vectorizer.fit_transform(doc_bodies)
    return vectorizer, document_term_mat

def calculate_word_dictionary(vectorizer):
    word_dictionary  = {}
    for index, word in enumerate(vectorizer.get_feature_names()):
        word_dictionary[word] = index 
    return word_dictionary

def generate_latent_topics(subset_matrix):
    print("\n\n---------\nsklearn decomposition")
    nmf = NMF(n_components=5)
    W_sklearn = nmf.fit_transform(subset_matrix)
    H_sklearn = nmf.components_
    return W_sklearn, H_sklearn

def calc_cosine_similarity(word_matrix, topic_vector):
    cosine_similarities = [1 - spatial.distance.cosine(article.todense(), topic_vector) for article in word_matrix]
    return cosine_similarities

#find indices of documents with consine similarity > threshold 
#                  *** threshold needs to be more intentional ***
def create_matrix_subset(raw_query, document_term_mat, threshold):
    vectorized_query = vectorizer.transform([raw_query])
    results = calc_cosine_similarity(document_term_mat, vectorized_query.todense())
    num_positive_values = len([result for result in results if result > threshold])
    positive_indices = np.argsort(np.abs(results))[-num_positive_values:-1]
    return document_term_mat[positive_indices]


def segment_and_categorize(query, current_matrix, threshold= .05):
    matrix_subset = create_matrix_subset(query,current_matrix, threshold)
    W_sklearn, H_sklearn = generate_latent_topics(matrix_subset)
    topics = describe_nmf_results(matrix_subset, W_sklearn, H_sklearn)
    return matrix_subset, topics



if __name__ == '__main__':

    print "begin"

    #Stemming and lemmatizing
    english_stemmer = Stemmer.Stemmer('en')
    snowball = SnowballStemmer('english')     

    #Initialize dataframe
    vox_raw_df = create_db()
    vox_df = vox_raw_df[vox_raw_df[1]!='']
    vox_df.shape
    doc_bodies = vox_df[1]


    vectorizer, document_term_mat = convert_corpus_to_matrix(doc_bodies)
    feature_words = vectorizer.get_feature_names()
    word_dictionary = calculate_word_dictionary(vectorizer)
    # W_sklearn, H_sklearn = generate_latent_topics(document_term_mat)
    # describe_nmf_results(document_term_mat, W_sklearn, H_sklearn)
    # print document_term_mat.shape
    # print W_sklearn.shape
    # print H_sklearn.shape

    main_query = 'Obama'
    subset_matrix = document_term_mat

    new_matrix, new_topics = segment_and_categorize(main_query, document_term_mat)
    print new_topics[3]

    new_query = main_query + ' '.join(new_topics[3])
    new_matrix, new_topics = segment_and_categorize(new_query, new_matrix, threshold = .1)

    new_query += ' '.join(new_topics[2])
    new_matrix, new_topics = segment_and_categorize(new_query, new_matrix, threshold = .4)

    new_query += ' '.join(new_topics[2])
    new_matrix, new_topics = segment_and_categorize(new_query, new_matrix, threshold = .4)
