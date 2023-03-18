# This module performs the specific task of retrieving the content of a provided URL

# Standard library imports
import time

# 3rd party imports
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from bs4 import BeautifulSoup as soup


# Verify and correct requested URL scheme
def checkURL(requested_url: str) -> str:

    # If the url does.t start with 'https://', append this to the start of the URL
    if not urlparse(requested_url).scheme:
        requested_url = 'https://' + requested_url

    # Return new URL
    return requested_url


# Fetches data from requested url and parse through beautifulsoup
def get_URL_content(requested_url: str):

    # Get URL
    requested_url = checkURL(requested_url)

    # Try to get URL content
    try:
        # Define headers to be provided for request authentication
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.11 (KHTML, like Gecko) '
            'Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
        }

        # Create an object for requesting URL content
        request_obj = Request(url=requested_url, headers=headers)

        # Open URL
        opened_url = urlopen(request_obj)

        # Read HTML content to variable
        page_html = opened_url.read()

        # Close URL
        opened_url.close()

        # Parse content
        page_soup = soup(page_html, 'html.parser')
        return page_soup, requested_url

    # Print error message
    except Exception as e:
        print(e)


# Run an example if this module is executed as the main file
if __name__ == '__main__':

    # Define an example URL
    url = 'https://www.google.co.uk/'

    # Record execution start time
    start_time = time.time()

    # Return URL content, corrected URL
    page_soup, requested_url = get_URL_content(url)

    # Calculate execution time (for just this one URL)
    time_taken = time.time() - start_time

    # Print parsed URL content and execution time to console
    print(page_soup)
    print(f'[INFO] returned in {time_taken} seconds')
