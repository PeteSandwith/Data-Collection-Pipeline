from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import Scraping_Classes as SC
import json
import re
import time
import unittest
import uuid









class Scraper_ObjectTestCase(unittest.TestCase):
    def setUp(self):
        #instantiates self.tester as an instance of the Scraper_Object class
        self.tester = SC.Scraper_Object('energy supplier', 'https://www.trustpilot.com/')
        

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

    def test_scrape_from_cralwer(self):
        self.tester.crawler = ['https://www.trustpilot.com/review/integrityenergy.com']
        self.tester.scrape_from_crawler()
        data = self.tester.scraped_data
        print(data)
        #Checks that data is a list
        self.assertIsInstance(data, list, "The scraped data is not stored in a list")
        #Checks that the list elements (representing data for one specific business) are dictionaries 
        self.assertIsInstance(data[0], dict, "The elements in data are not dictionary objects")
        #The values of the dictionary are liable to change over time; however we can check that all of the keys are correct
        correct_keys = ['Name', 'ID', 'Timestamp', 'Href', 'Number of Reviews', 'Rating', 'Email']
        actual_keys = list(data[0].keys())
        self.assertTrue(correct_keys == actual_keys, "The keys of the dictionary in self.scraped_data are not correct.")

        
if __name__ == "__main__":
    unittest.main()