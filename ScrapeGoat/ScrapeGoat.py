import string
import os.path
import requests
from bs4 import BeautifulSoup
import json
import numpy as np

BASE_URL = 'https://en.wikipedia.org'
CATEGORY_TITLE = 'Category:19th-century_classical_composers'
ENTRIES_FILENAME = 'data/entries.json'
GRAPH_DATA_FILENAME = 'data/graph_data.json'

def getPageContent(pageUrl):
    page = requests.get(pageUrl)
    if (page.status_code != 200):
        return None
    else:
        return BeautifulSoup(page.content, features='html.parser')

def getSelection(content, selector):
    return content.select(selector)

def getLinks(links, useTitleAsKey=False):
    linksDict = {}
    soup = BeautifulSoup('', features='html.parser')
    for link in links: 
        soup.append(link)
    for a in soup.find_all('a'):
        if useTitleAsKey and a.has_attr('title') and a.has_attr('href'):
            linksDict[a['title']] = a['href']
        else:
            if a.string != None and a.has_attr('href') and a.string in string.ascii_letters:
                linksDict[a.string] = 'https:' + a['href']
    return linksDict

def getCategoryPages():
    pageUrl = BASE_URL + '/wiki/' + CATEGORY_TITLE
    selector = 'div.toc a'
    content = getPageContent(pageUrl)
    pages = {}
    if (content != None):
        pages = getLinks(getSelection(content,selector), useTitleAsKey=False)
    return pages
 
def getCategoryEntries(pageUrl):
    selector = 'div.mw-category-group a'
    content = getPageContent(pageUrl)
    entries = {}
    if (content != None):
        entries = getLinks(getSelection(content,selector), useTitleAsKey=True)
    return entries

def writeToFile(obj, filename):
    with open(filename, 'w') as fp:
        json.dump(obj, fp)

def readFromFile(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as fp:
            return json.load(fp)
    return None

def saveEntriesList(entries):
    writeToFile(entries, ENTRIES_FILENAME)

def getSavedEntriesList():
    return readFromFile(ENTRIES_FILENAME)

def createEntriesList():
    entries = {}
    for k, v in getCategoryPages().items():
        for k2, v2 in getCategoryEntries(v).items():
            entries[k2] = v2
    return entries

def getEntryPage(entryPageUrl):
    pageUrl = BASE_URL + entryPageUrl
    return getPageContent(pageUrl)

def getEntryPageLinks(content):
    selector = 'div.mw-body-content a'
    links = {}
    if content != None:
        links = getLinks(getSelection(content,selector), useTitleAsKey=True)
    return links

def getEntryPageLinksToOtherEntries(links, entriesList):
    return list(filter(lambda k: k in entriesList.keys(), links.keys()))

def saveEntryLinksList():
    writeToFile(createEntriesList(), ENTRY_LINKS_FILENAME)

def saveEntryLinksLists():
    sel = getSavedEntriesList()
    for letter in string.ascii_uppercase:
        writeToFile(createEntryLinksList(sel, letter), 'data/' + letter + '.json')

def createEntryLinksList(entriesList, letter):
    entryLinks = {}
    filtered = dict(filter(lambda item: item[0].startswith(letter), entriesList.items()))
    for k, v in filtered.items():
        entryLinks[k] = getEntryPageLinksToOtherEntries(getEntryPageLinks(getEntryPage(v)), entriesList)
    return entryLinks
 
def mergeGraphData():
    merged = {}
    for letter in string.ascii_uppercase:
        d = readFromFile('data/' + letter + '.json')
        merged.update(d)
    writeToFile(merged, GRAPH_DATA_FILENAME)


# start scraping and create entries list
# saveEntriesList()

# read from saved entries list and create entry links list
# saveEntryLinksLists()

#save merged file
# mergeGraphData()




