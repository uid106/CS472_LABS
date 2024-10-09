import json
import requests
import csv
import os

# Check if "Eric_data" directory exists, if not, create it
if not os.path.exists("Eric_data"):
    os.makedirs("Eric_data")

# GitHub Authentication function
# @param url: GitHub API URL to make the request
# @param lsttoken: List of GitHub authentication tokens
# @param ct: Current index of the token to be used (rotates through tokens)
# @return: JSON response from GitHub API and updated token index
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        # Rotate through tokens using modulo operator
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1  # Increment token counter for next use
    except Exception as e:
        # Handle exceptions by printing the error message
        pass
        print(e)
    return jsonData, ct

# Function to count the number of times each file has been touched (modified) in a GitHub repo
# @param dictfiles: Dictionary to store file names and their touch count
# @param lsttokens: List of GitHub authentication tokens
# @param repo: Repository name in the format 'owner/repo'
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # Page counter for API pagination
    ct = 0  # Token index counter
    v_extensions = ['.java', '.kt', '.cpp', '.c', '.cmake']  # File extensions to track

    try:
        # Loop through commit pages until no more commits are returned
        while True:
            spage = str(ipage)  # Convert page number to string for URL
            commitsUrl = f'https://api.github.com/repos/{repo}/commits?page={spage}&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # Exit loop when no more commits are found
            if len(jsonCommits) == 0:
                break

            # Process each commit in the current page
            for shaObject in jsonCommits:
                sha = shaObject['sha']  # Extract commit SHA
                # Fetch details for the specific commit
                shaUrl = f'https://api.github.com/repos/{repo}/commits/{sha}'
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)

                # Extract the list of files changed in this commit
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']  # Get the file name
                    # Increment touch count if the file has a tracked extension
                    if any(filename.endswith(ext) for ext in v_extensions):
                        dictfiles[filename] = dictfiles.get(filename, 0) + 1
                    print(filename)  # Print the file name being processed
            ipage += 1  # Move to the next page of commits
    except:
        # Handle any errors and exit the script
        print("Error receiving data")
        exit(0)

# GitHub repository to be analyzed
repo = 'scottyab/rootbeer'
# Other example repos (heavy in commits)
# repo = 'Skyscanner/backpack'
# repo = 'k9mail/k-9'
# repo = 'mendhak/gpslogger'

# List of authentication tokens (empty here for security reasons)
# Ensure to create and provide multiple tokens for large repositories
lstTokens = [""]

dictfiles = dict()  # Dictionary to store file touch counts
countfiles(dictfiles, lstTokens, repo)  # Call function to populate file touch counts

# Output the total number of files touched
print('Total number of files: ' + str(len(dictfiles)))

# Prepare to write results to a CSV file
file = repo.split('/')[1]  # Extract repository name to use in file name
fileOutput = f'Eric_data/file_{file}.csv'  # Define output file path
rows = ["Filename", "Touches"]  # Define CSV headers
fileCSV = open(fileOutput, 'w')  # Open CSV file for writing
writer = csv.writer(fileCSV)
writer.writerow(rows)  # Write CSV headers

bigcount = None  # Variable to store the largest touch count
bigfilename = None  # Variable to store the file with the largest touch count

# Write each file and its touch count to the CSV
for filename, count in dictfiles.items():
    rows = [filename, count]
    writer.writerow(rows)
    # Track the file with the highest touch count
    if bigcount is None or count > bigcount:
        bigcount = count
        bigfilename = filename

fileCSV.close()  # Close the CSV file after writing
# Output the file with the highest touch count
print(f'The file {bigfilename} has been touched {bigcount} times.')
