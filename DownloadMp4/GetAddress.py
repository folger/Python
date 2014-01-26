# from urllib.request import urlopen
# from bs4 import BeautifulSoup

# response = urlopen('http://tv.sohuxia.com/20130318/n369301834.shtml')
# soup = BeautifulSoup(response)

# print(soup.prettify())

from selenium import webdriver

driver = webdriver.Chrome(r'c:\dropbox\Windows\chromedriver.exe')
driver.get('http://tv.sohuxia.com/20130415/n372763492.shtml')
with open("my.html", "wt", encoding='utf-8') as f:
    f.write(driver.page_source)

driver.get('http://tv.sohuxia.com/20130415/n372763498.shtml')
with open("my2.html", "wt", encoding='utf-8') as f:
    f.write(driver.page_source)

