import json
import requests
import csv

import os

if not os.path.exists("KyleM_data"):
 os.makedirs("KyleM_data")

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

def build_commits_url(repo, page):
    """Builds the URL for retrieving a page of commits."""
    return f'https://api.github.com/repos/{repo}/commits?page={page}&per_page=100'

def build_commit_details_url(repo, sha):
    """Builds the URL for retrieving commit details by SHA."""
    return f'https://api.github.com/repos/{repo}/commits/{sha}'

def process_commit_files(filesjson, shaDetails, writer):
    """Processes the files touched by a commit and writes relevant data to CSV."""
    source_ext = ['.java', '.kt', '.cpp', '.h']
    
    for file in filesjson:
        filename = file['filename']
        if any(filename.endswith(ext) for ext in source_ext):
            author = shaDetails['commit']['author']['name']
            date = shaDetails['commit']['author']['date']
            writer.writerow([filename, author, date])
            print(f"{filename} : {author} : {date}")

def get_commit_data(commitsUrl, lsttokens, ct):
    """Gets the commit data for a given commit URL."""
    return github_auth(commitsUrl, lsttokens, ct)

def count_files(lsttokens, repo, writer):
    """Counts files in a GitHub repository that match certain extensions."""
    page = 1
    token_counter = 0
    
    try:
        while True:
            commitsUrl = build_commits_url(repo, page)
            jsonCommits, token_counter = get_commit_data(commitsUrl, lsttokens, token_counter)

            if not jsonCommits:  # Break if no more commits are found
                break
            
            for commit in jsonCommits:
                sha = commit['sha']
                commitDetailsUrl = build_commit_details_url(repo, sha)
                shaDetails, token_counter = get_commit_data(commitDetailsUrl, lsttokens, token_counter)
                process_commit_files(shaDetails['files'], shaDetails, writer)

            page += 1
    except Exception as e:
        print(f"Error receiving data: {e}")
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
lstTokens = ["nope",
                "nope",
                "nope"]



file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'KyleM_data/authorsTouches.csv'
rows = ["Filename", "Author","Date"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

count_files(lstTokens, repo, writer)

fileCSV.close()
