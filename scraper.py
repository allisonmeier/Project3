import urllib
import pandas
import pip._vendor.requests as requests
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
from html.parser import HTMLParser
 
# here we have to pass url and path
# (where you want to save your text file)
#urllib.request.urlretrieve("https://www.geeksforgeeks.org/grep-command-in-unixlinux/?ref=leftbar-rightbar",
 #                          "/home/gpt/PycharmProjects/pythonProject1/test/text_file.txt")

site_url = 'https://transcripts.foreverdreaming.org/'
forum_url = 'https://transcripts.foreverdreaming.org/viewforum.php?f=463'

# last kingdom transcripts:
#https://transcripts.foreverdreaming.org/viewforum.php?f=463
#https://tvshowtranscripts.ourboard.org/viewforum.php?f=463


dataFile = 'dataFile.txt'

# create all the files we need. i do not want to type all of this!!
def createFiles():
    global allFiles
    allFiles = []
    for i in range(1,47):
        allFiles.append(open('e' + str(i) + '.txt', 'w'))


# obtain the actual *stuff* to put into the files
def getText(url):
    forum = requests.get(url)
    soup = BeautifulSoup(forum.content, 'html.parser')
    divs = soup.find_all("a", {"class":"topictitle"})
    del divs[0] # snip off the unnecessary extra forum link

    specific_links = []

    for div in divs:
        text = str(div)
        link = str(div['href'])[2:]
        specific_links.append(site_url+link)
        ti = text.find('>')+1
        global episode
        episode = text[ti+3:ti+5]
        global season
        season = text[ti:ti+2]
    
    file = open(dataFile, "w")

    for link in specific_links:
        page = urllib.request.urlretrieve(link)
        #print(page)
        #newSoup = BeautifulSoup(link.content, 'html.parser')
        
        data = BeautifulSoup(requests.get(link).content, 'html.parser').find("div", {"class":"content"})

        #print(data)

        #f = open(link, "r")

        sum = data.get_text()
        file = open(dataFile, "a", encoding='utf-8')
        file.write('\n\n************************************************************************************\nSEASON: '+season+'\nEPISODE: '+episode+'\n************************************************************************************\n\n')
        file.writelines(sum)
    
    file.close()

    #data = data.split("\n") # then split it into lines

    #for line in data:
        #print(line)

    #print(soup.get_text('\n'))



getText(forum_url)


