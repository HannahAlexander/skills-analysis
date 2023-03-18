# Standard library imports
import json
import os
from datetime import datetime
import csv

# 3rd party imports
import enlighten

# Local application/library specific imports
from scraping_functions.search_result import get_search_size, get_listing_URLs
from scraping_functions.listing_info import get_listing_info

# Initialise a scraper class
class glassdoor_scraper:

    # Initialise class
    def __init__(self) -> None:

        # Get variables from config.json
        search_url, target_num_listings = self.load_configs()

        # Initialise output director
        output_dir = 'output/glassdoor_scraping'
        os.makedirs(output_dir, exist_ok=True)

        # Define output csv file to store scraped urls
        scraped_url_csv_name="output/glassdoor_scraping/scraped_urls.csv"

        # TODO : Potential improvements
        # Add logic for reading and writing to the same file so we can expand with daily runs
        # Can we skip the scraping existing URLs?
        # IDEA: Load all the listing URLs from every page, then skip URL if it already exists in the output CSV

        # Get current time and format as string
        now = datetime.now().strftime('%d-%m-%Y-%H-%M')

        # Define an output csv file name in the output directory
        output_file_name = output_dir + '/listings_scraped_raw_' + now + '.csv'

        # Define the CSV column headers
        csv_headers = [(
                'company_name',
                'company_star_rating',
                'role_title',
                'role_location',
                'industry',
                'company_type',
                'listing_desc',
                'listing_url',
                'page_url',
                'page_num'
        )]

        # Write column headers to the CSV before starting scraping
        self.file_writer(contents=csv_headers, output_file_name=output_file_name)

        # Establish the number listings and pages this search generates
        num_listings, num_pages = get_search_size(search_url)

        # Print number listings and pages to console
        print(f'[INFO] The number of job listings for this search result is: {num_listings}')
        print(f'[INFO] The number of pages for this search result is: {num_pages}')

        # If the number of listings specified in `config.json` is greater than the available listings from the search, throw error and exit
        if target_num_listings >= num_listings:
            print(
                f'[ERROR] Target number of listings {target_num_listings} larger than available listings \
                from search {num_listings}. Exiting program...\n'
                )
            os._exit(0)

        # Initialise enlighten_manager (This is simply a visual progress bar for the terminal)
        enlighten_manager = enlighten.get_manager()

        # Define progress bar for overall job
        progress_overall = enlighten_manager.counter(
            total=target_num_listings,
            desc='Total progress',
            unit='listings',
            color='green',
            leave=False,
        )

        # Initialise variables
        page_index = 1
        total_listings_scraped = 0

        # Initialise a list to store tuples, each tuple will contain the results from one job listing
        listing_tuples = []

        # Initialise first page URL using search_url
        page_url = search_url.replace('.htm', '_IP1.htm')

        # Scrape listings until the target number is reached
        while total_listings_scraped < target_num_listings:

            # Retrieve set containing each listing on the page and the number of unique listing URLs
            listing_links_set, num_unique_listings = get_listing_URLs(page_url, scraped_url_csv_name)

            ######


            # Define progress bar for current page
            progress_page = enlighten_manager.counter(
                total=num_unique_listings,
                desc='Listings scraped from page',
                unit='listings',
                color='blue',
                leave=False,
            )

            # Print info regarding this page to console
            print(f'[INFO] Processing page index {page_index}: {page_url}')
            print(f'[INFO] Found {num_unique_listings} links in page index {page_index}')

            # Loop through this page's listings to scrape
            for listing_url in listing_links_set:

                # Stop if the number of listings scraped reaches the target number
                if total_listings_scraped == target_num_listings:
                    break

                # TODO implementing cache here will improve speed

                # Get details for this listing (as tuple)
                listing_tuple = (get_listing_info(listing_url) + (listing_url,) + (page_url,) + (page_index,))

                # Append this listing's tuple to the list of returned tuples
                listing_tuples.append(listing_tuple)

                # Update the page progress bar after each listing
                progress_page.update()
                progress_overall.update()

                # Update counter for number of listings scraped
                total_listings_scraped += 1

            # Close page progress bar ready to reinitialize for next page
            progress_page.close()

            # Print progress at end of page
            print(f'[INFO] Finished processing page index {page_index}')
            print(f'Total number of listings processed: {total_listings_scraped}')

            # Update page number
            page_index = page_index + 1
            
            # Update page URL to next page number
            page_url = self.update_page_url(current_page_url=page_url, desired_page_index=page_index)


        # Write scraped listings to CSV
        self.file_writer(contents=listing_tuples, output_file_name=output_file_name)

    # Retrieve user parameters from `config.json`
    def load_configs(self):

        # Open config file and load content
        with open('glassdoor_scraper/src/config.json') as config_file:
            configurations = json.load(config_file)

        # Extract parameters as variables
        search_url = configurations['base_url']
        target_num_listings = int(configurations['target_num'])

        # Return variables
        return search_url, target_num_listings

    # Write the scraped results to a CSV in the output folder
    def file_writer(self, contents, output_file_name):

        # Open output CSV
        with open(file=output_file_name, mode='a', newline='') as output:
            output_csv = csv.writer(output)

            # Try to write the job listing tuples to the output CSV (row by row)
            for row in contents:

                # Try to write the job listing to the output CSV
                try:
                    output_csv.writerow(row)
                    
                # Print error if necessary
                except Exception as e:
                    print(f'[WARN] Problem occurred in file_writer: {e}')


    # Update url to move to the next page
    def update_page_url(self, current_page_url, desired_page_index):

        # Determine the URL substring relating to the current and desired pages
        # This is the last few characters of the URL string
        current_substring = '_IP' + str(desired_page_index - 1) + '.htm'
        desired_substring = '_IP' + str(desired_page_index) + '.htm'

        # Get desired page URL from old page URL
        new_page_url = current_page_url.replace(current_substring, desired_substring)

        # Return desired page URL
        return new_page_url


# Run pipeline to scrape job listings if this file is executed as the main file
if __name__ == '__main__':
    # Execute scraper given config.json argument
    glassdoor_scraper()
