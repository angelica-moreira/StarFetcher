import requests
import os
import argparse
import shutil
import subprocess
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get the token from environment variables
TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    raise ValueError("GitHub token not found in environment variables.")

HEADERS = {"Authorization": f"token {TOKEN}"}


# Parse command-line arguments
def get_args():
    parser = argparse.ArgumentParser(description="Clone top GitHub repositories from an organization based on language.")
    parser.add_argument("--org", type=str, default="microsoft", help="GitHub organization name (default: microsoft)")
    parser.add_argument("--language", type=str, default="C", help="Programming language filter (default: C)")
    parser.add_argument("--top_n", type=int, default=5, help="Number of top repositories to clone (default: 5)")
    parser.add_argument("--force", action="store_true", help="Force delete existing 'cloned_repos' directory without asking")
    return parser.parse_args()


# Function to get repositories
def get_repositories(org, language, top_n=5):
    url = f"https://api.github.com/orgs/{org}/repos?per_page=100"
    repos = []

    while url:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 403:
            raise PermissionError("API rate limit exceeded. Try again later or use an authenticated token.")
        elif response.status_code != 200:
            raise Exception(f"Error fetching repositories: {response.status_code}, {response.text}")

        repos.extend(response.json())
        url = response.links.get("next", {}).get("url")  # Handle pagination

    # Filter by language (handle None values safely)
    filtered_repos = [repo for repo in repos if repo.get("language") and repo["language"].lower() == language.lower()]

    if not filtered_repos:
        raise ValueError(f"No repositories found in '{org}' using language '{language}'.")

    # Sort by stargazers_count
    sorted_repos = sorted(filtered_repos, key=lambda x: x["stargazers_count"], reverse=True)

    return sorted_repos[:top_n]


# Prepare cloning directory
def prepare_cloning_directory(force=False):
    repo_dir = "cloned_repos"
    if os.path.exists(repo_dir):
        if force:
            shutil.rmtree(repo_dir)
        else:
            response = input(f"The folder '{repo_dir}' already exists. Do you want to delete its contents? (y/n): ")
            if response.lower() != 'y':
                print("Aborting operation.")
                exit(1)
            shutil.rmtree(repo_dir)

    os.makedirs(repo_dir, exist_ok=True)
    return repo_dir


# Clone repositories
def clone_repositories(repos, repo_dir):
    for repo in repos:
        name = repo["name"]
        clone_url = repo["clone_url"]
        print(f"Cloning {name} with submodules...")
        
        repo_path = os.path.join(repo_dir, name)
        try:
            subprocess.run(["git", "clone", "--recurse-submodules", clone_url, repo_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error cloning {name}: {e}")


if __name__ == "__main__":
    args = get_args()

    print(f"Fetching top {args.top_n} repositories from {args.org} in {args.language}...")
    try:
        top_repos = get_repositories(args.org, args.language, args.top_n)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

    repo_dir = prepare_cloning_directory(args.force)

    print("Cloning repositories:")
    clone_repositories(top_repos, repo_dir)
