import urllib
import pip._vendor.requests as requests
from bs4 import BeautifulSoup
 
# here we have to pass url and path
# (where you want to save your text file)
#urllib.request.urlretrieve("https://www.geeksforgeeks.org/grep-command-in-unixlinux/?ref=leftbar-rightbar",
 #                          "/home/gpt/PycharmProjects/pythonProject1/test/text_file.txt")


allLinks = []

site_url = 'https://transcripts.foreverdreaming.org/'
forum_url = 'https://transcripts.foreverdreaming.org/viewforum.php?f=463'

# last kingdom transcripts:
#https://transcripts.foreverdreaming.org/viewforum.php?f=463
#https://tvshowtranscripts.ourboard.org/viewforum.php?f=463


# create all the files we need. i do not want to type all of this!!
def createFiles():
    global allFiles
    allFiles = []
    for i in range(1,47):
        allFiles.append(open('e' + str(i) + '.txt', 'w'))


# obtain the actual *stuff* to put into the files
def getText(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    divs = soup.find_all("a", {"class":"topictitle"})
    del divs[0] # snip off the unnecessary extra forum link

    specific_links = []
    for div in divs:
        link = str(div['href'])[2:]
        specific_links.append(link)
        text = str(div)
    # episodeIndex = text.find('>')+1
    # as of here, each episode page can be found at site_url + specific_links[i]


# throw all the stuff in there
def fillFiles():
    i = 1

    for element in allFiles:
        file = open(element, "r") # 'r' = read mode 
        content = file.read()

        page = urllib.request.urlretrieve()

        soup = BeautifulSoup(page.content, 'html.parser')
    
        f = open(allLinks[i], "w")

        i+=1

        print(i)
    
    # traverse article guts from soup
    for data in soup.find_all("article"):
        sum = data.get_text()
        f.writelines(sum)
    
    f.close()


getText(forum_url)


