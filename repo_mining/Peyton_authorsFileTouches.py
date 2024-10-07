import json
import requests
import csv

import os

if not os.path.exists("data"):
 os.makedirs("data")

# GitHub Authentication function
def github_auth(url, token_list, current_token_index):

   # Function to authenticate with GitHub API using a list of tokens.
    
   # Args:
   #     url (str): The GitHub API URL to make the request to.
   #    token_list (list): A list of authentication tokens.
   #     current_token_index (int): The current index of the token being used.
        
   # Returns:
   #     tuple: Contains the JSON response data (if available) and the updated token index.

    json_data = None  # Initialize the response data
    try:
        # Cycle through the list of tokens using modulus to avoid index out of range
        current_token_index = current_token_index % len(token_list)
        
        # Set up the authorization header using the current token
        headers = {'Authorization': f'Bearer {token_list[current_token_index]}'}
        
        # Make the request to the GitHub API
        response = requests.get(url, headers=headers)
        
        # Parse the response content as JSON
        json_data = response.json()
        
        # Increment the token index for the next call
        current_token_index += 1
    except Exception as e:
        # Handle any exceptions, e.g., network errors
        print(f"An error occurred: {e}")
    
    # Return the response data and the updated token index
    return json_data, current_token_index

# Mapping of Language to Extension Type
mapping = {'Java': ['.java'],'Kotlin': ['.kt'],'C++': ['.cpp', '.h'],'C': ['.c', '.h'],'CMake': ['.cmake', 'CMakeLists.txt']}

# Getting Languages Used in Repo
def get_languages(repo, lsttokens):
    url = 'https://api.github.com/repos/' + repo + '/languages'
    languages, _ = github_auth(url,lsttokens,0)
    return languages.keys()

# Checking extension Type and Seeing if it Matches Language Mapping
def check_extension(language):
    extension = []
    for x in language:
        if x in mapping:
            extension += mapping[x]
    return extension

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo, get_extension):
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for commit in jsonCommits:
                sha = commit['sha']
                author = commit['commit']['author']['name']
                date = commit['commit']['author']['date']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    # If A Source File from Listed Mapping add to Dictionary
                    if any(filename.endswith(ext) for ext in get_extension):
                        dictfiles[filename] = dictfiles.get(filename, []) + [(author,date)]
                        # Print Matching Iterations
                        print(f"File: {filename}, Author: {author}, Date {date}")
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)
# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'

# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = [""]

# Calling Functions and Saving Results
get_languages = get_languages(repo,lstTokens)
get_extensions = check_extension(get_languages)

dictfiles = {}
countfiles(dictfiles, lstTokens, repo, get_extensions)


file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/Peyton_authorsTouches.csv'
rows = ["Filename", "Author", "Date"]

# Saving to CSV selected Extension Types
with open(fileOutput, 'w') as fileCSV:
    writer = csv.writer(fileCSV)
    writer.writerow(rows)

    for filename, touches in dictfiles.items():
        for author, date in touches:
            writer.writerow([filename, author, date])