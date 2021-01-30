# Web_scraping_Social_Academic_Sites
Scraping user profiles from social academic networking sites 
I want to scrape the users profile information from a social academic networking site 
https://www.researchgate.net. I first search for an institution(i.e university, college, institution etc)
the go for departments in the institution. after going to department i finaly select the department researchers
or members than scraps all the profiles information like name, institution name, citations, profiles reads, questions
asked, answers given etc.

The institute members page is here:
'https://www.researchgate.net/institution/Islamia_College_Peshawar/department/Department_of_Computer_Science/members'
from this page scraping the data.
It cannot be done with scrapy or beautifulsoup because it this website contains javascript.
And second is it requires login to see any data or scrped any data.
So scrapy here fails.
The final solution is using selenium.

At last i want to store the data in a database. Here i using mysql database but you can use any other database. 


Anyone who want to contribute in this project are welcomed.


