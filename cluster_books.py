import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

from yellowbrick.cluster import SilhouetteVisualizer
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.manifold import TSNE
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans, MiniBatchKMeans

import pickle
with open('book_vec_df.pickle','rb') as read_file:
    book_vecs_df = pickle.load(read_file)

def cluster_books(book_vecs, n_clusters, random_st):
    km = KMeans(n_clusters, random_state=random_st)
    cluster_labels=km.fit_predict(book_vecs)
    return cluster_labels

nan_list = [488,838,1371,1834,3122,3382,4044,4118,4190,4398,4420,4474,4515,4590,4664,4759,4825,4959,
            4979,5243,5372,5705,6069,6118,6912,7023,7241,7449,7605,7822,7936,7962,8402,8881,9007,9038,
            9077,9220,9242,9326,9569,9609,9729,9769,9828,9857,9966]

book_vecs_df = book_vecs_df.drop(nan_list)
with open ('book_vecs_df_drop_na.pickle', 'wb') as to_write:
    pickle.dump(book_vecs_df, to_write)

book_vecs = book_vecs_df.drop(columns = 'Title')
with open ('book_vecs_drop_title.pickle', 'wb') as to_write:
    pickle.dump(book_vecs, to_write)

#find optimal value for k
SSE = []
for k in range(2,100):
    km = KMeans(n_clusters = k, random_state = 42)
    km.fit(book_vecs)
    labels = km.labels_
    SSE.append(km.inertia_)
plt.figure(dpi = 150)
plt.xlabel("Number of clusters")
plt.ylabel("SSE")
plt.plot(range(2,100),SSE);
#plt.ylim((0,600))
plt.savefig("cluster_plot")

book_clusts = cluster_books(book_vecs, 42, 42)

visualiser = SilhouetteVisualizer(KMeans(n_clusters=42), random_state = 42)
visualiser.fit(book_vecs)
visualiser.poof()

tsne_model = TSNE(n_components=2, random_state = 42, verbose = 0)
low_data = tsne_model.fit_transform(book_vecs)

from matplotlib import colors as mcolors
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
plot_colors = (list(colors.keys())[:42])

#colors = (['crimson','b','mediumseagreen','cyan','m','y', 'k', 'orange', 'springgreen', 'deepskyblue', 'yellow', 'teal', 'navy', 'plum', 'darkslategray', 'lightcoral', 'papayawhip'])

plt.figure(dpi = 150)
for i, c, label in zip (range(42), plot_colors, list(range(42))):
    plt.scatter(low_data[book_clusts == i, 0], low_data[book_clusts == i, 1], c=c, label = label, s = 15, alpha = 1)
#plt.legend(fontsize = 10, loc = 'upper left', frameon = True, facecolor = '#FFFFFF', edgecolor = '#333333');
plt.title("Clusters with TSNE", fontsize = 12);
plt.xlim(-125,125);
plt.ylim(-125,125);
plt.ylabel("Y Axis");
plt.xlabel("X Axis");
plt.yticks(fontsize =10);
plt.xticks(fontsize = 10);
plt.show()
plt.savefig("tsne_plot")

nn = NearestNeighbors(n_neighbors=10, metric='cosine', algorithm='brute')
nn.fit(book_vecs)

def get_title_index(book_title):
    try:
        filtered_vecs = book_vecs_df[book_vecs_df.Title == book_title]
        vec_index = filtered_vecs.index[0]
    except:
        print("Book currently checked out, please pick another")
    return vec_index

def get_reading_list(last_book_read):
    vec_index = get_title_index(last_book_read)
    nn = NearestNeighbors(n_neighbors=10, metric='cosine', algorithm='brute')
    nn.fit(book_vecs)
    book_recs = nn.kneighbors(np.array([book_vecs.iloc[vec_index]]))
    reading_list = book_recs[1][0]
    from collections import defaultdict
    rec_dict = defaultdict(list) #initializes default dictionary for book recommendations
    for ix, book_ix in enumerate(reading_list):
        #print (ix, book_ix)
        rec_dict[last_book_read].append(book_vecs_df.iloc[book_ix].Title)
    return rec_dict    

#get_reading_list("Eat, pray, love: one woman's search for everything across Italy, India and Indonesia")
#get_reading_list("The Tipping Point: How Little Things Can Make a Big Difference")
#get_reading_list("Winnie-the-Pooh")
#get_reading_list("Blink: The Power of Thinking Without Thinking")

def get_bigger_reading_list(last_book_read):   
    vec_index = get_title_index(last_book_read)
    nn = NearestNeighbors(n_neighbors=15, metric='cosine', algorithm='brute')
    nn.fit(book_vecs)
    book_recs = nn.kneighbors(np.array([book_vecs.iloc[vec_index]]))
    reading_list = book_recs[1][0]
    from collections import defaultdict
    rec_dict = defaultdict(list) #initializes default dictionary for book recommendations
    for ix, book_ix in enumerate(reading_list):
        #print (ix, book_ix)
        rec_dict[last_book_read].append(book_vecs_df.iloc[book_ix].Title)
    return rec_dict    

#get_bigger_reading_list("Blink: The Power of Thinking Without Thinking")
#get_bigger_reading_list("The Lord of the Rings")
#get_bigger_reading_list('A Game of Thrones')
#get_bigger_reading_list('Pride and Prejudice')

