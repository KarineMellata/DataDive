import requests
from bs4 import BeautifulSoup

searchQuery = "bitcoin"
outputFile = "textdata2.txt"

currentUrl = "https://www.google.ca/search?q=bitcoin&hl=en&source=lnms&tbm=nws&sa=X&ved=0ahUKEwja3Nm27sjXAhXrhFQKHQGnArEQ_AUICigB&biw=1280&bih=605";
f1=open(outputFile, 'w+')

page = requests.get("https://www.google.ca/search?q=bitcoin&biw=1280&bih=605&source=lnt&tbs=cdr%3A1%2Ccd_min%3A2013%2Ccd_max%3A2014&tbm=nws")
soup = BeautifulSoup(page.content, 'html.parser')

print >> f1, soup

# for article in soup.find_all("b"):
# 	if article.parent.name == 'a':
# 		print >> f1, article.parent.getText().encode('utf-8');


