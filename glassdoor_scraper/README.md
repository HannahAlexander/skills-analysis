### Code that scrapes the popular job listings from "Glassdoor"
* Functions without any authentication e.g. user sign-ins/ API tokens and keys. Users simply modifies a config file (glassdoor-scraper\src\config.json) to provide: 
   - A 'base URL' to scrape from, based on desired job role and country.
   - A 'target job size' i.e. number of individual job listings to scrape from.
* Script scrapes:
   - Job link, role, company, industry and job description from job listing results. 
* Information collected are accessible to users in the form of an output csv.
* Script has been tested and verified to be working as expected for a job with: 
   - A target job size of < 2000 individual listings, 
   - Multiple pages > 10 pages of job listing links.

Data Analysis Notebook: glassdoor-scraper\data_analysis.ipynb
* text cleaning/nlp/word tokens 
* fuzzy matching for similar skills based on glassdoor-scraper\input_data\skills.txt 


### ENVIRONMENT SETUP
Run the following code to create the env with the required dependencies 
 `conda env create -f glassdoor_scraper.yml`
 Install `ascent_nlp` into environment from folder using command `pip install -e .`