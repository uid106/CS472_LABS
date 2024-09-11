import json
import requests
import csv
import os
from Brandon_CollectFiles import countfiles, github_auth

if not os.path.exists("Brandon_data"):
    os.makedirs("Brandon_data")

def collect_authors_dates(dictfiles, lsttokens, repo):
    ipage = 1
    ct = 0
    authors_dates = {}

    try:
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            if len(jsonCommits) == 0:
                break

            for shaObject in jsonCommits:
                sha = shaObject['sha']
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
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

repo = 'scottyab/rootbeer'
lstTokens = [""]

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)
authors_dates = collect_authors_dates(dictfiles, lstTokens, repo)

fileOutput = 'Brandon_data/authors_dates_' + repo.split('/')[1] + '.csv'
rows = ["Filename", "Author", "Date"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

for filename, touches in authors_dates.items():
    for author, date in touches:
        rows = [filename, author, date]
        writer.writerow(rows)
fileCSV.close()