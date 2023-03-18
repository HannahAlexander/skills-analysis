from asyncio.windows_events import NULL
import docx2txt
import os
from bs4 import BeautifulSoup
from heapq import nlargest
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
import plotly.express as px
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
import inflect
from nltk import LancasterStemmer
import sys

# extract text
def extract_cv(folder = "../storage/"):
    
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

