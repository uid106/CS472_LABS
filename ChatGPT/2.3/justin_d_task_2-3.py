import json
import csv
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from collections import defaultdict
from typing import List, Tuple, Dict, Optional

# Constants
DATA_DIR = "Justin_data"
GITHUB_API_URL = 'https://api.github.com/repos'
LANGUAGE_MAPPING = {
    'Java': ['.java'],
    'Kotlin': ['.kt'],
    'C++': ['.cpp', '.h'],
    'C': ['.c', '.h'],
    'CMake': ['.cmake', 'CMakeLists.txt']
}

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def github_auth(url: str, tokens: List[str], token_index: int) -> Tuple[Optional[Dict], int]:
    """Authenticates and retrieves data from a GitHub API request."""
    try:
        token_index %= len(tokens)
        headers = {'Authorization': f'Bearer {tokens[token_index]}'}
        request = Request(url, headers=headers)
        with urlopen(request) as response:
            jsonData = json.load(response)
        return jsonData, token_index + 1
    except (HTTPError, URLError) as e:
        print(f"Error during GitHub request: {e}")
        return None, token_index  # Return token_index unchanged

def get_repo_languages(repo: str, tokens: List[str]) -> List[str]:
    """Retrieves the programming languages used in the repository."""
    url = f'{GITHUB_API_URL}/{repo}/languages'
    languages, _ = github_auth(url, tokens, 0)
    return list(languages.keys()) if languages else []

def get_file_extensions(languages: List[str]) -> List[str]:
    """Maps languages to their corresponding file extensions."""
    return [ext for lang in languages if lang in LANGUAGE_MAPPING for ext in LANGUAGE_MAPPING[lang]]

def collect_commit_data(files_dict: defaultdict, tokens: List[str], repo: str, valid_extensions: List[str]) -> None:
    """Collects commit data and tracks which authors touched which files."""
    page = 1
    token_index = 0

    while True:
        commit_url = f'{GITHUB_API_URL}/{repo}/commits?page={page}&per_page=100'
        commits, token_index = github_auth(commit_url, tokens, token_index)

        if not commits:
            break

        for commit in commits:
            sha = commit['sha']
            author = commit['commit']['author']['name']
            date = commit['commit']['author']['date']

            sha_url = f'{GITHUB_API_URL}/{repo}/commits/{sha}'
            commit_details, token_index = github_auth(sha_url, tokens, token_index)

            if commit_details and 'files' in commit_details:
                for file in commit_details['files']:
                    filename = file['filename']
                    if any(filename.endswith(ext) for ext in valid_extensions):
                        files_dict[filename].append((author, date))
                        print(f"File: {filename}, Author: {author}, Date: {date}")
        page += 1

def save_file_touches_to_csv(file_data: Dict[str, List[Tuple[str, str]]], output_file: str) -> None:
    """Saves file touches (authors and dates) to a CSV file."""
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename", "Author", "Date"])
        for filename, touches in file_data.items():
            writer.writerows(touches)

    print(f"Data saved to {output_file}")

# Main script execution
if __name__ == "__main__":
    repo = 'scottyab/rootbeer'
    tokens = [""]  # Add your tokens here

    # Get languages and file extensions used in the repository
    repo_languages = get_repo_languages(repo, tokens)
    file_extensions = get_file_extensions(repo_languages)

    # Dictionary to store file authorship data
    file_data = defaultdict(list)

    # Collect commit data for files with valid extensions
    collect_commit_data(file_data, tokens, repo, file_extensions)

    # Define output file path
    output_csv = os.path.join(DATA_DIR, 'Justin_authorsTouches.csv')

    # Save the collected file authorship data to CSV
    save_file_touches_to_csv(file_data, output_csv)
