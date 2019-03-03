import requests
import re
import datetime
import sys
import os #check
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



## SCRAPING AND POPULATING TXT
DICTIONARY.COM
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

subprocess.Popen(['explorer', locationOfYourScript])
