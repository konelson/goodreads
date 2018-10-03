# goodreads

**Hybrid book recommendation system that uses 10,000 books from goodreads with 6 million ratings, which is deployed in a flask app**

1.  get_goodreads.py
    - obtains csv files from github (https://github.com/zygmuntz/goodbooks-10k)
2.  collaborative_filtering_final.py
    - applies singular value decomposition to user rating data to find similarly rated books from similar users using a sparse matrix
3.  contentbased_filtering_final.py
    - applies gensim's Word2Vec to the booktag data to create book vectors 
4.  cluster_books.py
    - uses book vectors to find 10 nearest neighbors using cosine similarity and generates a reading list
5.  hybrid_filtering.py
    - filters collaborative recommendations through content based recommender
6.  goodreads_scraper.py
    - webscrapes book cover image and book description from goodreads website using BeautifulSoup
7.  goodreadsmain.oy
    - flask app that generates a reading list given either a User ID or book title
