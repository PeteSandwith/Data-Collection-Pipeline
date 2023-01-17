from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import json
import re
import time
import uuid


class Scraper_Object:
    """Class upon which methods can be called to drive Google Chrome webrowser and scrape data.

    Various methods can be called on this object to drive the browser and navigate the website. These include methods to accept cookies, search for a particular category of business, create a crawler, scrape data from each individual company's webpage, and save the saved data as a json file. 

    Attributes:
        self.category: String object that indicates what the user would like to search for.
        self.url: String object, the url of the website.
        self.crawler: List object to be filled by create_crawler method.
        self.scraped_data: List object to be filled with data scraped from the website.
    
    """

    def __init__(self):
        """Instantiates an instance of the Scraper_Object class.
        
        Args:
            category: String object that indicates what the user would like to search for.
            url: String object, the url of the website. 
        """
        #The following code specifies the option settings that are required to run the webdriver in headless mode
        options = Options()
        #Skips certain security features 
        options.add_argument('--no-sandbox')
        #The following code ensures that the web driver runs in headless mode with no GUI
        options.add_argument("--headless")
        #Disables memory sharing between system and container
        options.add_argument('--disable-dev-shm-usage')
        #Disables GPU usage for windows
        options.add_argument('--disable-gpu')
        options.add_argument("window-size=1920,1080")
        self.driver = webdriver.Chrome(options=options)
    
        self.category = input("Input the category you would like to search for:")
        self.length = int(input("Input the number of companies you would like to extract data from:"))
        self.url = 'https://www.trustpilot.com/'
        self.crawler = []
        self.scraped_data = []
        self.driver.get(self.url)
        self.__accept_cookies__()
        self.__search__()

    def __accept_cookies__(self):
        """Idenfies the 'accept cookies' button and clicks it."""
        time.sleep(12)
        accept_cookies_button = self.driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
        accept_cookies_button.click()
        time.sleep(3)

    def __search__(self):
        """Searches for the category.
        
        A method that navigates to the search bar, searches for the category that the user input when initialising the class and then directs the driver to the page containing businesses that fall into that category.
        """
        search_bar = self.driver.find_element(By.XPATH, '//input[@class="styles_searchInputField__Ltvjz"]')
        search_bar.send_keys(self.category)
        time.sleep(3)
        #The following line identifies the first suggested category by finding the following sibling of the 'categories' heading under the search box
        first_category = self.driver.find_element(By.XPATH, '//h4[contains(text(),"Categories")]//following-sibling::a')
        first_category.click()
        time.sleep(3)
    
    def create_crawler(self):
        """Creates a list object with hrefs as the individual elements.
        
        Iterates through each of the items in the search results and adds the individual href for each item's webpage to a list.append

        Args:
            length: int object that specifies how many different hrefs should be added to the crawler.

        Returns:
            self.crawler: list object that contains hrefs for individual businesses.
        """
        #While loop adds hrefs to the crawler whilst the desired length of the crawler is greater than 20 (there are 20 items on each page of search results)
        while self.length > 20:
            #creates a list of the html elements corresponding to different companies 
            business_list = self.driver.find_elements(By.XPATH, '//div[@class="paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_wrapper__2JOo2"]/a')
            #Iterates through the html elements and puts each href into the crawler
            for index in range(0, 20):
                href = business_list[index].get_attribute('href')
                self.crawler.append(href)
            self.length -= 20
            #Try to click on the next page button
            self.__next_page__()
            time.sleep(3)
            
        
        #creates a list of the html elements corresponding to different companies
        business_list = self.driver.find_elements(By.XPATH, '//div[@class="paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_wrapper__2JOo2"]/a')
        #Iterates through the html elements and puts each href into the crawler
        for index in range(0, self.length):
            href = business_list[index].get_attribute('href')
            self.crawler.append(href)
        return self.crawler

    def scrape_from_crawler(self):
        """Scrapes data from the webpage of each business and adds this data to scraped_data.
        
        Iterates through each link from the self.crawler list and uses the scrape_stuff function to scrape all relevant data from each webpage."""
        for business in self.crawler:
            self.scraped_data.append(self.__scrape_stuff__(business))

    def save_json(self):
        """Saves scraped data as a json file.
        
        Uses the self.category to generate a file name and saves the data in scraped_data as a json file. The file is saved in a folder called raw_data in the root of the project."""
        file_name = "/Users/petersandwith/Documents/AiCore/TrustPilot_WebScraper/raw_data/{}.json".format(self.category.replace(" ", "_"))
        with open(file_name, 'w') as json_file:
            json.dump(self.scraped_data, json_file)
        self.driver.quit()


    def __scrape_stuff__(self, url):
        """Scrapes data from a webpage.
    
        A function that scrapes relevant data from a single url and creates a dictionary that contains the scraped data.

        Args:
            url: String object, the href for the webpage to be scraped.
    
        Returns:
            item_dictionary: Dictionary object that maps keys to the corresponding data which have been scraped from the webpage.
        """
        self.driver.get(url)
        time.sleep(1)
        item_dictionary = {}  

        #Finds name of company
        Name = self.driver.find_element(By.XPATH, '//span[@class="typography_display-s__qOjh6 typography_appearance-default__AAY17 title_displayName__TtDDM"]/.').text
        item_dictionary['Name'] = Name

        #Gives the item a unique ID (uuid4)
        item_dictionary['ID'] = str(uuid.uuid4())

        #Gives the item a timestamp
        item_dictionary['Timestamp'] = time.time()

        #Adds the href to item_dictionary
        item_dictionary['Href'] = url

        #Finds the number of reviews
        try:
            Num_reviews = self.driver.find_element(By.XPATH, '//p[@class="typography_body-l__KUYFJ typography_appearance-default__AAY17"]/.').text
            Number_reviews = Num_reviews.split(' ')
            item_dictionary["Number of Reviews"] = Number_reviews[0]
        except:
            item_dictionary["Number of Reviews"] = "N/A"

        #Finds the rating 
        try:
            Rating = self.driver.find_element(By.XPATH, '//span[@class="typography_heading-m__T_L_X typography_appearance-default__AAY17"]').text
            item_dictionary["Rating"] = Rating
        except:
            item_dictionary["Rating"] = "N/A"
        #Finds the email of the company
        try:
            Email = self.driver.find_element(By.XPATH, '//a[@class="link_internal__7XN06 typography_body-m__xgxZ_ typography_appearance-action__9NNRY link_link__IZzHN link_underlined__OXYVM"]').text
            item_dictionary['Email']= Email
        except:
            item_dictionary['Email']= "N/A"

        return item_dictionary

    def __next_page__(self):
        next_page_button = self.driver.find_element(By.XPATH, '//a[@aria-label="Next page"]')
        next_page_button.click()
        

if __name__ == "__main__":
    Scraper = Scraper_Object()
    Scraper.create_crawler()
    Scraper.scrape_from_crawler()
    print(Scraper.scraped_data)
    Scraper.save_json()
   