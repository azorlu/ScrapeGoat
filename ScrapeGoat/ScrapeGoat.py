import requests
from bs4 import BeautifulSoup
import json
import numpy as np

# CONSTANTS
BASE_URL = "https://en.wikipedia.org"
CATEGORY_TITLE = "Category:19th-century_classical_composers"

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

def writeToFile(obj, filename):
    with open(filename, 'w') as fp:
        json.dump(obj, fp)

def getCategoryPages():
    pageUrl = BASE_URL + '/wiki/' + CATEGORY_TITLE
    selector = 'div.mw-category-group a'
    content = getPageContent(pageUrl)
    print(content)
 

def createList():
    pageUrl = BASE_URL + '/wiki/' + CATEGORY_TITLE
    selector = 'div.mw-category-group a'
    content = getPageContent(pageUrl)
    filename = 'data/composers.json'
        
    if (content != None):
        links = getLinks(getSelection(content,selector))
        writeToFile(links, filename)

# action
# createList()


