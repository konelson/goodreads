from pymongo import MongoClient
client = MongoClient()
db = client.goodreads

import pandas as pd
book_df = pd.read_csv('books.csv')

import os
import random
import time
import requests
from bs4 import BeautifulSoup

from collections import defaultdict
recs_dict = defaultdict(list)

#Insert example
#recs = {0: 'https://www.goodreads.com/book/show/18710190', 1: 'https://www.goodreads.com/book/show/890', 2: 'https://www.goodreads.com/book/show/12691', 3: 'https://www.goodreads.com/book/show/8127', 4: 'https://www.goodreads.com/book/show/43641', 5: 'https://www.goodreads.com/book/show/32542', 6: 'https://www.goodreads.com/book/show/2956', 7: 'https://www.goodreads.com/book/show/2187', 8: 'https://www.goodreads.com/book/show/7613', 9: 'https://www.goodreads.com/book/show/19063'}
#url = recs[1]

for ix, url in recs:
    recs_dict[ix].append(url)

for url in recs.values():
    print (url)

response = requests.get(url)
page = response.text   
soup = BeautifulSoup(page,"lxml")
print(soup.find(class_="editionCover").findNext()['src'])

for key, url in recs.items():
    response = requests.get(url)
    page = response.text   
    soup = BeautifulSoup(page,"lxml")
    recs.setdefault(key, [])
    recs[key].append(soup.find(class_="editionCover").findNext()['src'])

soup.find(class_="editionCover")
soup.find(class_="editionCover").findNext()['src']


def book_summaries(book_urls_list):
    for url in book_urls_list:
        print(url)        
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
    if soup.find(class_="editionCover") != None:
        image = soup.find(class_="editionCover").findNext()['src']
    else:
        image = ''
    return image

#book_image('https://www.goodreads.com/book/show/3')

def book_description(url):

    response = requests.get(url)
    page = response.text   
    soup = BeautifulSoup(page,"lxml")
    if soup.find(id = 'description')!= None:
        description = soup.find(id = 'description').text
    else:
        description = ''
    return description

#url
#book_image(url)

#rec_list = list(recs.values())
#book_summaries(rec_list)

# Beginning of url --> 'https://www.goodreads.com/book/show/'

filtered_books.head()
''.join(['https://www.goodreads.com/book/show/',str(filtered_books.goodreads_book_id[0])])

book_info = defaultdict(list)
for book in db.books.find_one():
    print (book)

def find_book_info(ID):
    for book in db.books.find({'book_id':ID}):
        print (book)

rec_titles = ['Allegiant', 'Of Mice and Men', "Marley & Me: Life and Love with the World's Worst Dog", 
                'Anne of Green Gables', 'Water for Elephants', 'A Time to Kill', 
                'The Adventures of Huckleberry Finn', 'Middlesex', 'Animal Farm: A Fairy Story', 
                'The Book Thief']

def show_book_info_bytitle(rec):
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

#find_book_info_bytitle("Allegiant")

#rec_dict.values()
#rec_dict.keys()

rec_dict = defaultdict(list)
for rec in rec_titles:
    find_book_info_bytitle(rec)

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

import pickle
with open ('rec_dict.pickle', 'wb') as to_write:
    pickle.dump(rec_dict, to_write)

rec_dict = defaultdict(list)

for ix, title in enumerate(rec_titles):
    print(ix, title)

def create_flask_dict(rec_titles):
    rec_dict = defaultdict(list)
    for ix, title in enumerate(rec_titles):
        for rec in db.books.find({'original_title':title}):
            goodreads_id = (rec['goodreads_book_id'])
            rec_dict[ix].append(goodreads_id)
            
            title = (rec['original_title'])
            rec_dict[ix].append(title)
            
            author = (rec['authors'])
            rec_dict[ix].append(author)
            
            rating = (rec['average_rating'])
            rec_dict[ix].append(rating)
            
            url = ('https://www.goodreads.com/book/show/'+str((rec)['goodreads_book_id']))
            
            image = book_image(url)
            rec_dict[ix].append(image)
            
            description = book_description(url)
            rec_dict[ix].append(description)
    
    return rec_dict

rec_dict = defaultdict(list)
create_flask_dict(rec_titles)

url = 'https://www.goodreads.com/book/show/18710190'

response = requests.get(url)
page = response.text   
soup = BeautifulSoup(page,"lxml")
image = soup.find(class_="editionCover").findNext()['src']
soup.find(id = 'description')
print(soup.find(id="description").text)


for title in rec_titles:
    for rec in db.books.find({'original_title':title}):
        print(''.join(['https://www.goodreads.com/book/show/',str((rec)['goodreads_book_id'])]))

#dict(filtered_books.T)
book_info = dict(filtered_books.T)

url_list = []
for book in list(filtered_books.goodreads_book_id):
    url = (''.join(['https://www.goodreads.com/book/show/',str(book)]))
    url_list.append(url)

'''
import requests
import csv
from bs4 import BeautifulSoup
import urllib
import os
import pandas
import random
import time

def goodreads_book_summaries(url_list):
    index = 0
    indx_list = []
    desc_dict = {}
    failed_page = {}
    for book_url in url_list:
        secs = random.uniform(.001, .1)
        time.sleep(secs)
        response = requests.get(book_url)
        page = response.text
        soup = BeautifulSoup(page,"lxml")
        try:    
            desc_dict[index] = {'url':url, 'description': soup.find(id="description").text}
        except: 
            #if fails for some reason, then print out the url and the page
            pass#indx_list.append(index)
            #failed_page[index] = soup, book_url
        index = index + 1 
    return desc_dict 
'''
urls = ['https://www.goodreads.com/book/show/2767052',
 'https://www.goodreads.com/book/show/3',
 'https://www.goodreads.com/book/show/41865']

desc_dict = goodreads_book_summaries(urls)
#desc_dict = goodreads_book_summaries(url_list)

#desc_dict
#desc_dict[0]['description']

more_book_info = {}
def add_img_desc(url_list):
    import time  
    for ix, url in enumerate(url_list):       
        more_book_info[ix] = {'url': url}
        secs = random.uniform(.001, .5)
        time.sleep(secs)
        image = book_image(url)
        description = book_description(url)  
        more_book_info[ix]['image'] = image
        more_book_info[ix]['description'] = description
    return more_book_info

#more_book_info[0]['url']
#more_book_info

url = 'https://www.goodreads.com/book/show/2767052'

add_img_desc(url_list[0:100])
book_image(url)

import pickle
with open ('rec_dict.pickle', 'wb') as to_write:
    pickle.dump(rec_dict, to_write)

content_booklist = ['Blink: The Power of Thinking Without Thinking',
              'Dreams from My Father',
              'ねじまき鳥クロニクル [Nejimakidori kuronikuru]',
              "Pandora's Star",
              'E.E. Cummings: Complete Poems 1904-1962',
              'The Road to Character',
              'A Constellation of Vital Phenomena',
              'The Magic (The Secret #3)',
              'Fates and Furies',
              'number9dream',
              'The Martian Chronicles']

content_bookdict = create_flask_dict(content_booklist)
with open ('content_bookdict.pickle', 'wb') as to_write:
    pickle.dump(content_bookdict, to_write)

