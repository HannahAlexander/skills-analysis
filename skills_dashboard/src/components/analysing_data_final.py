from ast import Return
from glob import glob
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import glob
import re
import string
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
import nltk
import sys
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
import numpy as np
from heapq import nlargest
import plotly.express as px
import plotly.graph_objects as pgo
from nltk.stem import PorterStemmer
porter=PorterStemmer()
wnl = WordNetLemmatizer()
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import itertools
import os
from wordcloud import WordCloud

import sys
#sys.path.append('../../../sharepoint_scrapper')
#sys.path.append('C:/Users/hannah.alexander/OneDrive - Ascent Software Ltd/Documents/Internal projects/ascent-skills-analysis/sharepoint_scrapper')

#from extract_text import extract_cv

# create list of stopwords
stop_words = stopwords.words('english') + ["restricted", "external", "use", "used", "data", "overview", "profile", "professional_experience",
 "skills", "tools_and_utilities", "education", "languages", "data_scientist", "data_science", "university", "using", "&amp", "&", "end", "new", "work", "including", "19", "develop"]


dictionary = {"machine learning": "machine_learning",
    "ml": "machine_learning",
    "power bi": "power_bi",
    "shiny application": "shiny_application",
    "shiny dashboard": "shiny_dashboard",
    "shiny application": "shiny_application",
    "deep learning": "deep_learning",
    "time series": "time_series",
    "professional experience": "professional_experience",
    "natural language processing": "nlp",
    "tools and utilities": "tools_and_utilities",
    "data scientist": "data_scientist",
    "data science": "data_science",
    "statistical": "statistic",
    "covid19": "covid_19",
    "covid-19": "covid_19",
    "covid 19": "covid_19",
    "back end": "back_end",
    " sas ": "sas_programming",
    " sa ": "sas_programming",
    " r ": " r_language ",
    "time-series": "time_series",
    "developed": "develop",
    "development": "develop"}

sys.path.append('C:/Users/hannah.alexander/OneDrive - Ascent Software Ltd/Documents/Internal projects/ascent-skills-analysis/text_cleaning')
#sys.path.append('../../../text_cleaning')

from nlp import replace_all, remove_punctuation,remove_non_ascii, clean_text
import docx2txt
from bs4 import BeautifulSoup

# read in CVs from storage folder
def extract_cv(folder = "../../../storage/"):
    
    print(os.getcwd())
    text_files = {}
    for f in os.listdir(folder):
        try:
            file_name = folder + f
            text = docx2txt.process(file_name)
            # using beautifulsoup to tidy things up
            soup = str(BeautifulSoup(text, "html.parser"))
            text_files[f] = soup
        except:
            pass
    
    return(text_files)
cvs = extract_cv()

# get list of employee names
employee = list(cvs.keys())

def get_clean_descriptions(cvs = extract_cv()):
    descriptions = [val for key, val in cvs.items()]

    for i in range(len(descriptions)):

        # clean text
        words = clean_text(descriptions[i], raw_text = False)
        words = [word.lower() for word in words.split()]

        words = remove_non_ascii(words)
        words = remove_punctuation(words)

        # join, remove and re-split words 
        words = replace_all(" ".join(words), dictionary)

        # remove stopwords
        words = [w for w in words.split() if not w.lower() in stop_words]

        # lemmatize words (i.e. convert playing to play, using to use)
        words = [wnl.lemmatize(word) for word in words]

        words = " ".join(words)

        # add back to list
        descriptions[i] = words
    
    return descriptions

def get_employee_names(cvs = extract_cv()):
    employee = list(cvs.keys()) # list employee names
    # cleaning names
    employee_names = [e.split("-")[0] for e in employee]
    employee_names = [x.replace("Ascent Profile.docx", "") for x in employee_names]
    return employee_names

def create_clusters_of_words(descriptions = get_clean_descriptions()):
    # create vectoriser
    vectoriser = TfidfVectorizer(
        lowercase = True,
        max_features= 100, #only look at 100 words
        max_df = 0.6, #document frequency threshold - number of documents containing a term
        min_df=0.1, # min percentage of documents word has to occur in corpus
        ngram_range= (1,3), # look at up to trigrams
        stop_words = "english" # remove english stop words (just to make sure)
    )

    # transform descriptions into vectors
    vectors = vectoriser.fit_transform(descriptions)
    dense = vectors.todense()

    # create set of words that meet TDIF criteria
    denselist = dense.tolist()

    true_k = 3 #number of clusters we want
    model = KMeans(n_clusters= true_k, init = "k-means++", max_iter=100, n_init=1, random_state= 4) # define the model, setting random state to make clusters reproducible
    model.fit(vectors) #fit model to clusters

    order_centroids = model.cluster_centers_.argsort()[:, ::-1] # get centroids of each cluster
    terms = vectoriser.get_feature_names() # get words in each cluster

    cluster_list = {}

    for i in range(true_k): # for each cluster
            dynamic_variable_name = f"Cluster_{i}"
            term_list = []
            for ind in order_centroids[i, :20]: #look at top 20 words
                term_list.append(terms[ind])
            cluster_list[dynamic_variable_name] = term_list

    return cluster_list

