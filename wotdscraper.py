import requests
import re
import datetime
import sys
import os
import subprocess
import time
import webbrowser

def main():
    #path to text file is just file name (in working directory)
    pathToTXTfile = 'today.txt'

    # Getting today's date
    today = datetime.date.today().strftime("%A %d %B %Y")

    # Overwriting existing files containing today's words
    with open(pathToTXTfile, 'w') as fileHandler:
        fileHandler.write("\nWORDS OF THE DAY\n\n")

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

        with open(pathToTXTfile, 'a') as fileHandler:
                    fileHandler.write("- {}\n".format(entryForTextFile))

    except:
        print("Error in retrieving information from The Free Dictionary [http://www.thefreedictionary.com/].", file = sys.stderr)


    ## OPENING TEXT FILES, HTML AND THE CONTAINING FOLDER
    print("Finished. \nCheck your email. :)")

if __name__ == "__main__":
    main()
