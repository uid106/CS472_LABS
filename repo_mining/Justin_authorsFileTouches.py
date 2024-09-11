import json
import csv
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Ensure data directory exists
DATA_DIR = "Justin_data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# GitHub Authentication function
def github_auth(url, tokens, token_index):
    """
    Authenticates and retrieves data from a GitHub API request.
    
    Parameters:
    - url (str): GitHub API URL.
    - tokens (list): List of GitHub API tokens.
    - token_index (int): Current index for token rotation.
    
    Returns:
    - jsonData (dict): Parsed JSON response.
    - token_index (int): Updated token index.
    """
    jsonData = None
    try:
        token_index = token_index % len(tokens)
        headers = {'Authorization': f'Bearer {tokens[token_index]}'}
        request = Request(url, headers=headers)
        with urlopen(request) as response:
            jsonData = json.load(response)
        token_index += 1
    except (HTTPError, URLError) as e:
        print(f"Error during GitHub request: {e}")
    return jsonData, token_index

# Mapping of Language to File Extensions
LANGUAGE_MAPPING = {
    'Java': ['.java'],
    'Kotlin': ['.kt'],
    'C++': ['.cpp', '.h'],
    'C': ['.c', '.h'],
    'CMake': ['.cmake', 'CMakeLists.txt']
}

def get_repo_languages(repo, tokens):
    """
    Retrieves the programming languages used in the repository.
    
    Parameters:
    - repo (str): GitHub repository in the format 'owner/repo'.
    - tokens (list): GitHub API tokens.
    
    Returns:
    - languages (list): List of languages used in the repo.
    """
    url = f'https://api.github.com/repos/{repo}/languages'
    languages, _ = github_auth(url, tokens, 0)
    return list(languages.keys())

def get_file_extensions(languages):
    """
    Maps languages to their corresponding file extensions.
    
    Parameters:
    - languages (list): List of languages used in the repository.
    
    Returns:
    - extensions (list): List of file extensions to look for.
    """
    extensions = []
    for lang in languages:
        if lang in LANGUAGE_MAPPING:
            extensions += LANGUAGE_MAPPING[lang]
    return extensions

def collect_commit_data(files_dict, tokens, repo, valid_extensions):
    """
    Collects commit data and tracks which authors touched which files.
    
    Parameters:
    - files_dict (dict): Dictionary to store file authorship data.
    - tokens (list): GitHub API tokens.
    - repo (str): GitHub repository in the format 'owner/repo'.
    - valid_extensions (list): List of valid file extensions to check.
    
    Returns:
    None. (Modifies the files_dict in place).
    """
    page = 1
    token_index = 0

    try:
        while True:
            # Build URL for commit data retrieval
            commit_url = f'https://api.github.com/repos/{repo}/commits?page={page}&per_page=100'
            commits, token_index = github_auth(commit_url, tokens, token_index)

            # Exit if no more commits
            if not commits:
                break

            # Process each commit
            for commit in commits:
                sha = commit['sha']
                author = commit['commit']['author']['name']
                date = commit['commit']['author']['date']

                # Get detailed commit data (files modified in that commit)
                sha_url = f'https://api.github.com/repos/{repo}/commits/{sha}'
                commit_details, token_index = github_auth(sha_url, tokens, token_index)

                if not commit_details or 'files' not in commit_details:
                    continue
                
                files_changed = commit_details['files']
                
                # Track authorship for each valid file
                for file in files_changed:
                    filename = file['filename']
                    if any(filename.endswith(ext) for ext in valid_extensions):
                        if filename not in files_dict:
                            files_dict[filename] = []
                        files_dict[filename].append((author, date))
                        print(f"File: {filename}, Author: {author}, Date: {date}")
            
            page += 1
    except Exception as e:
        print(f"Error during commit data collection: {e}")
        exit(1)

def save_file_touches_to_csv(file_data, output_file):
    """
    Saves file touches (authors and dates) to a CSV file.
    
    Parameters:
    - file_data (dict): Dictionary of file names and their authorship data.
    - output_file (str): Path to the CSV output file.
    
    Returns:
    None.
    """
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename", "Author", "Date"])
        
        for filename, touches in file_data.items():
            for author, date in touches:
                writer.writerow([filename, author, date])

    print(f"Data saved to {output_file}")

# Main script execution
if __name__ == "__main__":
    # Specify GitHub repository and tokens
    repo = 'scottyab/rootbeer'
    tokens = [""]  # Add your tokens here

    # Get languages and file extensions used in the repository
    repo_languages = get_repo_languages(repo, tokens)
    file_extensions = get_file_extensions(repo_languages)

    # Dictionary to store file authorship data
    file_data = {}

    # Collect commit data for files with valid extensions
    collect_commit_data(file_data, tokens, repo, file_extensions)

    # Define output file path
    output_csv = os.path.join(DATA_DIR, 'Justin_authorsTouches.csv')

    # Save the collected file authorship data to CSV
    save_file_touches_to_csv(file_data, output_csv)

