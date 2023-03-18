# This module performs the specific task of extracting the following fields from a beautiful soup object:
# company_name
# company_star_rating
# role_title
# role_location
# company_type
# industry

# Standard library imports
from time import time
import re

# Local application/library specific imports
# This will depend on whether the module is being run as '__main__' or not
try:
    from scraping_functions.URL_content import get_URL_content
except ModuleNotFoundError:
    from URL_content import get_URL_content


# Extracts desired data from the listing description's body text
def get_listing_desc(listing_soup):

    # Assume the description element cannot be found, so assign field NA
    listing_desc = 'NA'

    # Try to locate an element with the id 'JobDescriptionContainer'
    try:
        # Get description container element
        listing_job_desc_raw = listing_soup.find('div', id='JobDescriptionContainer')

        # Get all bullet point elements from description body
        # Most roles list necessary skills as a bullet point list
        job_desc_items = listing_job_desc_raw.findAll('li')


        # First we will try to focus on list elements (bullet points), this is where employers tend to specify
        # skills. If this fails, default back to the container's raw text.

        # Extract each of the bullet point elements to a list object
        listing_desc_items_lst = []
        for job_desc_item in job_desc_items:
            listing_desc_items_lst.append(job_desc_item.text)

        # Collapse list into a single string
        listing_desc = ' '.join(listing_desc_items_lst)

        # If our description is less than 10 characters long (likely empty), just take the container's raw text
        if len(listing_desc) <= 10:
            listing_desc = listing_job_desc_raw.text


    # If there is an error, leave the field as NA and print the error message
    except Exception as e:
        print(f'[ERROR] {e} in get_listing_desc')

    # Return the listing description string as a tuple
    return (listing_desc,)


def extract_company_info(listing_soup):

    # Assume the return values won't be found and assign NA
    company_type = 'NA'
    industry = 'NA'

    try:
        # If '/Overview/ is found in an <a href> tag, this is a relative link to the hiring company's Glassdoor page
        # e.g '/Overview/Working-at-Noir-EI_IE795725.11,15.htm'
        overview_tag = listing_soup.find(name='a', href=re.compile('/Overview/'))

        # Build the full company page URL
        company_URL = 'www.glassdoor.com' + overview_tag['href']
        
        # Get the URL content from the company's Glassdoor page
        # TODO: Information regarding company revenue, size etc is also available from this object
        company_overview_soup, _ = get_URL_content(company_URL)

        # Find company type element from soup object
        # This is the employer type attrs field (found by manual inspection through browser)
        company_type_element = company_overview_soup.find(
            attrs={'data-test':'employer-type'}
        )

        # Extract company type from element
        company_type = company_type_element.text

        # Find industry element from soup object
        # This is the employer industry attrs field (found by manual inspection through browser)
        industry_element = company_overview_soup.find(
            attrs={'data-test':'employer-industry'}
        )

        # Extract industry from element
        industry = industry_element.text

    # Skip URL and move on
    except Exception as e:
        print('[ERROR] Error occurred in extract_company_info')

    # Return company type and industry
    return (company_type, industry)


# Extracts desired data from a listing banner
def get_listing_banner_info(listing_soup):

    # Try to locate and extract the star rating
    try:
        # This is the star rating class (found by manual inspection through browser)
        star_rating_class = 'css-1pmc6te e11nt52q4'

        # Extract star rating text
        company_star_rating = listing_soup.find(
            'span', class_=star_rating_class
        ).text

        # Remove the '★' symbol, this is the last character
        company_star_rating = company_star_rating[:-1]

    # Set field to NA if there are errors
    except:
        company_star_rating = 'NA'


    # Try to locate and extract the employer name
    try:
        # This is the employer name attrs field (found by manual inspection through browser)
        # Extract employer name
        company_name = listing_soup.find(name = 'div', attrs={'data-test':'employer-name'}).text

        # If the company star rating was found, this we occupy the last 4 character of the name field, as it is a child element (e.g '5.0★'), so remove this.
        if company_star_rating != 'NA':
            company_name = company_name[:-4]

    # Set field to NA if there are errors
    except:
        company_name = 'NA'

    # Try to locate and extract the role title
    try:
        # This is the role title attrs field (found by manual inspection through browser)
        # Extract role title
        role_title = listing_soup.find(name = 'div', attrs={'data-test':'job-title'}).text

    # Set field to NA if there are errors
    except:
        role_title = 'NA'

    # Try to locate and extract the role location
    try:
        # This is the role location class (found by manual inspection through browser)
        role_location_class = 'css-1v5elnn e11nt52q2'

        # Extract role title
        role_location = listing_soup.find(
            'div', class_=role_location_class
        ).text

    # Set field to NA if there are errors
    except:
        role_title = 'NA'

    # Try to locate and extract the company type and industry
    try:
        company_type_and_industry = extract_company_info(listing_soup)

    # Set both fields to NA if there are errors
    except:
        company_type_and_industry = ['NA'] * 2
        
    return (
    company_name,
    company_star_rating,
    role_title,
    role_location
    ) + company_type_and_industry


