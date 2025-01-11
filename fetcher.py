import requests
import os
import argparse
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get the token from environment variables
TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    raise Exception("GitHub token not found in environment variables.")

HEADERS = {"Authorization": f"token {TOKEN}"}

# Parse command-line arguments
def get_args():
    parser = argparse.ArgumentParser(description="Clone top GitHub repositories from an organization based on language.")
    parser.add_argument("--org", type=str, default="microsoft", help="GitHub organization name (default: microsoft)")
    parser.add_argument("--language", type=str, default="C", help="Programming language filter (default: C)")
    parser.add_argument("--top_n", type=str, default="5", help="Number of top repositories to clone (default: 5)")
    return parser.parse_args()

# Function to get repositories
def get_repositories(org, language, top_n=5):
    top_n = int(top_n)  # Ensure top_n is an integer
    url = f"https://api.github.com/orgs/{org}/repos?per_page=100"
    repos = []

    while url:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code}, {response.text}")
        repos.extend(response.json())
        url = response.links.get("next", {}).get("url")  # Handle pagination

    # Filter by language and sort by stars
    filtered_repos = [repo for repo in repos if repo["language"] == language]
    sorted_repos = sorted(filtered_repos, key=lambda x: x["stargazers_count"], reverse=True)

    return sorted_repos[:top_n]  # Ensure slicing works correctly

# Clone repositories
def clone_repositories(repos):
    for repo in repos:
        name = repo["name"]
        clone_url = repo["clone_url"]
        print(f"Cloning {name} with submodules...")
        os.system(f"git clone --recurse-submodules {clone_url}")

if __name__ == "__main__":
    args = get_args()
    args.top_n = int(args.top_n)  # Ensure top_n is converted to an integer

    print(f"Fetching top {args.top_n} repositories from {args.org} in {args.language}...")
    top_repos = get_repositories(args.org, args.language, args.top_n)

    print("Cloning repositories:")
    clone_repositories(top_repos)
