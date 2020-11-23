from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
import sys

chrome_driver_path = '/media/danish-khan/New Volume/Web_scraping/rgcrawler2/chromedriver'

url = 'https://www.researchgate.net/login'

chrome_options = Options()
#chrome_options.add_argument('--headless')

driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

driver.get(url)

username = 'danishkhankd237@gmail.com'
password = 'danish3.16khan'

driver.find_element_by_id("input-login").send_keys(username)
driver.find_element_by_id("input-password").send_keys(password)
driver.find_element_by_class_name("nova-c-button__label")
time.sleep(20)

#driver.close()

