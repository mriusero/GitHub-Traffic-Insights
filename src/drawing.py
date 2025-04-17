import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
from datetime import datetime

def apply_theme(title_color, icon_color, text_color, bg_color):
    plt.rcParams.update({
        'axes.facecolor': bg_color,
        'axes.edgecolor': text_color,
        'axes.labelcolor': text_color,
        'xtick.color': text_color,
        'ytick.color': text_color,
        'text.color': text_color,
        'grid.color': text_color,
        'grid.alpha': 0.6,
        'legend.facecolor': bg_color,
        'figure.facecolor': bg_color,
    })

def plot_curves(dates, main_data, secondary_data, title, main_label, secondary_label, filename, theme='chartreuse_dark'):
    with open('themes.json', 'r') as file:
        themes = json.load(file)

    chosen_theme = themes.get(theme, 'default')

    title_color, icon_color, text_color, bg_color = (
        chosen_theme.get(key, default) for key, default in (
            ("title_color", "#2f80ed"),
            ("icon_color", "#4c71f2"),
            ("text_color", "#434d58"),
            ("bg_color", "#fffefe")
        )
    )

    apply_theme(title_color, icon_color, text_color, bg_color)

    dates = pd.to_datetime(dates)

    df = pd.DataFrame({
        'date': dates,
        'main_data': main_data,
        'secondary_data': secondary_data
    })

    df['date_only'] = df['date'].dt.date
    df_latest = df.groupby('date_only').last().reset_index()

    df_latest['delta_main_data'] = df_latest['main_data'].diff().fillna(df_latest['main_data']).astype(int)
    df_latest['delta_secondary_data'] = df_latest['secondary_data'].diff().fillna(df_latest['secondary_data']).astype(int)

    df_latest[['delta_main_data', 'delta_secondary_data']] = df_latest[['delta_main_data', 'delta_secondary_data']].clip(lower=0)

    df_latest['cumulative_main_data'] = df_latest['delta_main_data'].cumsum()
    df_latest['cumulative_secondary_data'] = df_latest['delta_secondary_data'].cumsum()

    # 1. Données annuelles des années précédentes à l'année en cours
    current_year = df_latest['date'].dt.year.max()
    previous_years_data = df_latest[df_latest['date'].dt.year < current_year].groupby(df_latest['date'].dt.year).last()

    # 2. Données mensuelles de l'année en cours et des mois précédents au mois en cours
    current_month = df_latest['date'].dt.to_period('M').max()
    current_year_data = df_latest[
        (df_latest['date'].dt.year == current_year) & (df_latest['date'].dt.to_period('M') < current_month)].groupby(
        df_latest['date'].dt.to_period('M')).last()

    # 3. Données quotidiennes du mois en cours
    current_month_data = df_latest[df_latest['date'].dt.to_period('M') == current_month]

    final_series = pd.concat([previous_years_data, current_year_data, current_month_data])

    # Final serie
    dates_latest = final_series['date']
    main_data_latest = final_series['cumulative_main_data']
    secondary_data_latest = final_series['cumulative_secondary_data']

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(range(len(dates_latest)), main_data_latest, color=title_color, marker='o', label=main_label, linewidth=2)
    ax.set_xlabel('Date')
    ax.set_ylabel(main_label, color=title_color)
    ax.tick_params(axis='y', labelcolor=title_color)

    for i, txt in enumerate(main_data_latest):
        ax.text(i, main_data_latest.iloc[i], f'{txt}', color=title_color, ha='center', va='bottom', fontsize=12,
                bbox=dict(facecolor=bg_color, edgecolor=title_color, boxstyle='round,pad=0.3'))

    ax2 = ax.twinx()
    ax2.plot(range(len(dates_latest)), secondary_data_latest, color=icon_color, marker='o', label=secondary_label, linewidth=2)
    ax2.set_ylabel(secondary_label, color=icon_color)
    ax2.tick_params(axis='y', labelcolor=icon_color)

    for i, txt in enumerate(secondary_data_latest):
        ax2.text(i, secondary_data_latest.iloc[i], f'{txt}', color=icon_color, ha='center', va='bottom',
                 fontsize=12, bbox=dict(facecolor=bg_color, edgecolor=icon_color, boxstyle='round,pad=0.3'))

    x_ticks = range(len(dates_latest))
    x_tick_labels = [
        date.strftime('%Y') if date.year < current_year else
        (date.strftime('%b %y') if date.month < current_month.month else
         date.strftime('%y/%m/%d'))
        for date in dates_latest
    ]

    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_tick_labels, rotation=45, fontsize=10)

    plt.yticks(fontsize=10)

    ax.set_title(title, fontsize=14, loc='left', color=title_color)
    ax.grid(visible=True, which='major', linestyle='--', alpha=0.5)

    main_space = 2
    secondary_space = 1

    ax.set_ylim(bottom=main_data_latest.min() - main_space, top=main_data_latest.max() + main_space)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    ax2.set_ylim(bottom=secondary_data_latest.min() - secondary_space,
                 top=secondary_data_latest.max() + secondary_space)
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close(fig)

