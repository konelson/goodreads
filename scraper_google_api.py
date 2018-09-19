'''
This Scraper did not pick up all images / descriptions for all books.  
Find selection or use goodreads scraper.
'''
import pandas as pd
import json
import urllib

book_df = pd.read_csv('books.csv')
book_df.isbn13.fillna(0,inplace = True)
book_df['isbn13_f'] = book_df.isbn13.apply(lambda x: str(int(x)))

isbn_dict = {}

for ix, isbn in (enumerate(list(book_df.isbn13_f))):
    isbn_dict[ix] = {'isbn' : isbn}

for key, value in isbn_dict.items():
    link = ((''.join(['https://www.googleapis.com/books/v1/volumes?q=isbn:',value['isbn']])))
    isbn_dict[key]['url'] = link 

url = urllib.request.urlopen('http://books.google.com/books/content?id=8dEEuAEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api')

''' #Test on one isbn number#

current_isbn = str(9780439023481)
test_url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:{}'.format(current_isbn)
import requests
from ast import literal_eval
a_test_thing = requests.get(test_url)
j = json.loads(a_test_thing.content)
for item in j['items']:
    #print (item['volumeInfo'])
    print (item['volumeInfo']['description'])
    print(item['volumeInfo']['imageLinks']['thumbnail'])
'''

isbn_dict.items()
for key, val in isbn_dict.items():
    current_isbn = val['isbn']
    test_url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:{}'.format(current_isbn)
    import requests
    from ast import literal_eval
    a_test_thing = requests.get(test_url)
    j = json.loads(a_test_thing.content)
    try:
        for item in j['items']:
            desc = (item['volumeInfo']['description'])
            img = (item['volumeInfo']['imageLinks']['thumbnail'])
    except:
        desc = ''
        img = ''      
    isbn_dict[key]['description'] = desc
    isbn_dict[key]['image'] = img

import pickle
with open ('isbn_dict.pickle', 'wb') as to_write:
    pickle.dump(isbn_dict, to_write)