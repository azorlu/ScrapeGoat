import requests
from bs4 import BeautifulSoup
import numpy as np

def getPageContent(pageUrl):
    page = requests.get(pageUrl)
    if (page.status_code != 200):
        return None
    else:
        return BeautifulSoup(page.content, features='html.parser')

def getSelection(content, selector):
    return content.select(selector)

def getLinks(links):
    linksDict = {}
    soup = BeautifulSoup('', features='html.parser')
    for link in links: 
        soup.append(link)
    for a in soup.find_all('a'):
        linksDict[a['title']] = a['href']
    return linksDict

    
 
# 
pageUrl = 'https://en.wikipedia.org/wiki/Category:19th-century_classical_composers'
selector = 'div.mw-category-group a'
content = getPageContent(pageUrl)

if (content != None):
    print(getLinks(getSelection(content,selector)))




