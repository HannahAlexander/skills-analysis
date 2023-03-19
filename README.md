# Skills Analysis
Updated: 03/11/22

Analysis of data that may give us insight of strength and weaknesses of knowledge throughout the business compared to what projects we win and lose as a business. 

## Aims
- Understand the skills DS at Ascent currently have
- Understand industry demands for DS skills


## Approach
- Collect data on employee CVs and Glassdoor Job descriptions
- Conduct analysis on data
- Create front end dashboard

## Outcome
-


## To Run
To srape the CVs from a sharepoint location run the download_cvs notebook in sharepoint_scrapper folder. This will save all cvs in the Storage folder. Note: This will currently only run if you provide the FOLDER_NAME variable in the download_cvs notebook and provide an .env file contain the following:

sharepoint_email = "your sharepoint email"
sharepoint_password = ".."
sharepoint_url_site = "the sharepoint url you're scrapping from"
sharepoint_site_name = "the sharepoint site name"
sharepoint_doc_library= "the sharepoint library"

NOTE: For example purposed the CVs in the storage folder are generic CVs created by chatGPT

### Glassdorr scraper
To run the glassdoor scraper run the main.py file from within the glassdoor_scraper/src folder from the terminal
To run the analysis on this data run the data_analysis notebook from within the glassdoor_scraper/src folder