def plot_clusters(descriptions = get_clean_descriptions(), employee_names = get_employee_names()):

    # create vectoriser
    vectoriser = TfidfVectorizer(
        lowercase = True,
        max_features= 100, #only look at 100 words
        max_df = 0.6, #document frequency threshold - number of documents containing a term
        min_df=0.1, # min percentage of documents word has to occur in corpus
        ngram_range= (1,3), # look at up to trigrams
        stop_words = "english" # remove english stop words (just to make sure)
    )

    # transform descriptions into vectors
    vectors = vectoriser.fit_transform(descriptions)
    dense = vectors.todense()

    # create set of words that meet TDIF criteria
    denselist = dense.tolist()

    true_k = 3 #number of clusters we want
    model = KMeans(n_clusters= true_k, init = "k-means++", max_iter=100, n_init=1, random_state= 4) # define the model, setting random state to make clusters reproducible
    model.fit(vectors) #fit model to clusters

    # plot employee clusters
    terms = vectoriser.get_feature_names() # get words in each cluster
    kmean_indices = model.fit_predict(vectors) #types of cluster

    fig, ax = plt.subplots(1, figsize=(15,10))
    pca = PCA(n_components=2)
    scatter_plot_points = pca.fit_transform(vectors.toarray()) # get plotting points
    df = {}

    x_axis = [o[0] for o in scatter_plot_points]
    y_axis = [o[1] for o in scatter_plot_points]

    df = pd.DataFrame(list(zip(y_axis, x_axis)), columns = ["y_vals", "x_vals"])

    df['cluster'] = list(kmean_indices)

    colors = ['b', 'g', 'r'] 
    df['c'] = df.cluster.map({0:colors[0], 1:colors[1], 2:colors[2]}) #, 4:colors[4]

    # plot data
    plt.scatter(x_axis, y_axis, c = [colors[d] for d in kmean_indices], alpha = 0.6, s=10)

    # draw enclosure
    for i in np.unique(kmean_indices):
        points = df[df.cluster == i][['x_vals', 'y_vals']].values
        # get convex hull
        hull = ConvexHull(points)
        # get x and y coordinates
        # repeat last point to close the polygon
        x_hull = np.append(points[hull.vertices,0],
                        points[hull.vertices,0][0])

        y_hull = np.append(points[hull.vertices,1],
                        points[hull.vertices,1][0])
        # plot shape
        plt.fill(x_hull, y_hull, alpha=0.3, c=colors[i])

    for i, txt in enumerate(employee_names):
        ax.annotate(txt, (x_axis[i], y_axis[i]))
    
    return fig


    
def wordcloud_clusters(descriptions = get_clean_descriptions()):
    
    vectoriser = TfidfVectorizer(
        lowercase = True,
        max_features= 100, #only look at 100 words
        max_df = 0.6, #document frequency threshold - number of documents containing a term
        min_df=0.1, # min percentage of documents word has to occur in corpus
        ngram_range= (1,3), # look at up to trigrams
        stop_words = "english" # remove english stop words (just to make sure)
    )

    # transform descriptions into vectors
    vectors = vectoriser.fit_transform(descriptions)
    dense = vectors.todense()

    # create set of words that meet TDIF criteria
    denselist = dense.tolist()

    terms = vectoriser.get_feature_names()
    true_k = 3 #number of clusters we want
    model = KMeans(n_clusters= true_k, init = "k-means++", max_iter=100, n_init=1, random_state= 4)
    model.fit(vectors) #fit model to clusters

    word_importance_df = pd.DataFrame(list(zip(terms, model.cluster_centers_[0], model.cluster_centers_[1], model.cluster_centers_[2])), columns = ["Words", "Cluster 0", "Cluster 1", "Cluster 2"])

    word_importance_dict = {}

    for cluster in ["Cluster 0", "Cluster 1", "Cluster 2"]:
        
        word_importance = []

        c = -1
        for w in word_importance_df["Words"]:
            c = c +1
            importance = word_importance_df[cluster][c]
            val = round(importance*100)
            word_importance.append([(w + " ")*val])

            cluster_word_importance = " ".join(list(itertools.chain.from_iterable(word_importance)))
            cluster_word = cluster_word_importance.split()
            word_importance_dict[cluster] = cluster_word
    
    index = 0
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize = (25, 50))

    cluster_word_0 = " ".join(word_importance_dict["Cluster 0"])
    cluster_word_1 = " ".join(word_importance_dict["Cluster 1"])
    cluster_word_2 = " ".join(word_importance_dict["Cluster 2"])

    ax1.plot()
    wordcloud = WordCloud(width = 800, height = 800,
                                background_color ='white',
                                min_font_size = 10, collocations=False, colormap= "Blues").generate(str(cluster_word_0))
    ax1.imshow(wordcloud)
    ax1.axis("off")
    ax1.set_title("Cluster 0", fontsize=30)

    ax2.plot()
    wordcloud = WordCloud(width = 800, height = 800,
                                background_color ='white',
                                min_font_size = 10, collocations=False, colormap= "Greens").generate(str(cluster_word_1))
    ax2.imshow(wordcloud)
    ax2.axis("off")
    ax2.set_title("Cluster 1", fontsize=30)

    ax3.plot()
    wordcloud = WordCloud(width = 800, height = 800,
                                background_color ='white',
                                min_font_size = 10, collocations=False, colormap= "Reds").generate(str(cluster_word_2))
    ax3.imshow(wordcloud)
    ax3.axis("off")
    ax3.set_title("Cluster 2", fontsize=30)

    return fig


