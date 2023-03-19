# Skills Analysis

## Aims
- Understand the skills employees currently have
- Understand industry demands for DS skills

## Approach
- Collect data on employee CVs and Glassdoor Job descriptions
- Undertake data cleaning and apply nlp techniques
- Apply clustering algorithm to CV data to develop a greater understanding of the demographic of the workforce
- Compare this to analysis of Glassdoor data to indentify gaps in the skills of the workforce
- Create front end dashboard

## To Run
To srape the CVs from a sharepoint location run the download_cvs notebook in sharepoint_scrapper folder. This will save all cvs in the Storage folder. Note: This will currently only run if you provide the FOLDER_NAME variable in the download_cvs notebook and provide an .env file contain the following:

sharepoint_email = "your sharepoint email"
sharepoint_password = ".."
sharepoint_url_site = "the sharepoint url you're scrapping from"
sharepoint_site_name = "the sharepoint site name"
sharepoint_doc_library= "the sharepoint library"

NOTE: For example purposed the CVs in the storage folder are generic CVs created by chatGPT

### Glassdoor scraper
To run the glassdoor scraper run the main.py file from within the glassdoor_scraper/src folder from the terminal
To run the analysis on this data run the data_analysis notebook from within the glassdoor_scraper/src folder

### Dashboard
To run the Dashboard, set you working directory to ".\skills-analysis\skills_dashboard\src\components" and from within the terminal run python main.py

## TODO
- Update Dahsboard to contain analysis from glassdoor