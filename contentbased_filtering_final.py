from pymongo import MongoClient
client = MongoClient()
db = client.goodreads

import nltk
from nltk.corpus import stopwords
import gensim
import numpy as np
import pandas as pd
import pprint
import sys
import copy

import pickle
with open('removed_tags.pickle','rb') as read_file:
    removed_tags = pickle.load(read_file)

removed_tag_list = []

for tag in removed_tags:
    for word in tag:
        removed_tag_list.append(word)

stop_words = stopwords.words('english')
removed_words = removed_tag_list + stop_words

with open('goodreads_id_list.pickle','rb') as read_file:
    goodreads_id_list = pickle.load(read_file)

goodreads_id_list

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

def create_booktag_list(ID):
    book_word_list = []
    for tag in find_booktags_name(ID):
        for word in tag:
            if word not in removed_words:
                book_word_list.append(word)
    return book_word_list

'''
def create_word_vecs(goodreads_ids):
 #   for bookid in goodreads_ids:
    book_word_list = create_booktag_list(goodreads_id)
    #    vector_list.append(book_word_list)
    return book_word_list
'''

#Use Google Model
google_vec_file = 'GoogleNews-vectors-negative300.bin'
google_model = gensim.models.KeyedVectors.load_word2vec_format(google_vec_file, binary=True)

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
    for vec in vector_list:
        book_vec = create_document_vector(vec, google_model)
  #      book_vecs.append(book_vec)
    return book_vec


#Run Model
book_vecs = []
for ix in goodreads_id_list[:]:
    book_word_list = create_booktag_list(ix)
    book_vec = create_vectors(book_word_list)
    book_vecs.append(book_vec)

#Check
#len(book_vecs)

vector_df = pd.DataFrame(book_vecs)
#vector_df

sys.getsizeof(book_vecs)
with open ('book_vecs.pickle', 'wb') as to_write:
    pickle.dump(book_vecs, to_write)

book_vec_copy = copy.copy(book_vecs)


def find_goodreads_title(ID):
    for book in db.books.find({'goodreads_book_id':ID}):
        return(book['original_title'])

book_titles = []
for goodreads_id in goodreads_id_list:
    book_title = find_goodreads_title(goodreads_id)
    book_titles.append(book_title)

#Remove books that have no associated word tags
for ix, vec in enumerate(book_vec_copy[0:10000]):
    if vec is None:
        print (ix)

#Add NaNs inplace of NoneType
for ix, vec in enumerate(book_vec_copy[0:10000]):
    if vec is None:
        book_vec_copy[ix] = (np.array(['NaN']*300))

#Check
for ix, vec in enumerate(book_vec_copy[0:10000]):
    if vec is None:
        print (ix)

vec_df = pd.DataFrame(book_vec_copy)
#vec_df

book_vec_df = pd.concat([pd.DataFrame(book_titles).rename(columns = {0:'Title'}), vec_df], axis = 1)
#book_vec_df

with open ('book_vec_df.pickle', 'wb') as to_write:
    pickle.dump(book_vec_df, to_write)

