import requests
import json
import os
from datetime import datetime


def fetch_repo_stats(owner, repo, headers):
    """
    Fetches GitHub repository statistics including views, clones, forks, and stars.
        :param owner: GitHub repository owner
        :param repo: GitHub repository name
        :param headers: Headers for GitHub API requests
        :return: Dictionary containing repository statistics
    """
    base_url = f"https://api.github.com/repos/{owner}/{repo}"
    print(f"Fetching stats for {repo}...")

    repo_data = requests.get(base_url, headers=headers).json()
    forks = repo_data.get("forks_count", 0)
    stars = repo_data.get("stargazers_count", 0)

    traffic_url = f"{base_url}/traffic/views"
    views_data = requests.get(traffic_url, headers=headers).json()

    clones_url = f"{base_url}/traffic/clones"
    clones_data = requests.get(clones_url, headers=headers).json()

    referring_sites_url = f"{base_url}/traffic/popular/referrers"
    referring_sites = requests.get(referring_sites_url, headers=headers).json()

    popular_content_url = f"{base_url}/traffic/popular/paths"
    popular_content = requests.get(popular_content_url, headers=headers).json()

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "views": {
            "total": views_data.get("count", 0),
            "unique_visitors": views_data.get("uniques", 0),
        },
        "clones": {
            "total": clones_data.get("count", 0),
            "unique_cloners": clones_data.get("uniques", 0),
        },
        "referring_sites": referring_sites,
        "popular_content": popular_content,
        "forks": forks,
        "stars": stars
    }


def save_stats(repo_name, stats, output_dir):
    """
    Save the fetched statistics to a JSON file.
        :param repo_name: Name of the repository
        :param stats: Statistics to save
        :param output_dir: Directory to save the JSON file
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_path = os.path.join(output_dir, f"{repo_name.replace('/', '_')}.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_data.append(stats)

    with open(file_path, "w") as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)

    print(f"... stats saved to {file_path}.")



