import requests
import re
import datetime
import sys
import os
import subprocess
import time
import webbrowser

## SETTING UP TXT AND HTML FILES
locationOfYourScript = r'{}'.format(os.path.dirname(os.path.realpath(__file__)))

os.chdir(locationOfYourScript)
pathToTXTfile = r'{}\today.txt'.format(os.getcwd())
pathToHTMLfile = r'{}\today.html'.format(os.getcwd())
pathToArchiveFile = r'{}\archive.txt'.format(os.getcwd())

# Getting today's date
today = datetime.date.today().strftime("%A %d %B %Y")

# Overwriting existing files containing today's words
with open(pathToTXTfile, 'w') as fileHandler:
                fileHandler.write("\t\t********************* {} *********************".format(today))
                fileHandler.write("\nWORDS OF THE DAY\n")

with open(pathToHTMLfile, 'w') as fileHandler:
                fileHandler.write("<!DOCTYPE html>\n<html>\n<head><title>Lexicon {}</title>\n".format(today))
                fileHandler.write("<style>body {font-family: Calibri; font-size: 18px;} #content {width: 70%; margin-left: 15%; border: 3px solid black; padding: 15px; margin-top: 5%;}</style>\n")
                fileHandler.write("</head>\n\n<body>\n\n<div id = \"content\">\n")
                fileHandler.write("<center><h2>Lexicon | {}</h2></center>\n".format(today))
                fileHandler.write("<center><h3>WORDS OF THE DAY</h3></center>\n")
                fileHandler.write("<ul>\n")



## SCRAPING AND POPULATING TXT & HTML FILES
# 1 DICTIONARY.COM
print("Fetching word of the day from Dictionary.com...")

url = 'http://dictionary.reference.com/wordoftheday/'
source = requests.get(url)

matchedObject = re.search(r'Definitions for <strong>(.+?)</strong>[\S\s\n]*?<li class="first"><span>(.+?)</span></li>', source.text)

try:
    word = matchedObject.group(1)
    meaning = matchedObject.group(2)

    cleanedWord = re.sub('<.*?>', '', word)
    cleanedWord = re.sub('&#\d{2,4};', '', cleanedWord)
    cleanedWord = re.sub('&nbsp;', ' ', cleanedWord)

    cleanedMeaning = re.sub('<.*?>', '', meaning)
    cleanedMeaning = re.sub('&#\d{2,4};', '', cleanedMeaning)
    cleanedMeaning = re.sub('&nbsp;', ' ', cleanedMeaning)

    entryForTextFile = "{}: {}".format(cleanedWord, cleanedMeaning)
    entryForHTMLFile = "<strong>{}</strong>: {}".format(cleanedWord, cleanedMeaning)

    with open(pathToTXTfile, 'a') as fileHandler:
                fileHandler.write("- {}\n".format(entryForTextFile))

    with open(pathToHTMLfile, 'a') as fileHandler:
                fileHandler.write("<li>{}</li>\n".format(entryForHTMLFile))

except:
    print("Error in retrieving information from Dictionary.com [http://dictionary.reference.com/wordoftheday/].", file = sys.stderr)

# 2 LEARNER'S DICTIONARY
print("Fetching word of the day from Learner's Dictionary...")

url = 'http://www.learnersdictionary.com/word-of-the-day'
source = requests.get(url)

matchedObject = re.search(r'Word of the Day:\s(.*?)\s-[\S\s\n]*?<div class = "midbt"><p>(.*?)</p>[\S\s\n]*?<li class = "vi"><p>(.*?)</p>', source.text)

