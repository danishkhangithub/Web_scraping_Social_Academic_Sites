from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException 
import time
import sys
import pandas as pd
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="your username",
  password="your password",
  db='reseachgate_profiles'
)

cur = mydb.cursor()


#create table
cur.execute("""DROP TABLE IF EXISTS Data2""")

cur.execute(''' CREATE TABLE IF NOT EXISTS Data2
               (Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                Name varchar(255),
                Institution VARCHAR(255),
                Department varchar(255),
                Citations INTEGER,
                Recommendation INTEGER, 
                Total_Reads INTEGER, 
                Total_research_interest DECIMAL(7,1), 
                Research_items INTEGER,
                Projects INTEGER, 
                Questions  INTEGER,
                Answers INTEGER, 
                Scores  DECIMAL(7,1),
                Followers INTEGER,
                Followings INTEGER
               )''')



login_url = 'https://www.researchgate.net/login'
base_url = "https://www.researchgate.net/institution/COMSATS-University-Islamabad/department/Department-of-Computer-Science/members"
chrome_driver_path = '/home/danish-khan/scrapers/researchgate/chromedriver'

chrome_options = Options()
#chrome_options.add_argument('--headless')

webdriver = webdriver.Chrome(
  executable_path=chrome_driver_path, options=chrome_options
)

# default login credential and search query
username = 'your researchgate username'
password ='your password'

results = []
total_profiles = []

