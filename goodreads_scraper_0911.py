
import pandas as pd
book_df = pd.read_csv('books.csv')

from pymongo import MongoClient
client = MongoClient()
db = client.goodreads

import requests
from bs4 import BeautifulSoup

recs = {0: 'https://www.goodreads.com/book/show/18710190', 1: 'https://www.goodreads.com/book/show/890', 2: 'https://www.goodreads.com/book/show/12691', 3: 'https://www.goodreads.com/book/show/8127', 4: 'https://www.goodreads.com/book/show/43641', 5: 'https://www.goodreads.com/book/show/32542', 6: 'https://www.goodreads.com/book/show/2956', 7: 'https://www.goodreads.com/book/show/2187', 8: 'https://www.goodreads.com/book/show/7613', 9: 'https://www.goodreads.com/book/show/19063'}

for key, url in recs.items():
    response = requests.get(url)
    page = response.text   
    soup = BeautifulSoup(page,"lxml")
    recs.setdefault(key, [])
    recs[key].append(soup.find(class_="editionCover").findNext()['src'])

def book_summaries(book_urls_list):
    # scrape on goodreads.com using desire genre type or key word
    # and save the titles and autors in a csv file
    for url in book_urls_list:
   #     print(url)
        
        response = requests.get(url)
        page = response.text   
        soup = BeautifulSoup(page,"lxml")
    
        image = soup.find(class_="editionCover").findNext()['src']
        description = soup.find(id = 'description').text
     
        print(image, description)

def book_summary(url):
    response = requests.get(url)
    page = response.text   
    soup = BeautifulSoup(page,"lxml")    
    image = soup.find(class_="editionCover").findNext()['src']
    description = soup.find(id = 'description').text
    return image, description

def book_image(url):
    response = requests.get(url)
    page = response.text   
    soup = BeautifulSoup(page,"lxml")
    image = soup.find(class_="editionCover").findNext()['src']
    return image

def book_description(url):
    response = requests.get(url)
    page = response.text   
    soup = BeautifulSoup(page,"lxml")
    description = soup.find(id = 'description').text
    return description

rec_list = list(recs.values())
book_summaries(rec_list)


from collections import defaultdict


book_info = defaultdict(list)


def find_book_info(ID):
    for book in db.books.find({'book_id':ID}):
        print (book)

rec_titles = ['Allegiant', 'Of Mice and Men', "Marley & Me: Life and Love with the World's Worst Dog", 'Anne of Green Gables', 'Water for Elephants', 'A Time to Kill', 'The Adventures of Huckleberry Finn', 'Middlesex', 'Animal Farm: A Fairy Story', 'The Book Thief']

'''
def find_book_info_bytitle(rec):
    for book in db.books.find({'original_title':rec}):
        try:
            print ((book)['goodreads_book_id'])
        except:
            pass
        try:
            print ((book)['original_title'])
        except:
            pass
        try:
            print ((book)['authors'])
        except:
            pass
        try:
            print ((book)['average_rating'])
        except:
            pass  
        try:
            url = ('https://www.goodreads.com/book/show/'+str((book)['goodreads_book_id']))
            print (url)
        except:
            pass
    
        book_summary(url)
'''

def find_book_info_bytitle(rec):
    for book in db.books.find({'original_title':rec}):
        if (book)['goodreads_book_id'] in rec_dict:
            pass
        else:
            try:
                rec_dict[(book)['goodreads_book_id']].append((book)['original_title'])
            except:
                pass
            try:
                rec_dict[(book)['goodreads_book_id']].append((book)['authors'])
            except:
                pass
            try:
                rec_dict[(book)['goodreads_book_id']].append((book)['average_rating'])
            except:
                pass  
            try:
                url = ('https://www.goodreads.com/book/show/'+str((book)['goodreads_book_id']))
                rec_dict[(book)['goodreads_book_id']].append(url)
            except:
                pass
            try:
                image = book_image(url)
                rec_dict[(book)['goodreads_book_id']].append(image)
            except:
                pass
            try:
                description = book_description(url)
                rec_dict[(book)['goodreads_book_id']].append(description)
            except:
                pass


from collections import defaultdict
rec_dict = defaultdict(list)

for rec in rec_titles:
    find_book_info_bytitle(rec)



for key, value in rec_dict.items():
    print(value[0])



for goodreads_id in rec_dict.keys():
    image = (rec_dict[goodreads_id])[4]
    title = (rec_dict[goodreads_id])[0]
    author = (rec_dict[goodreads_id])[1]
    rating = (rec_dict[goodreads_id])[2]
    webpage = (rec_dict[goodreads_id])[3]
    image = (rec_dict[goodreads_id])[4]
    description = (rec_dict[goodreads_id])[5]
    print(image)
    print('Title:', title)
    print('Author:', author)
    print('Rating:', rating)
    print(description)