try:
    word = matchedObject.group(1)
    meaning = matchedObject.group(2)
    usage = matchedObject.group(3)

    cleanedWord = re.sub('<.*?>', '', word)
    cleanedWord = re.sub('&#\d{2,4};', '', cleanedWord)
    cleanedWord = re.sub('&nbsp;', ' ', cleanedWord)

    cleanedMeaning = re.sub('<.*?>', '', meaning)
    cleanedMeaning = re.sub('&#\d{2,4};', '', cleanedMeaning)
    cleanedMeaning = re.sub('&nbsp;', ' ', cleanedMeaning)

    cleanedUsage = re.sub('<.*?>', '', usage)
    cleanedUsage = re.sub('&#\d{2,4};', '', cleanedUsage)
    cleanedUsage = re.sub('&nbsp;', ' ', cleanedUsage)

    entryForTextFile = "{}{}. {}".format(cleanedWord, cleanedMeaning, cleanedUsage)
    entryForHTMLFile = "<strong>{}</strong>{}. {}".format(cleanedWord, cleanedMeaning, cleanedUsage)

    with open(pathToTXTfile, 'a') as fileHandler:
        fileHandler.write("- {}\n".format(entryForTextFile))

    with open(pathToHTMLfile, 'a') as fileHandler:
                fileHandler.write("<li>{}</li>\n".format(entryForHTMLFile))
except:
    print("Error in retrieving information from Learner's Dictionary [http://www.learnersdictionary.com/word-of-the-day].", file = sys.stderr)


#3 MERRIAM-WEBSTER
print("Fetching word of the day from Merriam-Webster...")

url = 'http://www.merriam-webster.com/word-of-the-day/'
source = requests.get(url)

matchedObject = re.search(r'<meta property="og:title" content="Word of the Day:\s(\w*)"\s*/>', source.text)
matchedObject2 = re.search(r'<div class="wod-definition-container">[.\n\s\S]+?<h2>Definition</h2>[.\n\s\S]+?<p>(.+?)</p>[.\n\s\S]+?<h2>Examples</h2>[.\n\s\S]+?(<p>[.\n\s\S]+?</p>)', source.text)

try:
    word = matchedObject.group(1)
    meaning = matchedObject2.group(1)
    example = matchedObject2.group(2)

    cleanedWord = re.sub('<.*?>', '', word)
    cleanedWord = re.sub('&#\d{2,4};', '', cleanedWord)
    cleanedWord = re.sub('&nbsp;', ' ', cleanedWord)

    cleanedMeaning = re.sub('<.*?>', '', meaning)
    cleanedMeaning = re.sub('&#\d{2,4};', '', cleanedMeaning)
    cleanedMeaning = re.sub('&nbsp;', ' ', cleanedMeaning)

    cleanedExample = re.sub('<.*?>', '', example)
    cleanedExample = re.sub('&#\d{2,4};', '', cleanedExample)
    cleanedExample = re.sub('&nbsp;', ' ', cleanedExample)

    entryForTextFile = "{}: {}. {}".format(cleanedWord, cleanedMeaning, cleanedExample)
    entryForHTMLFile = "<strong>{}</strong>: {}. {}".format(cleanedWord, cleanedMeaning, cleanedExample)

    with open(pathToTXTfile, 'a') as fileHandler:
                fileHandler.write("- {}\n".format(entryForTextFile))

    with open(pathToHTMLfile, 'a') as fileHandler:
                fileHandler.write("<li>{}</li>\n".format(entryForHTMLFile))
except:
    print("Error in retrieving information from Merriam-Webster [http://www.merriam-webster.com/word-of-the-day/].", file = sys.stderr)


#4 THE FREE DICTIONARY
print("Fetching word of the day from The Free Dictionary...")

url = 'http://www.thefreedictionary.com/'

source = requests.get(url)

matchedObject = re.search(r'[\s\S\n]*?<a href=".*?/(.*?)">Definition</a>:</td>[\n\s]*?<td>(.*?)</td></tr>[\n\s]*?<tr>.*?Synonyms:.*?<td>(.*?)</td></tr>[\n\s]*?<tr>.*?Usage:.*?<td>(.*?)[\n\s]*?<a.*?>', source.text)