# Extract data from listing
def get_listing_info(url):

    # Assume the content request will fail
    request_success = False

    # Try to get the URL content
    try:

        # Retrieve `soup object` (URL content) and the cleaned URL
        listing_soup, _ = get_URL_content(url)
        
        # Change request to success
        request_success = True
    
    # If there are errors, skip the URL and set all fields to NA
    except Exception as e:
        print(f'[ERROR] Error occurred in get_listing_info, requested url: {url} is unavailable.')
        return ('NA', 'NA', 'NA', 'NA', 'NA', 'NA')

    # Continue if the request succeeds
    if request_success:

        # Retrieve information about the listing and store in tuple
        listing_details = get_listing_banner_info(listing_soup)

        # Retrieve listing description body
        listing_desc = get_listing_desc(listing_soup)

        # Append description body to existing details tuple
        listing_details = listing_details + listing_desc

        # Return listing details
        return listing_details


# Run an example if this module is executed as the main file
if __name__ == '__main__':

    # Define an example Glassdoor job listing
    url = 'https://www.glassdoor.sg/job-listing/front-end-developer-noir-consulting-JV_IC2671300_KO0,19_KE20,35.htm?jl=1008243542129&pos=108&ao=1110586&s=58&guid=000001843e145a18a6bc9e309a26f271&src=GD_JOB_AD&t=SR&vt=w&cs=1_3ca9bf7b&cb=1667488832455&jobListingId=1008243542129&cpc=F41FEAB56D215062&jrtk=3-0-1ggv18mifjfkr801-1ggv18mjbi7l9800-386cb0562708e366--6NYlbfkN0Aj4-Lc4C6Hb0ykU3jOktLDIAAw4anZygn__rtZFvHgNTA_qTH8-VQLROOIkIXkVVD_P9MtkjVYDpXvWy5BxDMzFOESZCPbApnnq_u-Z2bEMzOzafxBinL5cZZ0dNiruou2OcnEeWmwpEbZislmQr3MyPCfl4qhKro6j3lXVTJZwSwBB1YaV4RXVdOEYJxIHPLofBM-pua250hVS5FPr5iKqQCRyrIzZeqcSSyAOW8qUhg7n0EHI3DCJ07slofn8AxAY8bPCkWuJpsXj2hu7Avt3UkG10xrss7QnUCVXGM7QuXPvyYY7mnXg89sD7Pg5mzdS5uLtUSMYXeU3pKZYm3qf-_owd4O5J7sfFbOTa45DDVXCIR6AGwHFGQRFDhsVyY31PiHReqfkssMMUJZ4Rr2R910jIcPCxsCTdDt98AJ6H9N-dm1Z72nyrbm5WrjPlJtbH9300o-iDpNCUarzTBPi7W_JFTtlgYfG-h1qV96LLa20eBefV1fcm__4dvtUO8%253D&ctt=1667488842530'
    
    # Record execution start time
    start_time = time()

    # Return tuple containing parsed listing details
    returned_tuple = get_listing_info(url)

    # Calculate execution time (for just this one URL)
    time_taken = time() - start_time

    # Print parsed tuple content and execution time to console
    print(returned_tuple)
    print(f'[INFO] returned in {time_taken} seconds')
