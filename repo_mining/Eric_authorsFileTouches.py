import requests
import json
import csv
import os
from Eric_CollectFiles import countfiles, github_auth  

if not os.path.exists("Eric_data"):
    os.makedirs("Eric_data")

def collect_authors_dates(dictfiles, lsttokens, repo):
    ipage = 1
    ct = 0
    authors_dates = {}

    try:
        while True:
            spage = str(ipage)
            commitsUrl = f'https://api.github.com/repos/{repo}/commits?page={spage}&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            if len(jsonCommits) == 0:
                break  # No more commits

            for shaObject in jsonCommits:
                sha = shaObject['sha']
                shaUrl = f'https://api.github.com/repos/{repo}/commits/{sha}'
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                if shaDetails is None:
                    print(f"Error retrieving details for commit {sha}")
                    continue

                author = shaDetails['commit']['author']['name']
                date = shaDetails['commit']['author']['date']
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    if filename in dictfiles:
                        if filename not in authors_dates:
                            authors_dates[filename] = []
                        authors_dates[filename].append((author, date))
            ipage += 1
    except Exception as e:
        print(f"Error receiving data: {e}")
        exit(0)
    return authors_dates

# Define your GitHub repository and tokens
repo = 'scottyab/rootbeer'
lstTokens = [""] 

# Collect files from the repository using countfiles function
dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)

# Collect authors and dates for each file
authors_dates = collect_authors_dates(dictfiles, lstTokens, repo)

# Output the collected data to a CSV file
fileOutput = f'Eric_data/authors_dates_{repo.split("/")[1]}.csv'
rows = ["Filename", "Author", "Date"]
with open(fileOutput, 'w', newline='') as fileCSV:
    writer = csv.writer(fileCSV)
    writer.writerow(rows)

    for filename, touches in authors_dates.items():
        for author, date in touches:
            writer.writerow([filename, author, date])

print(f"The data has now been saved to {fileOutput}")
