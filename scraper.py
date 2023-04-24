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



# TODO: Most likely need to get all my text into a csv somehow 
# I prob want it to be like: character, line, season, episode

csvFile = 'data.csv'

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



def anotherAttempt(filename):
    # Open the file and read its contents
    with open(filename, 'r') as f:
        script = f.read()

    # Split the script into sections for each season/episode
    #sections = re.split(r'SEASON:', script)[0:]
    #print(len(sections))
    sections = re.findall(r'SEASON: (\d+)\nEPISODE: (\d+)\n([\s\S]*?)(?=SEASON: \d+|$)', script)
    print(len(sections))
    #print(sections[0])

    print(type(sections[0]))

    print((sections[0])[0])

    results = []

    # Loop through each section and extract the character, dialogue, season, and episode
    sectionNum = 0
    for section in sections:
        season = (section[0])
        episode = (section[1])

        section = section[2].strip()

        # Extract the character and dialogue for each line
        lines = section.strip().split('\n')
        character = ''
        dialogue = ''
        for line in lines:
            #match = re.match(r'\[(.*?)\]', line)
            if '[' in line:
                # If this line contains a character's name, update the character variable
                character = line[line.index('[') + 1 : line.index(']')]
                
                # Add the rest of the line (the dialogue) to the dialogue variable
                dialogue += line[line.index(']')+1: ].strip() + ' '
            else:
                # If this line doesn't contain a character's name, add it to the dialogue variable
                dialogue += line.strip() + ' '

            # If we've reached the end of a character's dialogue, add it to the results list
            if line == len(lines) - 1 or re.match(r'\[(.*?)\]', line):
                results.append({
                    'character': character,
                    'dialogue': dialogue.strip(),
                    'season': season,
                    'episode': episode
                })
                # Reset the character and dialogue variables
                character = ''
                dialogue = ''
        

        sectionNum+=1

            # Print the results
    print(len(results))
    print(results[23])
    print(results[24])
    #print(results[len(results)-1])

anotherAttempt('data.txt')






# deal with next:

allDialog = pandas.DataFrame()

#print(allDialog)

