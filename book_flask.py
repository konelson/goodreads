import goodreads_scraper_0911.py
# read in the model
#beer_model = pickle.load(open("ensemble_model.pickle","rb"))

# create a function to take in user-entered amounts and apply the model
#def rec_func(amounts_float, model=beer_model):
    

#book_df = pd.read_csv('books.csv')
ratings_df = pd.read_csv('ratings.csv')
#booktags_df = pd.read_csv('booktags.csv')
#tags_df = pd.read_csv('tags.csv')

import numpy as np
import pandas as pd

from sklearn.neighbors import NearestNeighbors

from pymongo import MongoClient
client = MongoClient()
db = client.goodreads

import pickle

with open('U.pickle','rb') as read_file:
    U = pickle.load(read_file)

with open('book_vecs_df_drop_na.pickle','rb') as read_file:
    book_vecs_df = pickle.load(read_file)

with open('book_vecs_drop_title.pickle','rb') as read_file:
    book_vecs = pickle.load(read_file)

def find_book_rating(ID):
    for book in db.books.find({'book_id':ID}):
        print (book['average_rating'])

def find_book_title(ID):
    for book in db.books.find({'book_id':ID}):
        print(book['original_title'])
        return (book['original_title'])

def find_book_title_noprint(ID):
    for book in db.books.find({'book_id':ID}):
        #print(book['original_title'])
        return (book['original_title'])

def get_recommendations_for_user(userID, U, VT, num_recom):
    recs = []
    for item in range(VT.T.shape[0]):
        recs.append([item+1,np.dot(U[userID-1],VT.T[item])])
    final_rec = [(i[0],i[1]) for i in sorted(recs,key=lambda x: x[1],reverse=True)]
    return final_rec[:num_recom]


# **Content-Based Filtering**

def get_title_index(book_title):
    try:
        filtered_vecs = book_vecs_df[book_vecs_df.Title == book_title]
        vec_index = filtered_vecs.index[0]
    except:
        print("Book currently checked out, please pick another")
    return vec_index

def get_reading_list(last_book_read):
    
    vec_index = get_title_index(last_book_read)
    
    nn = NearestNeighbors(n_neighbors=1000, metric='cosine', algorithm='brute')
    nn.fit(book_vecs)
    book_recs = nn.kneighbors(np.array([book_vecs.iloc[vec_index]]))
    
    reading_list = book_recs[1][0]
    
    reading_list_recs = []
    
    for book in reading_list:
        if book != '':
            reading_list_recs.append(book_vecs_df.iloc[book].Title)
        else:
            continue
        
    return reading_list_recs

# **Hybrid Filtering**

'''
Combine the two methods above.  Recommend books by user ratings 
and then filter down recommendation listing based on related content.
'''

def find_book_id(input_title):
    for book in db.books.find({'original_title':input_title}):
        print (book['book_id'])

def find_goodreads_id(input_title):
    for book in db.books.find({'original_title':input_title}):
        print (book['goodreads_book_id'])
        return (book['goodreads_book_id'])

def find_goodreads_id_np(input_title):
    for book in db.books.find({'original_title':input_title}):
        #print (book['goodreads_book_id'])
        return (book['goodreads_book_id'])

'''
#input_title = "Winnie-the-Pooh"
input_title = "Freakonomics: A Rogue Economist Explores the Hidden Side of Everything"
find_book_id(input_title)


books_by_user = ratings_df.groupby(by = 'user_id')

ratings_df[ratings_df.user_id == 1][ratings_df[ratings_df.user_id == 1].rating == 5]


USERID=1
num_recom = 100
for item in get_recommendations_for_user(USERID,U,VT,num_recom):
    find_book_title(item[0])
    find_book_rating(item[0])


#People who rated Freakonomics a 5
ratings_df[ratings_df.book_id == 92][ratings_df[ratings_df.book_id == 92].rating == 5]

#People who rated Winnie the Pooh a 5
ratings_df[ratings_df.book_id == 444][ratings_df[ratings_df.book_id == 444].rating == 5]

'''

original_rec_list = []
def create_rec_list(user_id):
    original_recs = []
    for item in get_recommendations_for_user(user_id, U, VT, 1000):
        original_recs.append(find_book_title_noprint(item[0]))
    return original_recs


#filter original rec list based on related content of last book read (rated)

'''

This function finds the user ID
Takes a book highly rated by the user (if not 5, 4, if not 4, 3, etc.)
not already read by the user
Takes the rec list from the user ID, based on ratings of other users

filters that rec list based on related content of the randomly selected highly rated book
returns top 5

for rec in original_rec_list:
    if rec in get_reading_list(book_title):
        print (rec, "YAY")
    else:
        print (rec, "NO!")
'''

#find books user has previously rated
def previously_read(user_num):
    userread_df = ratings_df[ratings_df.user_id == user_num].join(
    book_df, how = 'left', lsuffix = ' ', on = 'book_id')[['user_id','book_id','original_title']]
    previously_readbooks = list(userread_df.original_title)
    return previously_readbooks

#find books user has rated a 5
def find_favorites(user_num):
    userread_df = ratings_df[ratings_df.user_id == user_num][ratings_df[ratings_df.user_id == user_num].rating == 5].join(
    book_df, how = 'left', lsuffix = ' ', on = 'book_id')[['user_id','book_id','original_title']]
    fav_books = list(userread_df.original_title)
    return fav_books

def find_bookurl(book_title):
    goodreads_book_id = find_goodreads_id_np(book_title)
    return 'https://www.goodreads.com/book/show/'+str(goodreads_book_id)

def hybrid_filtering(user_id):
    
    last_book_read = np.random.choice(find_favorites(user_id)) #picks favorite book from user's previously read books
    print('Last Book Read:', last_book_read)
    
    already_read_list = previously_read(user_id)   
    original_list = create_rec_list(user_id) #takes in user id and returns original rec list
    reading_list = get_reading_list(last_book_read) #returns reading list
    
    book_recs = []
    for book in original_list:
        if book in reading_list == '':
            pass
        elif book not in already_read_list:
            book_recs.append(book)
 	'''   
 	from collections import defaultdict
    url_dict = defaultdict(list)
    
    #url_dict = {}
    for ix, rec in enumerate(book_recs[:10]):
        book_link = find_bookurl(rec)
        url_dict[ix] = book_link
    '''
    return book_recs[:10]
 
#hybrid_filtering(2575)

