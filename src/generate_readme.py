import os
import json

INITIAL_README = """
# GitHub Traffic Insights
A GitHub-Actions-based tool that allows you to easily analyze and visualize GitHub repository activity over 14 days. It processes data related to visits, clones, referring sites, and popular content, generating insightful graphs and reports to track repository performance.

---
## How to Use it

### 1. Fork or Clone this repository
> This is a public repository, so you can fork it to your own GitHub account.
> You can also clone it and create a private repository if you want to keep your data private.

The repository will contain the workflow that will be used to collect the data and generate the report.
The report will be generated in the README file and show you analytics of all the repositories you choose to analyze.

### 2. Add your GitHub Token in the repository secrets
The token is used to authenticate the GitHub API requests.
> You can create a new token by going to your GitHub account settings, then "Developer settings", then "Personal access tokens". Make sure to give it the `repo` scope.

- Go to your repository settings.
- Click on "Secrets and variables" in the left sidebar.
- Click on "Actions" under "Secrets and variables".
- Click on "New repository secret".
- Add a new secret with the name `GH_SECRET_TOKEN` and paste your GitHub token as the value.

### 3. Set up the configuration
You can configure the `theme` and `repositories` that you want to track by editing the `config.json` file. 
All themes are available in `themes.json` file, you can choose any of the themes listed there.

```json
{
  "script_to_run": "src/main.py",
  "data_dir": "./data",
  "images_dir": "./images",
  "theme": "chartreuse-dark",     # Add your favorite theme here
  "owner": "mriusero",            # Set up your GitHub username here
  "repositories": [
  "GitHub-Traffic-Insights"                 # List the repositories you want to track here
  ]
}
```

### 4. Configure the workflow (optional)
The workflow is set to run once a day. 
> You can change the schedule by editing the `cron` expression in the `.github/workflows/update_traffic_stats.yml` file.  

> You can also trigger the workflow manually by going to the "Actions" tab in your repository and clicking the "Run workflow" button.

---
## Report
The report will be generated in the `README.md` file. It will show you the following information for each repository you choose to track:
- **Repository citation card:** shows the repository with the number of stars, forks, and issues.
- **Visitors graph:** shows the number of visitors and unique visitors.
- **Clones graph:** shows the number of clones and unique clones.
- **Referring sites:** shows referring sites that led to visits to the repository.
- **Popular content:** shows the most popular content in the repository.

> For graphs, to display information over 14 days, past years data are annually, past months data are monthly, and current month data are daily. This allows to see the global trends over time.

See below an example of the report generated by the tool for this repository.

---
"""

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
    readme_content = INITIAL_README   # Comment this line to remove the initial content

    readme_content += f"""# My Repositories Analytics 👾\n\n![Contributions](https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username={owner}&theme={theme})\n"""

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