try:
    word = matchedObject.group(1)
    meaning = matchedObject.group(2)
    synonyms = matchedObject.group(3)
    usage = matchedObject.group(4)

    cleanedWord = re.sub('<.*?>', '', word)
    cleanedWord = re.sub('&#\d{2,4};', '', cleanedWord)
    cleanedWord = re.sub('&nbsp;', ' ', cleanedWord)

    cleanedMeaning = re.sub('<.*?>', '', meaning)
    cleanedMeaning = re.sub('&#\d{2,4};', '', cleanedMeaning)
    cleanedMeaning = re.sub('&nbsp;', ' ', cleanedMeaning)

    cleanedSynonyms = re.sub('<.*?>', '', synonyms)
    cleanedSynonyms = re.sub('&#\d{2,4};', '', cleanedSynonyms)
    cleanedSynonyms = re.sub('&nbsp;', ' ', cleanedSynonyms)

    cleanedUsage = re.sub('<.*?>', '', usage)
    cleanedUsage = re.sub('&#\d{2,4};', '', cleanedUsage)
    cleanedUsage = re.sub('&nbsp;', ' ', cleanedUsage)

    entryForTextFile = "{}: {} Synonyms: {}. {}".format(cleanedWord, cleanedMeaning, cleanedSynonyms, cleanedUsage)
    entryForHTMLFile = "<strong>{}</strong>: {} Synonyms: {}. {}".format(cleanedWord, cleanedMeaning, cleanedSynonyms, cleanedUsage)

    with open(pathToTXTfile, 'a') as fileHandler:
                fileHandler.write("- {}\n".format(entryForTextFile))

    with open(pathToHTMLfile, 'a') as fileHandler:
                fileHandler.write("<li>{}</li>\n".format(entryForHTMLFile))
except:
    print("Error in retrieving information from The Free Dictionary [http://www.thefreedictionary.com/].", file = sys.stderr)


#5 WORDSMITH
print("Fetching word of the day from Wordsmith...")

url = 'http://wordsmith.org/words/today.html'

source = requests.get(url)

matchedObject = re.search(r'<h3>\n(.*?)\n</h3>[\S\s\n]*?<div style=".*?">MEANING:</div>[\S\s\n]*?<div style="margin-left: 20px;">\s+?([.\s\S\n]*?)</div>[.\s\S\n]*?<div.*?>USAGE:</div>[.\n\S]*?<div.*?>\s+?[.\n\S]*?([.\n\S\s]*?.*?)[\n]</div><br>[\n\s\S]*?A THOUGHT FOR TODAY:</div>[\n\s\S]*?(.*?)[\n\s\S]*?<br><br>', source.text)

try:
    word = matchedObject.group(1)
    meaning = matchedObject.group(2)

    cleanedWord = re.sub('<.*?>', '', word)
    cleanedWord = re.sub('&#\d{2,4};', '', cleanedWord)
    cleanedWord = re.sub('&nbsp;', ' ', cleanedWord)

    cleanedMeaning = re.sub('<.*?>', '', meaning)
    cleanedMeaning = re.sub('&#\d{2,4};', '', cleanedMeaning)
    cleanedMeaning = re.sub('&nbsp;', ' ', cleanedMeaning)

    entryForTextFile = "{}: {}".format(cleanedWord, cleanedMeaning)
    entryForHTMLFile = "<strong>{}</strong>: {}".format(cleanedWord, cleanedMeaning)

    with open(pathToTXTfile, 'a') as fileHandler:
                fileHandler.write("- {}\n".format(entryForTextFile))

    with open(pathToHTMLfile, 'a') as fileHandler:
                fileHandler.write("<li>{}</li>\n".format(entryForHTMLFile))
except:
    print("Error in retrieving information from Wordsmith [http://wordsmith.org/words/today.html].", file = sys.stderr)

## HTML FOR PHRASE OF THE DAY
with open(pathToHTMLfile, 'a') as fileHandler:
                fileHandler.write("</ul>\n\n<center><h3>PHRASE OF THE DAY</h3></center>\n")

#6 INTERNATIONAL HOUSE BRISTOL
print("Fetching Phrase of the Day from International House Bristol...")

url = 'https://www.ihbristol.com/english-phrases'

source = requests.get(url)

matchedObject = re.search(r'property="dc:title"><h2>(.*?)</h2>[\S\s\n]*?field-name-field-phrase-explanation[\S\s\n]*?<div class="field-item\seven">(.*?)</div>[\S\s\n]*?field-name-field-line-ex1-1[\S\s\n]*?field-item\seven">(.*?)</div></div></div>', source.text)

