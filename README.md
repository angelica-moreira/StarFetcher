# StarFetcher

## Overview
This script fetches and clones the top GitHub repositories from a specified organization based on a chosen programming language. The repositories are sorted by the number of stars, and the top N repositories are cloned.

## Prerequisites
- Python 3.x
- Git installed on your machine
- A GitHub personal access token
- `requests` and `python-dotenv` Python libraries

## Installation
1. Clone this repository or download the script.
2. Install the required dependencies:
   ```sh
   pip install requests python-dotenv
   ```
3. Create a `.env` file in the same directory as the script and add your GitHub token:
   ```sh
   GITHUB_TOKEN=your_personal_access_token
   ```

## Usage
Run the script with optional command-line arguments:

```sh
python3 fetcher.py --org=<organization_name> --language=<programming_language> --top_n=<number_of_repos> --threads=<number_of_threads> --force
```

### Parameters:
- `--org` (default: `microsoft`): The GitHub organization name.
- `--language` (default: `C`): The programming language filter.
- `--top_n` (default: `5`): Number of top repositories to clone.
- `--threads` (default: `4`): Number of threads for parallel cloning (optional, use for faster cloning).
- `--force` (optional): Force delete the existing `cloned_repos` directory without prompting.

### Example:
To fetch and clone the top 3 Python repositories from Microsoft, with 6 threads:
```sh
python3 fetcher.py --org=microsoft --language=Python --top_n=3 --threads=6
```

## How It Works
1. The script retrieves repositories from the specified GitHub organization.
2. Filters the repositories based on the specified language.
3. Sorts them by star count in descending order.
4. Clones the top N repositories using Git with parallel cloning support.

## License
This project is licensed under the MIT License.