with webdriver as driver:
    # Set timeout time 
    wait = WebDriverWait(driver, 5)

    # retrive url in headless browser
    driver.get(login_url)
    
    driver.find_element_by_id("input-login").send_keys(username)
    driver.find_element_by_id("input-password").send_keys(password)
    driver.find_element_by_class_name("nova-c-button__label").find_element(By.XPATH, "./..").click()
    time.sleep(2)

    driver.get(base_url)

    time.sleep(3)
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #names = driver.find_elements_by_css_selector('.display-name')
    #name = driver.find_elements_by_xpath('//ul[@class="list people-list-m"]/li//a[@class="display-name"]')
    last_height = driver.execute_script('return document.body.scrollHeight')
    print('height:',last_height)
    time.sleep(5)
   
    while True:
       # Scroll down to bottom
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
      time.sleep(2)
      
      #driver.execute_script("window.scrollTo(1, 5000);")
      new_height = driver.execute_script("return document.body.scrollHeight")
      print('new height:' +str(new_height))
      if new_height == last_height:
          break
      last_height = new_height    
    total_profiles.append(last_height)
    links = '//ul[@class="list people-list-m"]/li//a[@class="display-name"]'
    name = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, links))
              )
    print(len(name))
    lenname = len(name)
    total_profiles = total_profiles[0]
    print('total  profiles:', total_profiles)
    #selector = '.display-name'
    selector = '//ul[@class="list people-list-m"]/li//a[@class="display-name"]'
   
    for i in range(0,lenname-1):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        
            time.sleep(5)
            links = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, selector))
              )
                     
            links[i].click()

            details = {
                'Name' : driver.find_element_by_css_selector('.nova-e-text--size-xl.nova-e-text--color-grey-900').text,
                'Institution' : '',
                'Department' : driver.find_element_by_css_selector('.nova-v-institution-item__info-section-list-item .nova-e-link--theme-bare').text,
                'Citations' : '',
                'Recommendation' : '',
                'Total_Reads' : '',
                'Total_research_interest' : '',
                'Research_items' : '',
                'Projects' : '',
                'Questions' : '',
                'Answers' : '',
                'Scores' : '',
                'Followings' : '',
                'Followers' : ''
        
             }
    
    
            try:
              Institution = driver.find_element_by_css_selector('.nova-v-institution-item__title .nova-e-link--theme-bare').text
            except:
              Institution = 'N/A'
            
            try:   
              Citations = driver.find_element_by_css_selector('.application-box-layout__item--m:nth-child(2) .nova-e-text--size-xl').text
              Citations = int(Citations.replace(",", ""))
            except:
              Citations = 0 
                 
            try:     
              Recommendation =   driver.find_element_by_css_selector('.application-box-layout__item--m:nth-child(3) .nova-e-text--size-xl').text
              Recommendation = int(Recommendation.replace(' ', ''))
            except:
              Recommendation = 0 
            
            try:  
              Total_Reads = driver.find_element_by_css_selector('.application-box-layout__item--m:nth-child(4) .nova-e-text--size-xl').text                      
              Total_Reads = int(Total_Reads.replace(",", ""))
            except:
              Total_Reads = 0 
            
            try:
              Total_research_interest =   driver.find_element_by_css_selector('.application-box-layout__item--m:nth-child(1) .nova-e-text--size-xl').text           
              Total_research_interest = float(Total_research_interest)
            except:
              Total_research_interest = 0.0
            
            try:
              Research_items = driver.find_element_by_css_selector('.application-box-layout__item--xs:nth-child(1) .nova-e-text--color-inherit').text
              Research_items = int(Research_items)
            except:
              Research_items = 0
            
            try:
              Projects = driver.find_element_by_css_selector('.application-box-layout__item--xs:nth-child(2) .nova-e-text--color-inherit').text
              Projects = int(Projects)
            except:
              Projects = 0

            try:   
              Questions = driver.find_element_by_css_selector('.application-box-layout__item--xs:nth-child(3) .nova-e-text--size-xl').text
              Questions = int(Questions)
            except:
              Questions = 0
            
            try:
              Answers = driver.find_element_by_css_selector('.application-box-layout__item--xs:nth-child(4) .nova-e-text--size-xl').text
              Answers = int(Answers)
            except:
              Answers = 0
            
            
            try:
                Scores = driver.find_element_by_css_selector('.profile-header-details-meta-items .nova-e-list__item:nth-child(1)').text
                
                Scores = float(Scores)
            except: 
                Scores = 0
            
            try:                             
              Followings = driver.find_element_by_xpath(xpath = "//*[contains(text(), 'Following')]").text.strip('Following').strip('( )')
              
              Followings = int(Followings)
            except:
              Followings = 0
            
            try:                             
              Followers = driver.find_element_by_xpath(xpath = "//*[contains(text(), 'Followers')]").text.strip('Followers').strip('( )')

              Followers = int(Followers)
            except:
              Followers = 0  
            
            
            
            details['Institution'] = Institution 
            details['Citations'] =  Citations
            details['Recommendation'] =  Recommendation
            details['Total_Reads'] = Total_Reads 
            details['Total_research_interest'] = Total_research_interest 
            details['Research_items'] =  Research_items
            details['Projects'] = Projects 
            details['Questions'] = Questions 
            details['Answers'] =  Answers 
            details['Scores'] =  Scores
            details['Followings'] = Followings
            details['Followers'] = Followers
             
            results.append(details)
            driver.back()

            time.sleep(5)
            

profile_details = pd.DataFrame(results)
print(profile_details)

for row in profile_details.itertuples():
            
    cur.execute('''INSERT INTO Data2
                (Name,
                Institution,
                Department,
                Citations,
                Recommendation,
                Total_Reads,
                Total_research_interest,
                Research_items , Projects,
                Questions,
                Answers,
                Scores,
                Followers, 
                Followings)
                VALUES
                ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s", "%s" )''',
                (row.Name,
                row.Institution,
                row.Department,
                row.Citations,
                row.Recommendation,
                row.Total_Reads,
                row.Total_research_interest,
                row.Research_items,
                row.Projects,
                row.Questions,
                row.Answers,
                row.Scores,
                row.Followers,
                row.Followings ) )
                  
            
mydb.commit()
        
print('complete.')
  

mydb.close()
time.sleep(5)

driver.close()
