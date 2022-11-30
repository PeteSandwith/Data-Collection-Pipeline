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
        #instantiates self.tester as an instance of the Scraper_Object class
        self.tester = SC.Scraper_Object('energy supplier', 'https://www.trustpilot.com/')
        

    #def test_create_crawler(self):
        #Calls the create_crawler method on self.tester with a length argument of 1
        #self.tester.create_crawler(2)
    
        #Checks that the lenght of the crawler is equal to the number input into create_crawler
        #length = len(self.tester.crawler)
        #self.assertEqual(2, length)
        #Checks whether the crawler is a list
        #self.assertIsInstance(self.tester.crawler, list, "Crawler is not a list object")
        #Checks whether the items inside the crawler are strings
        #self.assertIsInstance(self.tester.crawler[0], str, "Url in crawler is not a string object")

    def test_scrape_from_cralwer(self):
        self.tester.crawler = ['https://www.trustpilot.com/review/integrityenergy.com']
        self.tester.scrape_from_crawler()
        data = self.tester.scraped_data
        #Checks that data is a list
        self.assertIsInstance(data, list, "The scraped data is not stored in a list")
        #Checks that the list elements (representing data for one specific business) are dictionaries 
        self.assertIsInstance(data[0], dict, "The elements in data are not dictionary objects")
        
if __name__ == "__main__":
    unittest.main()