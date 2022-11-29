from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import re
import uuid
import json
import unittest
import Scraping_Classes as SC






class Scraper_ObjectTestCase(unittest.TestCase):
    def setUp(self):
        self.tester = SC.Scraper_Object('energy supplier', 'https://www.trustpilot.com/')
        

    def test_create_crawler(self):
        self.tester.create_crawler(1)
        length = len(self.tester.crawler)
        #Checks that the lenght of the crawler is equal to the number input into create_crawler as length
        self.assertEqual(1, length)
        #Checks whether the crawler is a list
        self.assertIsInstance(self.tester.crawler, list, "Crawler is not a list object")
        #Checks whether the items inside the crawler are strings
        self.assertIsInstance(self.tester.crawler[0], str, "Url in crawler is not a string object")

    #def test_scrape_stuff(self):
        #url = 'https://www.trustpilot.com/review/igs.com'
       # data = scrape_stuff(url)
        #Checks whether the scrape_stuff function returns a dictionary.
       #test.assertIsInstance(data, dict, "The scraped data is not stored in a dictionary")
        #Could be good to check the values of the different items in the dictionary, however these will possibly change over time

if __name__ == "__main__":
    unittest.main()