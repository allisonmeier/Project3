import urllib
import re
import pandas 
import pip._vendor.requests as requests
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
from html.parser import HTMLParser
 

site_url = 'https://transcripts.foreverdreaming.org/'
forum_url = 'https://transcripts.foreverdreaming.org/viewforum.php?f=463'

#dataFile = 'data.txt'
dataFile = 'data.txt'

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
        file.write('\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nSEASON: '+season+'\nEPISODE: '+episode+'\n\n')
        file.writelines(sum)
    
    file.close()

# to re-scrape from link: getText(getLinks(forum_url))
# DON'T DO THAT THOUGH, or else you'll have to un-censor everything all over again


# returns list of each speaker instance like '[Character1]' '[Character2]
def getSpeakerInstances(filename):  # 2146 without isUpper check; 1655 with it; 1008 after getting rid of randomSFX; 53 names total
    roughBracketContents = []

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



# Remove random sfx like '[cheering]' '[waves crashing]' and useless empty lines from txt file
def removeTrash(filename): # 3911 brackets before; 655 after
    file = open(filename, 'r', encoding='utf-8')
    lines = file.readlines()
    characters = getCharacterList(getSpeakerInstances(filename))

    lineNum = 0

    for line in lines:
        if '[' in line:
            bracketContents = line[line.index('[') + 1 : line.index(']')] # works
            if bracketContents not in characters:
                replacementLine = line.replace('[' + bracketContents + ']', '')
                lines[lineNum] = replacementLine 
        if '- ' in line:
            replacementLine = line.replace('- ', '')
            lines[lineNum] = replacementLine 
        if '♪' in line:
            replacementLine = line.replace('♪', '')
            lines[lineNum] = replacementLine 
        if line == '\n': #68371 before, 35628 after (wow)
            replacementLine = line.replace('\n', '')
            lines[lineNum] = replacementLine 

        lineNum+=1

    file = open(filename, 'w', encoding='utf-8')
    file.writelines(lines)

    file.close()


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


specific_links = getLinks(forum_url)

def combineLines(filename):
    file = open(filename, 'r', encoding='utf-8')
    lines = file.readlines()
    characters = getCharacterList(getSpeakerInstances(filename))

    lineNum = 0

    for line in lines:
        if ('[' or '~' or 'SEASON' or 'EPISODE') in line:
            return
        else:
            replacementLine = line.replace('\n', '')
            lines[lineNum] = replacementLine 
        lineNum+=1

    file = open(filename, 'w', encoding='utf-8')
    file.writelines(lines)

    file.close()


'''this takes the entire txt file, and turns every single speaking instance into a dict like this: 
    {'character': 'someone',
        'dialog': 'bla bla bla',
        'episode': 'episode number',
        'season': 'season number'
    }'''
def textToDicts(filename):
    # Open the file and read its contents
    with open(filename, 'r') as f:
        script = f.read()

    # Split the script into sections for each season/episode
    sections = re.findall(r'SEASON: (\d+)\nEPISODE: (\d+)\n([\s\S]*?)(?=SEASON: \d+|$)', script)

    results = []

    # Loop through each section and extract the character, dialogue, season, and episode
    for section in sections:
        season = (section[0])
        episode = (section[1])

        section = section[2].strip()

        # Extract the character and dialogue for each line
        lines = section.strip().split('\n')
        character = ''
        dialogue = ''

        lineNum = 0
        for line in lines:
            if '[' in line:
                # If this line contains a character's name, update the character variable
                character = line[line.index('[') + 1 : line.index(']')]
                
                # Add the rest of the line (the dialogue) to the dialogue variable
                dialogue += line[line.index(']')+1: ].strip() + ' '
            else:
                # If this line doesn't contain a character's name, add it to the dialogue variable
                dialogue += line.strip() + ' '

            # If we've reached the end of a character's dialogue, add it to the results list
            if lineNum == len(lines) - 1 or '[' in lines[lineNum+1]:
                results.append({
                    'character': character,
                    'dialogue': dialogue.strip(),
                    'season': season,
                    'episode': episode
                })
                # Reset the character and dialogue variables
                character = ''
                dialogue = ''

            lineNum += 1

    return results

def dataToCSV():
    allData = pandas.DataFrame(textToDicts('data.txt'))
    allData.to_csv('./data.csv', index=False)

def getStopwords(arrayOfDicts, newFile):
    everySingleWord = ''
    for dict in arrayOfDicts:
        value = dict['dialogue']
        value = "".join(char.lower() for char in value if char.isalpha() or char.isspace())
        everySingleWord += str(value.split(' '))

    wordsList = everySingleWord.split()
    stopwords = []

    [stopwords.append(word) for word in wordsList if word not in stopwords]


    file = open(newFile, "w")
    file = open(newFile, "a", encoding='utf-8')

    for word in stopwords:
        file.write(word)
    
    file.close()


getStopwords(textToDicts('data.txt'), 'stopwords.txt')