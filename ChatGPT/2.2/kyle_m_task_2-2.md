# GitHub File Count Script Documentation

This script analyzes a GitHub repository, identifying the source files that have been modified the most. It uses the GitHub API to retrieve commit data and count how many times specific files have been changed, then exports the results to a CSV file.

### Key Features
- **GitHub API Interaction**: Uses GitHub tokens for authentication and retrieves commit history for a given repository.
- **File Tracking**: Counts how many times specific file types (e.g., `.java`, `.kt`, `.cpp`, `.h`) are modified.
- **CSV Export**: Saves the results in a CSV file, listing each file and how often it was changed.

### Main Functions
1. **`github_auth(url, lsttoken, ct)`**: Authenticates with GitHub and fetches data from the API.
2. **`countfiles(dictfiles, lsttokens, repo)`**: Collects commit data and counts how many times each file has been modified.

### Usage
- **Repository**: Specify the GitHub repository in the `repo` variable (e.g., `'scottyab/rootbeer'`).
- **Tokens**: Add your GitHub tokens to the `lstTokens` list for authentication.
- **Output**: Results are saved in a CSV file inside the `KyleM_data` directory.

### Example Output
The script prints the total number of unique files and identifies the most frequently modified file.
