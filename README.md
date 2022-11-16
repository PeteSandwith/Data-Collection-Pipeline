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