def top_skills_employees(descriptions = get_clean_descriptions(), employee_names = get_employee_names()):
    count = 0
    for d in descriptions:
        e = employee_names[count]
        d_split = d.split()
        words_employee_count = {key: d_split.count(key) for key in d_split}
        l = nlargest(10, words_employee_count, key = words_employee_count.get)
        new_dict = dict( ((key, words_employee_count[key]) for key in l) )
        df = pd.DataFrame(new_dict.items(), columns=['Word', 'Count'])
        df["Employee"] = [e] * 10

        if count == 0:
            df_total = df

        if count > 0:
            df_total = df_total.append(df)

        count = count + 1

    return df_total

def plotly_clusters(descriptions = get_clean_descriptions(), employee_names = get_employee_names()):

    # create vectoriser
    vectoriser = TfidfVectorizer(
        lowercase = True,
        max_features= 100, #only look at 100 words
        max_df = 0.6, #document frequency threshold - number of documents containing a term
        min_df=0.1, # min percentage of documents word has to occur in corpus
        ngram_range= (1,3), # look at up to trigrams
        stop_words = "english" # remove english stop words (just to make sure)
    )

    # transform descriptions into vectors
    vectors = vectoriser.fit_transform(descriptions)
    dense = vectors.todense()

    # create set of words that meet TDIF criteria
    denselist = dense.tolist()

    true_k = 3 #number of clusters we want
    model = KMeans(n_clusters= true_k, init = "k-means++", max_iter=100, n_init=1, random_state= 4) # define the model, setting random state to make clusters reproducible
    model.fit(vectors) #fit model to clusters

    # plot employee clusters
    terms = vectoriser.get_feature_names() # get words in each cluster
    kmean_indices = model.fit_predict(vectors) #types of cluster

    fig, ax = plt.subplots(1, figsize=(15,10))
    pca = PCA(n_components=2)
    scatter_plot_points = pca.fit_transform(vectors.toarray()) # get plotting points
    df = {}

    x_axis = [o[0] for o in scatter_plot_points]
    y_axis = [o[1] for o in scatter_plot_points]

    df = pd.DataFrame(list(zip(y_axis, x_axis)), columns = ["y_vals", "x_vals"])

    df['cluster'] = list(kmean_indices)
    df["employee"] = employee_names

    colors = ['b', 'g', 'r'] 
    df['c'] = df.cluster.map({0:colors[0], 1:colors[1], 2:colors[2]})

    layout = pgo.Layout(title='Employee Skills Analysis (PCA)',
                        xaxis=pgo.XAxis(showgrid=False,
                                        zeroline=False,
                                        showticklabels=False),
                        yaxis=pgo.YAxis(showgrid=False,
                                        zeroline=False,
                                        showticklabels=False),
                        hovermode='closest'
    )

    colors = ['blue', 'green', 'red'] 
    df['c'] = df.cluster.map({0:colors[0], 1:colors[1], 2:colors[2]})

    trace0 = pgo.Scatter(x=df["x_vals"],
                        y=df["y_vals"],
                        text=df["employee"],
                        mode="markers+text",
                        marker=pgo.scatter.Marker(color=df["c"]),
                        showlegend=False
    )

    data = pgo.Data([trace0])
    fig = pgo.Figure(data=data, layout=layout)

    # draw enclosure

    for i in np.unique(df["c"]):
        points = df[df["c"] == i][['x_vals', 'y_vals']].values
        # get convex hull
        hull = ConvexHull(points)
        # get x and y coordinates
        # repeat last point to close the polygon
        x_hull = np.append(points[hull.vertices,0],
                        points[hull.vertices,0][0])

        y_hull = np.append(points[hull.vertices,1],
                        points[hull.vertices,1][0])

        fig.add_trace(pgo.Scatter(x=x_hull, y=y_hull,
            fill="toself",
            mode='lines',
            line_color= i,
            showlegend=False
            ))

    return(fig)