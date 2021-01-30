from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import mysql.connector

#connection to database
mydb = mysql.connector.connect(
  host="localhost",
  user="danish-khan",
  password="12345",
  db='reseachgate_profiles'
)

cur = mydb.cursor()


#create table
cur.execute("""DROP TABLE IF EXISTS Data""")

cur.execute(''' CREATE TABLE IF NOT EXISTS Data
               (Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                Name varchar(20),
                Institution VARCHAR(255),
                Department varchar(255),
                Citations INTEGER,
                Recommendation BIGINT(20), 
                Total_Reads Real, 
                Total_research_interest INTEGER, 
                Research_items INTEGER,
                Projects INTEGER, 
                Questions  INTEGER,
                Answers INTEGER, 
                Scores INTEGER,
                Followers INTEGER,
                Followings INTEGER
               )''')



login_url = 'https://www.researchgate.net/login'
base_url = "https://www.researchgate.net/institution/Islamia_College_Peshawar/department/Department_of_Computer_Science/members"
chrome_driver_path = '/home/danish-khan/scrapers/researchgate/chromedriver'

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

    time.sleep(10)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    names = driver.find_elements_by_css_selector('.display-name')
    print(len(names))
    name_selector = '.nova-e-text--size-xl.nova-e-text--color-grey-900'
    selector = '.display-name'
    
    for i in range(0,len(names)):
         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
         try:
             links = WebDriverWait(driver, 50).until(
             EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
              )
                    
             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
             links[i].click()
             name_e = WebDriverWait(driver, 20).until(
             EC.presence_of_element_located((By.CSS_SELECTOR, name_selector))
             )
             
             Name = name_e.text
             Institution = driver.find_element_by_css_selector('.nova-v-institution-item__title .nova-e-link--theme-bare').text
             Department = driver.find_element_by_css_selector('.nova-v-institution-item__info-section-list-item .nova-e-link--theme-bare').text 
             Citations = driver.find_element_by_css_selector('.application-box-layout__item--m:nth-child(2) .nova-e-text--size-xl').text
             
             Recommendation =   driver.find_element_by_css_selector('.application-box-layout__item--m:nth-child(3) .nova-e-text--size-xl').text.replace(',',''),
             Total_Reads = driver.find_element_by_css_selector('.application-box-layout__item--m:nth-child(4) .nova-e-text--size-xl').text,         
                
             Total_research_interest =  driver.find_element_by_css_selector('.application-box-layout__item--m:nth-child(1) .nova-e-text--size-xl').text,
             Research_items = driver.find_element_by_css_selector('.application-box-layout__item--xs:nth-child(1) .nova-e-text--color-inherit').text,
             Projects = driver.find_element_by_css_selector('.application-box-layout__item--xs:nth-child(2) .nova-e-text--color-inherit').text,

             Questions = driver.find_element_by_css_selector('.application-box-layout__item--xs:nth-child(3) .nova-e-text--size-xl').text,
             Answers = driver.find_element_by_css_selector('.application-box-layout__item--xs:nth-child(4) .nova-e-text--size-xl').text,
            
             Scores = driver.find_element_by_css_selector('.profile-header-details-meta-items .nova-e-list__item:nth-child(1)').text,
                         
             Followers = driver.find_element_by_xpath('//div[@class="nova-e-text nova-e-text--size-m nova-e-text--family-sans-serif nova-e-text--spacing-none nova-e-text--color-inherit"]/b').text[11:13]
                     
             Followings = driver.find_element_by_xpath('//div[@class="nova-o-stack nova-o-stack--gutter-xxl nova-o-stack--spacing-xxs nova-o-stack--show-divider"]/div[2]/div/div/div/div/div/b').text[11:13]


             time.sleep(5)
         
         except Exception as e:
            print('Time out error')   

time.sleep(10)
#insert the scraped data into database.
cur.execute('INSERT INTO DATA(Name,Institution,Department,Citations,Recommendation , Total_Reads , Total_research_interest , Research_items , Projects, Questions , Answers , Scores , Followers, Followings) VALUES("%s","%s","%s","%s")' % (Name,Institution,Department,citations,Recommendation , Total_Reads , Total_research_interest , Research_items , Projects, Questions , Answers , Scores , Followers, Followings ) )
#driver.close()
mydb.commit()
print('complete.')


mydb.close()
time.sleep(10)

driver.close()








