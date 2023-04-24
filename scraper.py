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

combineLines('data.txt')


def firstAttempt(filename):
    file = open(filename, 'r', encoding='utf-8')
    lines = file.readlines()
    fileContents = file.read()
    characters = getCharacterList(getSpeakerInstances(filename))

    splitHere = '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

    #splitFile = [str(file).splitlines(line) for line in lines if line == '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~' ]
    #splitFile = fileContents.split(splitHere)

    #print(fileContents)
    #print(splitFile)
    #print(len(splitFile))

    global dataDict
    dataDict = {}

    # split each episode apart
    # get its season and episode
    # look through at each speaker instance
    # from there split text from tail of speaker inst to just before next

    dialog = ''
    for line in lines:
        if '[' in line:
            dialog = line[line.index(']')+1: ]
        elif 'SEASON:' not in line and 'EPISODE:' not in line and '[' not in line and '~' not in line:
            dialog += ' ' + str(line)


    for i in file:
        lineNum = 0
        dialog = ''
        for line in lines:
            if 'SEASON:' in line:
                season = line[7:10] # works
                #print(season)
                dataDict['season'] = season

            if 'EPISODE:' in line:
                episode = line[8:11] # works
                #print(episode)
                dataDict['episode'] = episode


            if '[' in line:
                speaker = line[line.index('[') + 1 : line.index(']')]
                #print('SPEAKING: ', speaker, '\n')
                dialog += line[line.index(']')+1: ]
            if '~' in line:
                dialog = dialog
            elif 'SEASON:' not in line and 'EPISODE:' not in line and  '[' not in line and '~' not in line:
                dialog += ' ' + str(line)
            
            #elif 'SEASON:' not in line and 'EPISODE:' not in line and  '[' not in line and '~' not in line:
                #dialog += str(line)
            #else:
                #print(dialog)
            

            lineNum+=1



def anotherAttempt(filename):
    # Open the file and read its contents
    with open(filename, 'r') as f:
        script = f.read()

    # Split the script into sections for each season/episode
    sections = re.split(r'SEASON: \d+\nEPISODE: \d+\n', script)[1:]

    # Loop through each section and extract the character, dialogue, season, and episode
    for section in sections:
        # Extract the season and episode
        #season = re.findall(r'SEASON: ', section)
        #episode = re.find(r'EPISODE: (\d+)\n', section)


        results = []

        # Extract the character and dialogue for each line
        lines = section.strip().split('\n')
        episode = ''
        season = ''
        character = ''
        dialogue = ''
        for line in lines:
            if 'SEASON:' in line:
                season = line[7:10] # works
                print(season)

            if 'EPISODE:' in line:
                episode = line[8:11] # works
                #print(episode)

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
            if line.endswith('.') or line.endswith('!') or line.endswith('?'):
                results.append({
                    'character': character,
                    'dialogue': dialogue.strip(),
                    'season': season,
                    'episode': episode
                })
                # Reset the character and dialogue variables
                character = ''
                dialogue = ''
        
            # Print the results
    print(len(results))
    print(results[0])


            #print(results[32:34])

            #dataDict = {}

            #dataDict[character] = character
            #dataDict[dialogue] = dialogue.strip()
            #dataDict[season] = season
            #dataDict[episode] = episode


anotherAttempt('data.txt')









#everythingToCSV('data.txt')
        



allDialog = pandas.DataFrame()

print(allDialog)

