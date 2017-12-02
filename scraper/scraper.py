import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def padZero(num):
    if len(num) == 1:
        return "0" + num
    return num

def monthToNum(shortMonth):
    
    dates = {
        'Jan' : "01",
        'Feb' : "02",
        'Mar' : "03",
        'Apr' : "04",
        'May' : "05",
        'Jun' : "06",
        'Jul' : "07",
        'Aug' : "08",
        'Sep' : "09",
        'Oct' : "10",
        'Nov' : "11",
        'Dec' : "12"
    }

    if shortMonth not in dates:
        return ""

    return dates[shortMonth]

driver = webdriver.Chrome('./scraper/chromedriver_win32/chromedriver.exe')
timeout = 5

searchQuery = "bitcoin"
outputFile = "news_data2.txt"

currentUrl = "https://www.google.ca/search?q=" + searchQuery + "&biw=1200&bih=567&source=lnt&tbs=cdr%3A1%2Ccd_min%3A2009%2Ccd_max%3A2015&tbm=nws";
f1=open(outputFile, 'w+')

count = 0;

while (True):
    page = requests.get(currentUrl)
    soup = BeautifulSoup(page.content, 'html.parser')

    driver.get(currentUrl)#put here the adress of your page
    
    wrappers = driver.find_elements_by_xpath('//div[@class="g"]')
    for wrapper in wrappers:
        title = wrapper.find_element_by_xpath(".//a[@class='l _PMs']").text.encode('utf-8');
        date = wrapper.find_element_by_xpath(".//span[@class='f nsa _QHs']").text.encode('utf-8');
        date = date.replace(",", "").replace(date[:3], monthToNum(date[:3]))
        date = date.split(" ")
        date[1] = padZero(date[1])
        print >> f1, date[2] + "" + date[0] + "" +  date[1] + "," + title.replace(",", "").replace(" ...", "")

    nextButton = driver.find_element_by_id('pnnext')
    nextButton.click();

    try:
        element_present = EC.presence_of_element_located((By.ID, 'pnnext'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print "Timed out waiting for page to load"

    currentUrl = driver.current_url
#count = count + 1

driver.close()

