# Data-Collection-Pipeline
An industry grade data colleciton pipeline which uses the python package Selenium to scrape data from review website Trustpilot. The system automatically controls Chrome to extract relevant data from the website. The data is stored on the cloud using AWS/RDS. It conforms to industry best practices such as being containerised in Docker and running automated tests.

## Milestone 1
- The review website Trustpilot was chosen as a target for data scraping, as it contains several pieces of useful data that could be used to compare different companies (average review, number of reviews, contact email ect). Companies are grouped by category depending on what industry they serve and this was something I wanted the user to be able to specify when running the web scraper.

## Milestone 2
- Selenium Webdriver was used to build the web scraper, as it allows control of a browser to be fully automated. Navigation and interaction of a webpage, as well as data retrieval, can be controlled programmatically within a python script.
- A scraper class was created in python upon which methods will be called in order to control the webdriver and scrape data. The instance variable *self.category* specifies which category of company will be scraped (eg. 'energy supplier', 'furniture store'). The *self.crawler* and *self.scraped_data* instance variables are empty lists which will be filled as different methods are called on the scraper object.
```
class Scraper_Object:
    def __init__(self, category, url):
        self.category = category
        self.url = url
        self.crawler = []
        self.scraped_data = []
        driver.get(url)
```
- Methods were created that allow the driver to navigate the website. For instance the method *search* enters the *self.category* into the search bar and navigates to a page that lists companies relevant to that category
```
def search(self):
        search_bar = driver.find_element(By.XPATH, '//input[@class="herosearch_searchInputField__Pp2MD"]')
        search_bar.send_keys(self.category)
        time.sleep(3)
        #The following line identifies the first suggested category by finding the following sibling of the 'categories' heading under the search box
        first_category = driver.find_element(By.XPATH, '//h4[contains(text(),"Categories")]//following-sibling::a')
        first_category.click()
        time.sleep(3)
```
- Other methods include a *create_crawler* which fills *self_crawler* with hrefs to each individual company
```
def create_crawler(self, length):
        self.length = length
        #creates a list of the html elements corresponding to different companies 
        items_list = driver.find_elements(By.XPATH, '//div[@class="paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_wrapper__2JOo2"]/a')
        #Iterates through the html elements and puts each href into the crawler
        for index in range(0, self.length):
            href = items_list[index].get_attribute('href')
            self.crawler.append(href)
        return self.crawler
```
- The versatility of Selenium is obvious during the webscraping process. It is an extremely flexible tool that allows very specific interaction with webpages based on their HTML. In the blocks of code above we have demonstrated how elements in the HTML can be found using their class, attribute, the text they contain and their relative position to other HTML elements.

## Milestone 3
- A funtion called *scrape_stuff* was created that scrapes data from a single company page and saves it in the form of a python dictionary. Included in the item dictionary is a unique id generated using the uuid package (the uuid4 object is converted to a string to allow it to be saved in a json file later on). The *scrape_stuff* function is called in a method that interates through each link in the crawler
```
def scrape_from_crawler(self):
        for item in self.crawler:
            self.scraped_data.append(scrape_stuff(item))
```
- A method was created to save the scraped data as a json file, which is the standard file format for data exchange. This was done using the built-in python package json. The file name is generated from *self.category* and saved in a directory called raw_data in the root of the project.
```
def save_json(self):
        file_name = "raw_data/{}.json".format(self.category.replace(" ", "_"))
        with open(file_name, 'w') as json_file:
            json.dump(self.scraped_data, json_file)
```
## Milestone 4
- Testing code is vitally important for ensuring that it is running as intended. The unit testing paradigm tests each small, fundamental 'unit' of code independently to check that they function correctly when receiving a particular input.
- In this case the units that were tested were the individual methods of the Scraper_Class. A separate script, test_Scraping_Classes.py, was created to perform unit testing on the methods of the Scraping_Object class. This script imports the classes and methods from Scraping_Classes.py. The built in python module unit was also imported, which allows the user to easily write and run tests.
- Unit tests were written for every public method from the Scraper_Object class. For instance, the unit test for the create_crawler method checks that the crawler that the method returns is a list object, that the entries are string objects and that the crawler is the correct length. 
```
def test_create_crawler(self):
        #Calls the create_crawler method on self.tester with a length argument of 1
        self.tester.create_crawler(2)
    
        #Checks that the lenght of the crawler is equal to the number input into create_crawler
        length = len(self.tester.crawler)
        self.assertEqual(2, length)
        
        #Checks whether the crawler is a list
        self.assertIsInstance(self.tester.crawler, list, "Crawler is not a list object")
        
        #Checks whether the items inside the crawler are strings
        self.assertIsInstance(self.tester.crawler[0], str, "Url in crawler is not a string object")
```
- The test_Scraping_Classes.py script can be run from the terminal to automatically test all of the public methods of the scraper class. If any of these tests fail, a message explaining the reason for the failure will be returned to the terminal:
```
======================================================================
FAIL: test_scrape_from_cralwer (__main__.Scraper_ObjectTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/petersandwith/Documents/AiCore/TrustPilot_WebScraper/test_Scraping_Classes.py", line 46, in test_scrape_from_cralwer
    self.assertTrue(correct_keys == actual_keys, "The keys of the dictionary in self.scraped_data are not correct.")
AssertionError: False is not true : The keys of the dictionary in self.scraped_data are not correct.

----------------------------------------------------------------------
Ran 1 test in 64.602s

FAILED (failures=1)
```
