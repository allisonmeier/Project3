import urllib
import pandas 
import pip._vendor.requests as requests
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
from html.parser import HTMLParser
 

site_url = 'https://transcripts.foreverdreaming.org/'
forum_url = 'https://transcripts.foreverdreaming.org/viewforum.php?f=463'

#dataFile = 'data.txt'
dataFile = 'extraFile.txt'

# returns array of specific links to all 46 episode transcripts
def getLinks(url):
    forum = requests.get(url)
    soup = BeautifulSoup(forum.content, 'html.parser')
    divs = soup.find_all("a", {"class":"topictitle"})
    del divs[0] # snip off the unnecessary extra forum link

    specific_links = []

    for div in divs:
        link = str(div['href'])[2:]
        specific_links.append(site_url+link)

    return specific_links

# obtain the actual *stuff* from each link to put into the file
def getText(links):    
    file = open(dataFile, "w")

    for link in links:
        data = BeautifulSoup(requests.get(link).content, 'html.parser').find("div", {"class":"content"})

        season = BeautifulSoup(requests.get(link).content, 'html.parser').find("h3", {"class":"first"})
        season = (season.get_text())[1:3]
        episode = BeautifulSoup(requests.get(link).content, 'html.parser').find("h3", {"class":"first"})
        episode = (episode.get_text())[4:6]

        sum = data.get_text()
        file = open(dataFile, "a", encoding='utf-8')
        file.write('\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nSEASON: '+season+'\nEPISODE: '+episode+'\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n')
        file.writelines(sum)
    
    file.close()

# to re-scrape from link: getText(getLinks(forum_url))
# DON'T DO THAT THOUGH, or else you'll have to un-censor everything all over again




# TODO: Most likely need to get all my text into a csv somehow 
# I prob want it to be like: character, line, season, episode

allDialog = pandas.DataFrame()

