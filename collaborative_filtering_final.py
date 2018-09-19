import numpy as np
import pandas as pd

from scipy.sparse.linalg import svds
from scipy.sparse import lil_matrix
from scipy.sparse import csr_matrix

ratings_df = pd.read_csv('ratings.csv')
book_df = pd.read_csv('books.csv')


from pymongo import MongoClient
client = MongoClient()
db = client.goodreads
books = db.books

#books.find_one()

ratings = db.ratings
booktags = db.booktags
tags = db.tags

import pprint

for book in db.books.aggregate([{'$sample':{'size':5}},
                    {'$project':{'_id':0,'Book ID':'$book_id','Title':'$original_title'}}
                   ]):
        pprint.pprint(book)

for book in db.books.aggregate([{'$sample':{'size':5}},
                    {'$lookup': {
                        'from': 'ratings',
                        'localField': 'book_id',
                        'foreignField': 'book_id',
                        'as': 'joined'},
                    },
                    {'$project':{'_id':0,'Book ID':'$book_id','Title':'$original_title'}}
                   ]):
        pprint.pprint(book)

for book in db.books.find({"book_id":2}):
    print('Book ID: ', book['book_id'])
    print('Title: ', book['original_title'])


def find_book_info(ID):
    for book in db.books.find({'book_id':ID}):
        print (book)

def find_book_rating(ID):
    for book in db.books.find({'book_id':ID}):
        print (book['average_rating'])

def find_book_title(ID):
    for book in db.books.find({'book_id':ID}):
#        print('Book ID: ', book['book_id'])
        print(book['original_title'])


mat = lil_matrix((53000,10000)) #linked list matrix

mat.shape

#Test small sample of 5
rating_cursor = ratings.aggregate([{'$sample':{'size':5}}]) 

for rating in rating_cursor:
        u = float(rating['user_id'])
        print(u)
        b = float(rating['book_id'])
        print(b)
        r = float(rating['rating'])
        print(r)
        mat[u, b] = r

mat.data
mat.shape
mat.sum()
print(mat)

for u, b, r in zip (u, b, r):
    mat[u,b] = r

int(rating['user_id'])

#Apply to all data
large_mat = lil_matrix((53425,10001)) #linked list matrix
large_rating_cursor = ratings.find()#aggregate([{'$sample':{'size':100000}}]) 

for rating in large_rating_cursor:
        u = float(rating['user_id'])
        b = float(rating['book_id'])
        r = float(rating['rating'])
        large_mat[u, b] = r

large_mat.data.nbytes
large_mat.tocsr().data.nbytes
csr_mat = large_mat.tocsr()
csr_mat.shape

U.shape
s.shape
VT.shape

csr_mat.data
csr_mat.shape

U, s, VT = svds(csr_mat,k=175)

U.data.nbytes
VT.data.nbytes


import pickle
with open ('U.pickle', 'wb') as to_write:
    pickle.dump(U, to_write)

with open ('VT.pickle', 'wb') as to_write:
    pickle.dump(VT, to_write)

def get_recommendations_for_user(userID, U, VT, num_recom):
    recs = []
    for item in range(VT.T.shape[0]):
        recs.append([item+1,np.dot(U[userID-1],VT.T[item])])
    final_rec = [(i[0],i[1]) for i in sorted(recs,key=lambda x: x[1],reverse=True)]
    return final_rec[:num_recom]

def item_similarity(item1,item2):
    return np.dot(VT.T[item1],VT.T[item2])


'''
USERID=20000
num_recom = 11
rec_list = []
for item in get_recommendations_for_user(USERID,U,VT,num_recom):
#    print(ix, find_book_title(item[0]), end="")
#    print(item[0])
    find_book_title(item[0])
#    find_book_rating(item[0])

USERID=1
num_recom = 10
rec_list = []
for item in get_recommendations_for_user(USERID,U,VT,num_recom):
    find_book_title(item[0])

USERID=700
num_recom = 10
rec_list = []

print("User ID:", USERID)
print('\nLast Book Read:\n',np.random.choice(find_favorites(USERID)))
print('\nRecommendations:\n')
for item in get_recommendations_for_user(USERID,U,VT,num_recom):
    find_book_title(item[0])
'''

#find books user has rated a 5
def find_favorites(user_num):
    userread_df = ratings_df[ratings_df.user_id == user_num][ratings_df[ratings_df.user_id == user_num].rating == 5].join(
    book_df, how = 'left', lsuffix = ' ', on = 'book_id')[['user_id','book_id','original_title']]
    fav_books = list(userread_df.original_title)
    return fav_books


