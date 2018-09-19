'''
This file reads in goodreads data and converts DataFrames to CSV files to upload to MongoDB
'''

import pandas as pd

bookurl = 'https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/books.csv'
ratingsurl = 'https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/ratings.csv'
booktagsurl = 'https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/book_tags.csv'
tagsurl = 'https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/tags.csv'

book_df = pd.read_csv(bookurl)
ratings_df = pd.read_csv(ratingsurl)
booktags_df = pd.read_csv(booktagsurl)
tags_df = pd.read_csv(tagsurl)

tags_df['tag_words'] = tags_df.tag_name.apply(lambda x: x.split('-'))


book_df.to_csv('books.csv', index = False, sep = ',')
ratings_df.to_csv('ratings.csv', index = False, sep = ',')
booktags_df.to_csv('booktags.csv', index = False, sep = ',')
tags_df.to_csv('tags.csv', index = False, sep = ',')

