# Data-Collection-Pipeline
An industry grade data colleciton pipeline which uses the python package Selenium to scrape data from review website Trustpilot. The system automatically controls Chrome to extract relevant data from the website. The data is stored on the cloud using AWS/RDS. It conforms to industry best practices such as being containerised in Docker and running automated tests.

## Milestone 1
- The review website Trustpilot was chosen as a target for data scraping, as it contains several pieces of useful data that could be used to compare different companies (average review, number of reviews, contact email ect). Companies are grouped by category depending on what industry they serve and this was something I wanted the user to be able to specify when running the web scraper.

## Milestone 2
- In order to scrape data Selenium WebDriver was used, as it allows control of a browser to be fully automated. Navigation and interaction of a webpage, as well as data retrieval, can be controlled programmatically within a python script.
- A scraper class was created in python upon which methods will be called in order to control the webdriver and scrape data. 
```class Scraper_Object:
    def __init__(self, category, url):
        self.category = category
        self.url = url
        self.crawler = []
        self.scraped_data = []
        driver.get(url)```
