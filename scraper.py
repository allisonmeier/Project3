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


# Remove sfx like '[cheering]' '[waves crashing]' and returns list of each speaker instance like '[Character1]' '[Character2]
def removeSFX(filename):  # 2146 without isUpper check; 1655 with it; 1008 after getting rid of randomSFX; 53 names total
    roughBracketContents = []
    randomSFX = ['screaming', 'exhales', 'panting', 'inaudible', 'coughing', 'kisses', 'chuckles', 'groans', 'all', 'exclaims', 
                 'yelling', 'weakly', 'softly', 'gasps', 'crying', 'praying', 'thud', 'whimpers', 'whimpering', 'laughing', 
                 'choking', 'thudding', 'grunting', 'grunts', 'scoffs', 'sighs', 'inhales', 'musician', 'laughs', 'man', 'screams', 
                 'caws', 'clatters', 'soldier', 'snoring', 'sniffles', 'sobbing', 'clucking', 'coughs', 'retching', 'stuttering', 
                 'sniffs', 'stutters', 'thuds', 'whistles', 'shushes', 'groaning', 'straining', 'nun', 'sobs', 'gasping', 
                 'shuddering', 'urinating', 'sable', 'echoing', 'vomits', 'boy', 'shakily', 'monk', 'dane', 'guard', 'whispers', 
                 'woman', 'driver', 'stammers', 'yells', 'snickers', 'snorts', 'mercian', 'stammering', 'cheering', 'laughter', 
                 'clattering', 'footsteps', 'shouting', 'silence', 'thunk!', 'murmuring', 'chuckling', 'cheers', 'whinnying', 
                 'snarling', 'moaning', 'sniffling', 'giggles', 'spitting', 'yawns', 'knocking', 'sigh', 'chuckle', 'scoff', 'clucks', 
                 'gasp', 'clang', 'sniffle', 'thump', 'spits', 'wheezing', 'hisses', 'shivering', 'slap', 'whistling', 'moans', 'moan', 'cries']

    file = open(filename, 'r')
    for line in file:
        if '[' in line:
            bracketContents = line[line.index('[') + 1 : line.index(']')]
            if (' ' not in bracketContents and bracketContents[0].isupper()):
                bracketContents = bracketContents.lower()
                roughBracketContents.append(bracketContents)

    speakerInstances = []
    [speakerInstances.append(x.capitalize()) for x in roughBracketContents if x not in randomSFX]

    file.close()

    return speakerInstances


def getCharacterList(speakerInstances):
    characterNames = []
    [characterNames.append(x) for x in speakerInstances if x not in characterNames]

    return characterNames # should be 53 


def getSpeakingCount(speakerInstances):

    nameCount = {}
    for name in speakerInstances:
        if name in nameCount:
            nameCount[name] += 1
        else: 
            nameCount[name] = 1

    for key, value in nameCount.items():
        print(f"{key}: {value}")

    return nameCount


# TODO: Most likely need to get all my text into a csv somehow 
# I prob want it to be like: character, line, season, episode

allDialog = pandas.DataFrame()

