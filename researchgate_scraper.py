from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

login_url = 'https://www.researchgate.net/login'
base_url = "https://www.researchgate.net/institution/Islamia_College_Peshawar/department/Department_of_Computer_Science/members"
chrome_driver_path = '/media/danish-khan/New Volume/Web_scraping/rgcrawler2/chromedriver'

chrome_options = Options()
#chrome_options.add_argument('--headless')

webdriver = webdriver.Chrome(
  executable_path=chrome_driver_path, options=chrome_options
)

# default login credential and search query
username = 'danishkhankd237@gmail.com'
password = 'danish3.16khan'
search_query = "Islamia college Peshawar"
results = []

with webdriver as driver:
    # Set timeout time 
    wait = WebDriverWait(driver, 5)

    # retrive url in headless browser
    driver.get(login_url)
    
    driver.find_element_by_id("input-login").send_keys(username)
    driver.find_element_by_id("input-password").send_keys(password)
    driver.find_element_by_class_name("nova-c-button__label").find_element(By.XPATH, "./..").click()
    time.sleep(5)

    driver.get(base_url)

    time.sleep(5)
    names = driver.find_elements_by_css_selector('.display-name')
    name_selector = '.nova-e-text--size-xl.nova-e-text--color-grey-900'
    selector = '.display-name'
    for i in range(len(names)):
         links = WebDriverWait(driver, 10).until(
         EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
         ) 
         links[i].click()
         name_e = WebDriverWait(driver, 10).until(
         EC.presence_of_element_located((By.CSS_SELECTOR, name_selector))
         )
         details = {
            'name' : name_e.text,
            'institution' : driver.find_element_by_css_selector('.nova-v-institution-item__title .nova-e-link--theme-bare').text,
            'department' : driver.find_element_by_css_selector('.nova-v-institution-item__info-section-list-item .nova-e-link--theme-bare').text, 
            'citations' : driver.find_element_by_css_selector('.application-box-layout__item--m:nth-child(2) .nova-e-text--size-xl').text,
            'recommendation' :   driver.find_element_by_css_selector('.application-box-layout__item--m:nth-child(3) .nova-e-text--size-xl').text,
            'reads' : driver.find_element_by_css_selector('.application-box-layout__item--m:nth-child(4) .nova-e-text--size-xl').text,
            'total research interest' :  driver.find_element_by_css_selector('.application-box-layout__item--m:nth-child(1) .nova-e-text--size-xl').text,
            'research_items' : driver.find_element_by_css_selector('.application-box-layout__item--xs:nth-child(1) .nova-e-text--color-inherit').text,
            'projects' : driver.find_element_by_css_selector('.application-box-layout__item--xs:nth-child(2) .nova-e-text--color-inherit').text,

            'questions' : driver.find_element_by_css_selector('.application-box-layout__item--xs:nth-child(3) .nova-e-text--size-xl').text,

            'answers' : driver.find_element_by_css_selector('.application-box-layout__item--xs:nth-child(4) .nova-e-text--size-xl').text,
        
            'scores' : driver.find_element_by_css_selector('.profile-header-details-meta-items .nova-e-list__item:nth-child(1)').text,
                     
            'followers' :  driver.find_element_by_css_selector('.nova-o-stack__item+ .nova-o-stack__item b').text,
                 
            'followings' : driver.find_element_by_css_selector('.nova-o-stack--show-divider .nova-o-stack__item:nth-child(1) .nova-o-stack__item b').text



                    }

         results.append(details)

    
         driver.back()
 
driver.close()

print(results)




