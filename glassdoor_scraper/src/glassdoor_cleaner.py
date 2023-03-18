# Standard library imports
import pandas as pd
import os
import glob

# 3rd party imports
from nltk.tokenize import RegexpTokenizer
from fuzzywuzzy import fuzz
from datetime import datetime

import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('omw-1.4')

# Local application/library specific imports
from ascent_nlp import text_cleaning

class glassdoor_cleaner:

    def __init__(self) -> None:

        # Get list of raw Glassdoor listings
        path = "output/glassdoor_scraping"
        listings_list = [filename for filename in os.listdir(path) if filename.startswith("listings_scraped_raw")]

        # Concat listings
        listings_raw = pd.DataFrame()
        for listing in listings_list:
            listing_pd = pd.read_csv(os.path.join(path, listing), encoding_errors= 'replace')
            listings_raw = pd.concat([listings_raw, listing_pd])

        # Extract fields of interest
        listings  = listings_raw[['company_name', 'role_title', 'role_location', 'industry', 'company_type', 'listing_desc']]

        # Remove listings where the description is empty
        listings.dropna(subset=['listing_desc'], inplace=True)

        # Clean text and set to lower case
        listings['listing_desc_clean'] = listings['listing_desc'].apply(text_cleaning.clean_text)
        listings['listing_desc_clean'] = listings['listing_desc_clean'].str.lower()

        # Create a dictionary of words-to-replace and words-to-replace-with
        dictionary = {'r':'r_code',
                    'machine learning':'machine_learning',
                    'power bi':'power_bi',
                    'github':'git', 'gitlab':'git', 'version':'git',
                    'ci':'ci_tools',
                    'db':'database',
                    'ai':'artificial_intelligence',
                    'computer vision':'computer_vision',
                    'a/b':'ab_testing',
                    'big data': 'big_data'
                    }

        # Execute the replacements
        listings['listing_desc_clean'] = listings['listing_desc_clean'].apply(text_cleaning.replace_all, dic=dictionary)

        # Initalise a tokenizer instance
        tokenizer = RegexpTokenizer(r'\w+')

        # Tokenize on a word level
        listings['desc_tokenized_word'] = listings['listing_desc_clean'].apply(lambda row: tokenizer.tokenize(row))

        # Remove punctuation marks
        listings['desc_tokenized_word'] = listings['desc_tokenized_word'].apply(lambda row: text_cleaning.remove_punctuation(row))

        # Remove non-ascii characters
        listings['desc_tokenized_word'] = listings['desc_tokenized_word'].apply(lambda row: text_cleaning.remove_non_ascii(row))

        # Remove stopwords
        listings['desc_tokenized_word'] = listings['desc_tokenized_word'].apply(text_cleaning.stopword_removal)

        # Retrieve skills bank as a list
        with open('glassdoor_scraper/input_data/skills.txt') as f:
            skills_str = f.read().lower() # Read file content to a long string (in lowercase)
            skills_list = skills_str.split('\n') # Split on newline character to list

        # Get all the words that have appeared in any description to a list
        all_words_corpus = []
        for row in listings['desc_tokenized_word']: all_words_corpus.extend(row)

        # Convert to set then back to list to drop duplicates
        all_words_corpus = set(all_words_corpus)
        all_words_corpus = list(all_words_corpus)

        # Create list of fuzzy matches for each word found in the descriptions and a proposed substitute word.
        # Keep only the best match for each word.
        fuzzy_matches_list = [max([(fuzz.token_set_ratio(proposed_match, word_from_desc), word_from_desc, proposed_match) for proposed_match in skills_list]) for word_from_desc in all_words_corpus]

        # Move matches to DF
        fuzzy_matches = pd.DataFrame(fuzzy_matches_list, columns=['similarity_score', 'word_from_description', 'proposed_match'])

        # Keep only matches that reach a selected similarity threshold
        similarity_threshold = 80
        fuzzy_matches.query('similarity_score >= @similarity_threshold', inplace=True)

        # Dictionary of words from the descriptions and their fuzzy matched equivalents
        fuzzy_dict = fuzzy_matches.set_index('word_from_description').to_dict()['proposed_match']

        # Create new column from the tokenized words with the new fuzzy matched equivalents
        # Words will be dropped entirely if they have no match
        listings['fuzzy_matched_words'] = listings.apply(
                lambda listings: [
                    fuzzy_dict[word]
                    for word in listings['desc_tokenized_word']
                    if word in fuzzy_dict.keys()
                ],
                axis=1,
            )

        # Add columns for stemmed and lemma words
        listings['fuzzy_stemmed'] = listings['fuzzy_matched_words'].apply(text_cleaning.stemming)
        listings['fuzzy_lemmed'] = listings['fuzzy_matched_words'].apply(text_cleaning.lemming)

        # Get current time and format as string
        now = datetime.now().strftime('%d-%m-%Y')

        # Define an output csv file name in the output directory
        output_file_name = 'output/glassdoor_scraping/listings_cleaned_' + now + '.csv'

        # Write the cleaned results to a CSV in the output folder
        listings.to_csv(path_or_buf = output_file_name)
        print("[INFO] Clean listings saved to", output_file_name)

if __name__ == '__main__':
    glassdoor_cleaner()