def generate_referring_sites_text(referring_sites, filename):
    """
    Generate a Markdown table with the referring sites data.
        :param referring_sites: List of referring sites with their information.
        :param filename: Name of the file where the text will be saved.
    """
    total_count = sum(site['count'] for site in referring_sites)

    table_header = "| Referrer   | Count | Percentage (%) |"
    table_separator = "|------------|-------|----------------|"
    table_rows = []

    for site in referring_sites:
        percentage = (site['count'] / total_count) * 100
        row = f"| {site['referrer']} | {site['count']} | {percentage:.1f}% |"
        table_rows.append(row)

    table_content = f"{table_header}\n{table_separator}\n" + "\n".join(table_rows)

    with open(filename, 'w') as f:
        f.write(table_content)

def generate_popular_content_text(popular_content, filename):
    """
    Generates a Markdown table with the popular content data.
        :param popular_content: List of popular content with their information.
        :param filename: Name of the file where the text will be saved.
    """
    table_header = "| Popular Content | Path | Count | Uniques |"
    table_separator = "|--------------|------|-------|---------|"
    table_rows = []

    for content in popular_content:
        row = f"| {content['title']} | {content['path']} | {content['count']} | {content['uniques']} |"
        table_rows.append(row)

    table_content = f"{table_header}\n{table_separator}\n" + "\n".join(table_rows)

    with open(filename, 'w') as f:
        f.write(table_content)

def create_graphs_for_repo(theme, repo_name, output_dir, images_dir):
    """
    Load the repository data and generate graphs for visits and clones.
        :param theme: Theme for the graphs.
        :param repo_name: Name of the repository.
        :param output_dir: Directory where the data files are stored.
        :param images_dir: Directory where the images will be saved.
    """
    file_path = os.path.join(output_dir, f"{repo_name.replace('/', '_')}.json")

    if not os.path.exists(file_path):
        print(f"Data file for {repo_name} not found.")
        return

    with open(file_path, 'r') as f:
        data = json.load(f)

    dates = []
    views = []
    unique_visitors = []
    clones = []
    unique_cloners = []
    referring_sites = data[0].get("referring_sites", [])
    popular_content = data[0].get("popular_content", [])

    for entry in data[:]:
        date = datetime.fromisoformat(entry["timestamp"].split("T")[0])
        dates.append(date)
        views.append(entry["views"]["total"])
        unique_visitors.append(entry["views"]["unique_visitors"])
        clones.append(entry["clones"]["total"])
        unique_cloners.append(entry["clones"]["unique_cloners"])

    repo_image_dir = os.path.join(f"{images_dir}", repo_name)
    os.makedirs(repo_image_dir, exist_ok=True)

    plot_curves(
        dates,
        views,
        unique_visitors,
        title="Visitors",
        main_label="Views",
        secondary_label="Unique visitors",
        filename=os.path.join(repo_image_dir, "visitors_graph.png"),
        theme=theme,
    )

    plot_curves(
        dates,
        clones,
        unique_cloners,
        title="Git Clones",
        main_label="Clones",
        secondary_label="Unique cloners",
        filename=os.path.join(repo_image_dir, "clones_graph.png"),
        theme=theme,
    )

    if referring_sites:
        generate_referring_sites_text(
            referring_sites,
            filename=os.path.join(repo_image_dir, "referring_sites.txt")
        )

    if popular_content:
        generate_popular_content_text(
            popular_content,
            filename=os.path.join(repo_image_dir, "popular_content.txt")
        )

    print(f"... graphs updated in {repo_image_dir}.")