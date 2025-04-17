import os
import json


def read_table_as_markdown(file_path):
    """ Reads a Markdown table from a file and returns its content. """
    with open(file_path, 'r') as file:
        content = file.read().strip()
    return content


def update_readme(theme='chartreuse-dark', owner='mriusero', base_path="./images", data_path="./data"):
    """
    Generates a README.md file with data from repositories.
        :param theme: Theme for the GitHub stats.
        :param owner: GitHub username.
        :param base_path: Path to the image directory.
        :param data_path: Path to the data directory.
    """
    readme_content = f"""# Traffic Analytics\n\n![Contributions](https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username={owner}&theme={theme})\n"""

    for repo in sorted(os.listdir(base_path)):
        repo_path = os.path.join(base_path, repo)
        if os.path.isdir(repo_path):

            visitors_graph = f"images/{repo}/visitors_graph.png"
            clones_graph = f"images/{repo}/clones_graph.png"

            readme_content += f"\n---\n## {repo}\n"
            readme_content += f'\n<img src="https://github-readme-stats.vercel.app/api/pin/?username={owner}&repo={repo}&theme={theme}" alt="Repo Citation">\n'

            readme_content += f'\n[See repo](https://github.com/{owner}/{repo})\n'

            readme_content += f'\n![Viewers Graph]({visitors_graph})\n'
            readme_content += f'\n![Clones Graph]({clones_graph})\n'

            popular_content_path = os.path.join(repo_path, "popular_content.txt")
            referring_sites_path = os.path.join(repo_path, "referring_sites.txt")

            if os.path.exists(popular_content_path):
                readme_content += f"\n{read_table_as_markdown(popular_content_path)}\n"

            if os.path.exists(referring_sites_path):
                readme_content += f"\n{read_table_as_markdown(referring_sites_path)}\n"

    with open("README.md", "w") as readme_file:
        readme_file.write(readme_content)