try:
    phrase = matchedObject.group(1)
    meaning = matchedObject.group(2)
    usage = matchedObject.group(3)

    cleanedPhrase = re.sub('<.*?>', '', phrase)
    cleanedPhrase = re.sub('&#\d{2,4};', '', cleanedPhrase)
    cleanedPhrase = re.sub('&nbsp;', ' ', cleanedPhrase)

    cleanedMeaning = re.sub('<.*?>', '', meaning)
    cleanedMeaning = re.sub('&#\d{2,4};', '', cleanedMeaning)
    cleanedMeaning = re.sub('&nbsp;', ' ', cleanedMeaning)

    cleanedUsage = re.sub('<.*?>', '', usage)
    cleanedUsage = re.sub('&#\d{2,4};', '', cleanedUsage)
    cleanedUsage = re.sub('&nbsp;', ' ', cleanedUsage)

    entryForTextFile = "{}: {} {}".format(cleanedPhrase, cleanedMeaning, cleanedUsage)
    entryForHTMLFile = "<p><strong>{}</strong>: {} {}</p>\n\n".format(cleanedPhrase, cleanedMeaning, cleanedUsage)

    with open(pathToTXTfile, 'a') as fileHandler:
                fileHandler.write("PHRASE OF THE DAY - {}\n".format(entryForTextFile))

    with open(pathToHTMLfile, 'a') as fileHandler:
                fileHandler.write("{}".format(entryForHTMLFile))

except:
    print("Error in retrieving information from International House Bristol [https://www.ihbristol.com/english-phrases].", file = sys.stderr)


## HTML FOR THOUGHT FOR THE DAY
with open(pathToHTMLfile, 'a') as fileHandler:
                fileHandler.write("<center><h3>THOUGHT FOR TODAY</h3></center>\n")

#7 WORDSMITH
print("Fetching Thought for the Day from Wordsmith...")

url = 'http://wordsmith.org/words/today.html'
 
source = requests.get(url)

matchedObject = re.search(r'<h3>\n.*?\n</h3>[\S\s\n]*?<div style=".*?">MEANING:</div>[\S\s\n]*?<div style="margin-left: 20px;">[.\s\S\n]*?</div>[.\s\S\n]*?<div.*?>USAGE:</div>[.\n\S]*?<div.*?>[.\n\S]*?[.\n\S\s]*?.*?[\n]</div><br>[\n\s\S]*?A THOUGHT FOR TODAY:</div>\s+?(.*?[\n\s\S]*?)<br><br>', source.text)

try:
    thought = matchedObject.group(1)

    entry = "".format(thought)

    cleanedThought = re.sub('<.*?>', '', thought)
    cleanedThought = re.sub('&#\d{2,4};', '', cleanedThought)
    cleanedThought = re.sub('&nbsp;', ' ', cleanedThought)

    entryForTextFile = "{}".format(cleanedThought)
    entryForHTMLFile = "{}".format(cleanedThought)

    with open(pathToTXTfile, 'a') as fileHandler:
                fileHandler.write("\nTHOUGHT FOR TODAY - {}\n".format(entryForTextFile))

    with open(pathToHTMLfile, 'a') as fileHandler:
                fileHandler.write("<p>{}</p>\n".format(entryForHTMLFile))

except:
    print("Error in retrieving information from Word Smith [http://wordsmith.org/words/today.html].", file = sys.stderr)



## ENDING HTML
with open(pathToHTMLfile, 'a') as fileHandler:
                fileHandler.write("</div>\n\n</body>\n\n</html>")

## APPENDING TODAY'S CONTENTS TO ARCHIVE
with open(pathToTXTfile, 'r') as fileHandler:
    contents = fileHandler.read()

with open(pathToArchiveFile, 'a') as fileHandler:
    fileHandler.write("{}".format(contents))

## OPENING TEXT FILES, HTML AND THE CONTAINING FOLDER
print("Opening files and containing directory.")
print("Finished")

webbrowser.open(pathToTXTfile)
webbrowser.open(pathToArchiveFile)
webbrowser.open(pathToHTMLfile)

subprocess.Popen(['explorer', locationOfYourScript])
