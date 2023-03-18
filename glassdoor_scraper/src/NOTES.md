## Glassdoor scrapper 

####  Retrieving variables with our web scraper and saving them into a data frame.
Begin with the page from where you will gather your data. The following URL provides a list with open DS positions in the UK.

url = “https://www.glassdoor.sg/Job/united-kingdom-data-scientist-jobs-SRCH_IL.0,14_IN2_KO15,29.htm”

For each of the URLs listed there, we need to tell our driver to open and retrieve the following information: 

- company name (css selector: `css-16nw49e e11nt52q1`)
- job description (find container inside HTML: `JobDescriptionContainer`)
- star rating (css selector: `css-1pmc6te e11nt52q4`)
- offered role (css selector: `css-17x2pwl e11nt52q6`)
- location (css selector: `css-1v5elnn e11nt52q2`)
- industry (seems to be a blocker atm) - The selector for company industry is `'//*[@id="EIOverviewContainer"]/div/div[1]/ul/li[6]/div'`. We are able to scrape the listed job URL, however for getting the industry company we need to use XPath, which is not supported in Beautiful Soup.



## LIMITATIONS 
- Glassdoor does not have any public API for Jobs (indeed is the same)
- If you were to do a get request to multiple links at once, it is likely that your IP address will get blocked, or you’ll have a slow connection. 


## NEXT steps 

- bypass the issue with industry. 
- crawl more than first page of URLs (i.e. threshold of 10 pages).
- bypass banned IP (??) this can be tricky. 



