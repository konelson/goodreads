
from pymongo import MongoClient
client = MongoClient()
db = client.goodreads

import nltk
from nltk.corpus import stopwords
import gensim
import pprint


import pickle
with open('removed_tags.pickle','rb') as read_file:
    removed_tags = pickle.load(read_file)

removed_tag_list = []
for tag in removed_tags:
    for word in tag:
        removed_tag_list.append(word)
stop_words = stopwords.words('english')
removed_words = removed_tag_list + stop_words

def get_goodreads_ids():
    '''
    Returns list of 10,000 goodreads books by ID
    '''
    goodreads_id_list = []
    for book in db.books.find():
        goodreads_id_list.append(book['goodreads_book_id'])
    return goodreads_id_list

get_goodreads_ids()
goodreads_id_list = get_goodreads_ids()
print(goodreads_id_list)


def find_booktags (ID):
    '''
    Finds booktag ID numbers associated with each goodread
    '''
    booktag_list = []
    for book in db.booktags.find({'goodreads_book_id': ID}):
        booktag_list.append(book['tag_id'])
    return booktag_list


def find_booktags_name(ID):
    '''
    Finds descriptive 'tags' for all goodreads books and looks up associated tag name
    '''
    booktag_list = []          
    for book in db.booktags.find({'goodreads_book_id':ID}):
        tagid = (book['tag_id'])
        for tag in db.tags.find({'tag_id':tagid}):
            try:
                booktag_list.append(tag['tag_name'].split('-'))
            except:
                booktag_list.append(str(tag['tag_name']).split('-'))
    #print(booktag_list)
    return(booktag_list)

find_booktags_name(2767052)

def create_booktag_list(ID):
    book_word_list = []
    for tag in find_booktags_name(ID):
        for word in tag:
            if word not in removed_words:
                book_word_list.append(word)
    return book_word_list

def create_word_vecs(goodreads_ids):
    vector_list = []
    for bookid in goodreads_ids:
        book_word_list = create_booktag_list(bookid)
        vector_list.append(book_word_list)
    return vector_list

#Use Google Model so don't have to train
google_vec_file = 'GoogleNews-vectors-negative300.bin'
google_model = gensim.models.KeyedVectors.load_word2vec_format(google_vec_file, binary=True)
#model = gensim.models.Word2Vec([vector_list], size = 100, window = 5, min_count = 1, workers = 4, sg = 1)

def create_document_vector(words, google_model):
    good_words = []
    for word in words:
        # Words not in the original model will fail
        try:
            if google_model.wv[word] is not None:
                good_words.append(word)
        except:
            continue
    # If no words are in the original model
    if len(good_words) == 0:
        return None
    # Return the mean of the vectors for all the good words
    return google_model.wv[good_words].mean(axis=0)

def create_vectors(vector_list):
    book_vecs = []
    for vec in vector_list:
        book_vec = create_document_vector(vec, google_model)
        book_vecs.append(book_vec)
    return book_vecs

create_vectors(vector_list)

import pandas as pd
vector_df = pd.DataFrame(book_vecs)
vector_df

