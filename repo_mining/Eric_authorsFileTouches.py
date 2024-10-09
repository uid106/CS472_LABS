import requests
import csv
import os
from collections import defaultdict
from Eric_CollectFiles import countfiles, github_auth

# Ensure data directory exists
if not os.path.exists("Eric_data"):
    os.makedirs("Eric_data")

def collect_authors_dates(dictfiles, lsttokens, repo):
    ipage = 1
    ct = 0
    authors_dates = defaultdict(list)

    try:
        while True:
            commitsUrl = f'https://api.github.com/repos/{repo}/commits?page={ipage}&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            if not jsonCommits:  # Break loop if no more commits
                break

            for shaObject in jsonCommits:
                sha = shaObject['sha']
                shaUrl = f'https://api.github.com/repos/{repo}/commits/{sha}'
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                
                if shaDetails is None:
                    print(f"Error retrieving details for commit {sha}")
                    continue

                author = shaDetails['commit']['author']['name']
                date = shaDetails['commit']['author']['date']

                # Check for 'files' in shaDetails safely
                filesjson = shaDetails.get('files', [])
                for fileObj in filesjson:
                    filename = fileObj['filename']
                    if filename in dictfiles:
                        authors_dates[filename].append((author, date))

            ipage += 1

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except KeyError as e:
        print(f"Key error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return authors_dates

# Define your GitHub repository and tokens
repo = 'scottyab/rootbeer'
lstTokens = [""] 

# Collect files from the repository using countfiles function
dictfiles = {}
countfiles(dictfiles, lstTokens, repo)

# Collect authors and dates for each file
authors_dates = collect_authors_dates(dictfiles, lstTokens, repo)

# Output the collected data to a CSV file
fileOutput = f'Eric_data/authors_dates_{repo.split("/")[1]}.csv'
with open(fileOutput, 'w', newline='') as fileCSV:
    writer = csv.writer(fileCSV)
    writer.writerow(["Filename", "Author", "Date"])

    for filename, touches in authors_dates.items():
        writer.writerows([[filename, author, date] for author, date in touches])

print(f"The data has now been saved to {fileOutput}")
