import requests #get(url)
import re #regular expressions to find certain words/phrases
import datetime #today's date/time
import sys
import os #
import subprocess
import time
import webbrowser

def main():
    """Scrape dictionary.com for word of the day info, overwrite scraped info to txt file, append to archive file."""
    ## SETTING UP TXT FILE
    locationOfYourScript = r'{}'.format(os.path.dirname(os.path.realpath(__file__)))

    os.chdir(locationOfYourScript)
    pathToTXTfile = r'{}\today.txt'.format(os.getcwd())
    pathToArchiveFile = r'{}\archive.txt'.format(os.getcwd())

    # Getting today's date
    today = datetime.date.today().strftime("%A %d %B %Y")

    # Overwriting existing files containing today's words
    with open(pathToTXTfile, 'w') as fileHandler:
                    fileHandler.write("\t\t********************* {} *********************".format(today))
                    fileHandler.write("\nWORD OF THE DAY\n")



    ## SCRAPING AND POPULATING TXT
    ## DICTIONARY.COM
    print("Fetching word of the day from Dictionary.com...")

    url = 'http://dictionary.reference.com/wordoftheday/'
    source = requests.get(url)

    matchedObject = re.search(r'Definitions for <strong>(.+?)</strong>[\S\s\n]*?<li class="first"><span>(.+?)</span></li>', source.text)

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

        with open(pathToTXTfile, 'a') as fileHandler:
                    fileHandler.write("- {}\n".format(entryForTextFile))

    except:
        print("Error in retrieving information from The Free Dictionary [http://www.thefreedictionary.com/].", file = sys.stderr)



    ## APPENDING TODAY'S CONTENTS TO ARCHIVE
    with open(pathToTXTfile, 'r') as fileHandler:
        contents = fileHandler.read()

    with open(pathToArchiveFile, 'a') as fileHandler:
        fileHandler.write("{}".format(contents))

    print("Done.")
    
if __name__=="__main__":
    main()
