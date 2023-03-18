# This module performs the specific task of extracting the URLs to each job listing from a single URL representing a Glassdoor search

# Standard library imports
import re
import csv
from time import time
import pandas as pd

# Local application/library specific imports
# This will depend on whether the module is being run as '__main__' or not
try:
    from scraping_functions.URL_content import get_URL_content
except ModuleNotFoundError:
    from URL_content import get_URL_content


# Extract number of job listings posted for this particular search
def get_search_size(url: str):

    # Get the URL content from the Glassdoor search result
    search_soup, _ = get_URL_content(url)

    # Try to determine the number of listings
    try:

        # Get number of listings element
        num_listings_element = search_soup.find(
            attrs={'data-test':'jobsCount'}
        )

        # Extract text (e.g. '1541 jobs')
        num_listings_raw = num_listings_element.text

        # Remove any non-numeric characters
        num_listings = re.sub(r'\D', '', num_listings_raw)

        # Convert result to integer object
        num_listings = int(num_listings)

    # If there is an error, print error and assign NA to the field
    except Exception as e:
        print('[ERROR] Error occurred in get_search_size')
        print('Failed to determine the number of listings')
        print(e)
        num_listings = 'NA'

    # Try to determine the number of pages
    try:

        # Get number of pages element
        num_pages_element = search_soup.find(
            attrs={'data-test':'pagination-footer-text'}
        )

        # Extract text (e.g. 'Page 1 of 30')
        num_pages_raw = num_pages_element.text

        # Remove any non-numeric characters, then also remove the first character, as this is the page '1' of... character
        num_pages = re.sub(r'\D', '', num_pages_raw)[1:]

        # Convert result to integer object
        num_pages = int(num_pages)

    # If there is an error, print error and assign NA to the field
    except Exception as e:
        print('[ERROR] Error occurred in get_search_size')
        print('Failed to determine the number of listings')
        print(e)
        num_pages = 'NA'

    # Return number of listings and pages
    return (num_listings, num_pages)


def read_url_csv(scraped_url_csv_name: str) -> set:
    """
    Takes in string of csv where previously scraped urls are stored.
    Returns set of urls.
    If csv does not exist, create an empty set to write to csv later.
    """
    try:
        with open(scraped_url_csv_name, newline='') as f:
            reader = csv.reader(f)

            # transform list of lists to set
            saved_urls = {i for lst in list(reader) for i in lst}

        print("Successfully read ", len(saved_urls), " urls from", scraped_url_csv_name)
    except Exception as e:
        print("[ERROR]", e)
        saved_urls = set()
        print("Created empty set of urls")
    return saved_urls


def build_full_urls(search_soup) -> set:
    """
    Takes page_soup object as input and returns full urls for each link on page
    """
    # Try to get the links for every job listing in the search results
    try:
        # Find the link element to every job listing
        listing_link_elements =  search_soup.find_all(name = 'a', class_='jobLink', href=True)

        # Build the full URL for each element from the href
        listing_links = ['www.glassdoor.com' + tag['href'] for tag in listing_link_elements]

        # Convert to set in case any jobs are posted twice
        all_urls_scraped = set(listing_links)

        # Check the number of urls scraped is more than zero
        assert len(all_urls_scraped) > 0

    # Print error message if necessary
    except Exception as e:
        print(f'[ERROR] Error occurred in build_full_urls')
        print(e)

    return all_urls_scraped


def get_unique_urls(all_urls_scraped: set, saved_urls: set) -> tuple[set, int]:
    """
    Takes all_urls_scraped from build_full_urls and saved_urls from read_url_csv
    and returns unique_urls which have not been saved/scraped before.
    """

    try:
        # compare sets
        unique_urls = all_urls_scraped.difference(saved_urls)
        print("[INFO] Urls successfully compared")

        # find length of resultings lists
        no_unique_urls = len(unique_urls)
        repeated_urls = len(all_urls_scraped) - no_unique_urls

        print("[INFO]", no_unique_urls, "unique urls found")
        print("[INFO]", repeated_urls, "repeated urls found")

    except Exception as e:
        print("[ERROR] Error has occured in get_unique_urls")
        print(e)

    return unique_urls, no_unique_urls
    

def url_file_writer(unique_urls: set, scraped_url_csv_name: str):
    """
    Take in set of unique_urls and name of output csv and apends set to csv
    """
    try:
        with open(scraped_url_csv_name, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(list(unique_urls))
            f.close()
        print("[INFO]", len(unique_urls), "urls saved to ", scraped_url_csv_name)
    # Print error if necessary
    except Exception as e:
        print(f'[WARN] Problem occurred in file_writer: {e}')


# Extract listing URLs
def get_listing_URLs(url: str, scraped_url_csv_name: str) -> tuple[set, int]:

    # Get the URL content from the Glassdoor search result
    search_soup, _ = get_URL_content(url)

    # Return full urls from search soup
    all_urls_scraped = build_full_urls(search_soup)

    # Get previously scraped urls
    saved_urls = read_url_csv(scraped_url_csv_name)

    # check recenly scraped urls against previously scraped urls
    unique_urls, no_unique_urls = get_unique_urls(all_urls_scraped, saved_urls)

    # add unique urls to csv of saved urls
    if no_unique_urls > 0:
        url_file_writer(unique_urls, scraped_url_csv_name)

    # Return the set of listing URLs and the number of unique listings
    return unique_urls, no_unique_urls


# Run an example if this module is executed as the main file
if __name__ == '__main__':

    # Define an example Glassdoor search result
    url = 'https://www.glassdoor.sg/Job/united-kingdom-data-scientist-jobs-SRCH_IL.0,14_IN2_KO15,29.htm'

    # Record execution start time
    start_time = time()

    # Return URL content, corrected URL
    num_listings, num_pages = get_search_size(url)

    # Return set containing each listing on the page and the number of unique listing URLs
    listing_links_set, num_unique_listings = get_listing_URLs(url, "output/glassdoor_scraping/scraped_urls_test.csv")

    # Calculate execution time (for just this one search)
    time_taken = time() - start_time

    # Print the number of job listings and pages to console
    # print(f'[INFO] Number of job listings in range: {num_listings}, number of pages in range: {num_pages}')

    # Print the set of unique listing URLs and the number thereof to console
    # print(f'[INFO] Number of unique listing URLs in range: {num_unique_listings}\nSet of unique listing URLs:\n\n{listing_links_set}')

    # Print execution time to console
    print(f'[INFO] returned in {time_taken} seconds')

    print([x[-5:] for x in list(listing_links_set)])

