import os
import json
from dotenv import load_dotenv

from fetch_traffic import fetch_repo_stats, save_stats
from drawing import create_graphs_for_repo
from generate_readme import update_readme

def load_settings(file_path):
    """Load settings from a JSON file."""
    with open(file_path, "r") as f:
        settings = json.load(f)
    return settings

def configure_environment():
    """Configure the environment variables."""
    load_dotenv()
    github_api_token = os.getenv("GH_SECRET_TOKEN")
    headers = {
        "Authorization": f"token {github_api_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    config = load_settings("config.json")
    data_dir, images_dir, theme, owner, repos = (
        config.get(key, default) for key, default in (
            ("data_dir", ""),
            ("images_dir", ""),
            ("theme", "chartreuse_dark"),
            ("owner", ""),
            ("repositories", [])
        )
    )
    return headers, data_dir, images_dir, theme, owner, repos

def main():
    """
    Main function to fetch repo stats, create graphs, and update README.
    """
    headers, data_dir, images_dir, theme, owner, repos = configure_environment()

    for repo in repos:
        stats = fetch_repo_stats(owner, repo, headers)
        save_stats(repo, stats, data_dir)
        create_graphs_for_repo(theme, repo, data_dir, images_dir)
        print("________________________________________________________________________")

    update_readme(
        theme=theme,
        owner=owner,
        base_path=images_dir,
        data_path=data_dir
    )
    print("Stats fetched and saved, README updated !")

if __name__ == "__main__":
    main()