# library for text preprocessing
import nltk
import pandas as pd
import re, unicodedata
from nltk.corpus import stopwords
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

from nltk.stem import LancasterStemmer
from nltk.stem.wordnet import WordNetLemmatizer


def clean_text(raw, raw_text = True):
    """Case specific to be used with pandas apply method"""
    try:
        if raw_text == True:
            # remove carriage returns and new lines
            raw = ''.join(raw.splitlines())

        raw = raw.replace("�","")
        
        # brackets appear in all instances
        raw = raw.replace("[", "")
        raw = raw.replace("]", "")
        raw = raw.replace(")", "")
        raw = raw.replace("(", "")
        raw = raw.replace("·", "")
        
        # removing html tags
        clean_html = re.compile("<.*?>")
        clean_text = re.sub(clean_html, " ", raw)
        
        # removing duplicate whitespace in between words
        clean_text = re.sub(" +", " ", clean_text) 
        
        # stripping first and last white space 
        clean_text = clean_text.strip()
        
        # commas had multiple spaces before and after in each instance
        clean_text = re.sub(" , ", ", ", clean_text) 
        
        # eliminating the extra comma after a period
        clean_text = clean_text.replace(".,", ".")
    except:
        clean_text = np.nan
        
    return clean_text

def replace_all(text, dic):
    for i, j in dic.items():
        text = re.sub(r"\b%s\b" % i, j, text)
        # r"\b%s\b"% enables replacing by whole word matches only
    return text

def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words    


def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words    



def stopword_removal(text):
    ## remove verbs as well
    pos_tagged_tokens = nltk.pos_tag(text)

    list_of_verbs_modals = []
    for i in range(len(pos_tagged_tokens)):
        if pos_tagged_tokens[i][1].startswith('VB') or pos_tagged_tokens[i][1]=="MD" or pos_tagged_tokens[i][1]=="CD":
            list_of_verbs_modals.append(pos_tagged_tokens[i][0])


    stop_words = stopwords.words("english")
    # update stop words list with compensation keywords
    stop_words.extend(list_of_verbs_modals)
    stop_words.extend(["year","description", "years","yrs","team","application","job",
    "holiday","internal","external","company","opportunities","applications"
    "hour","shift","mellon", "knowledge", "month","etc","end","least","experience","skill","new",
    "tool","tools","data","techniques","colleagues","home","referral","holidays","cost"])
    stop_words = set(stop_words)
    cleaned = [word for word in text if word not in stop_words]
    return cleaned


# stemmed and lemma words were both examined to choose which method was best suited
def stemming(text):
    #porter = PorterStemmer()
    porter = LancasterStemmer()
    stemmed = [porter.stem(word) for word in text]
    return stemmed


def lemming(text):
    lemmatizer = WordNetLemmatizer()
    lemmed = [lemmatizer.lemmatize(word) for word in text]
    return lemmed    


def get_top_n_words(corpus):
    vec = CountVectorizer().fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in      
                   vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key = lambda x: x[1], 
                       reverse=True)
    return words_freq

# Most frequently occurring Bi-grams

def get_top_n2_words(corpus, n=None):
    vec1 = CountVectorizer(ngram_range=(2,2), max_features=2000).fit(corpus)
    bag_of_words = vec1.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in     
                  vec1.vocabulary_.items()]
    words_freq = sorted(words_freq, key = lambda x: x[1], 
                reverse=True)
    return words_freq[:n]    


#Most frequently occurring Tri-grams
def get_top_n3_words(corpus, n=None):
    vec1 = CountVectorizer(ngram_range=(3,3), 
           max_features=2000).fit(corpus)
    bag_of_words = vec1.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in     
                  vec1.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], 
                reverse=True)
    return words_freq[:n]

def search_skills(texts, skills_txt):
    skills_list = skills_txt["Skill"].map(lambda x: x.lower()).to_list()
    list_matched = [word for word in texts if word in skills_list]
    return list_matched    