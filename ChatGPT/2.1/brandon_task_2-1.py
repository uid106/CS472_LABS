import matplotlib.pyplot as plt
import csv
from datetime import datetime
import matplotlib.colors as mcolors

def read_authors_dates(file_path):
    """Reads the authors and dates from a CSV file, returning a dictionary where each
    key is a filename and the value is a list of (author, date) tuples."""
    authors_dates = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header
        
        for row in reader:
            # Skip empty rows and rows without the required number of columns
            if not row or len(row) != 3:
                continue

            filename, author, date_str = row
            date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')

            if filename not in authors_dates:
                authors_dates[filename] = []
            authors_dates[filename].append((author, date))

    return authors_dates

def assign_author_colors(authors, colormap):
    """Assigns a unique color to each author using a specified colormap."""
    num_colors = len(colormap.colors)
    author_colors = {}
    for idx, author in enumerate(authors):
        author_colors[author] = colormap(idx % num_colors)
    return author_colors

def calculate_weeks(touches):
    """Calculates the week difference between each touch date and the earliest date."""
    min_date = min(date for _, date in touches)
    weeks = [(date - min_date).days // 7 for _, date in touches]
    return weeks

def plot_scatter(authors_dates, output_path, legend_path):
    """Generates and saves a scatter plot showing file touches over time by authors."""
    plt.figure(figsize=(12, 8))
    colormap = plt.get_cmap('tab20')  # Use a distinct colormap with 20 colors

    filenames = list(authors_dates.keys())
    filename_to_num = {filename: i + 1 for i, filename in enumerate(filenames)}

    # Collect all unique authors across the dataset
    all_authors = {author for touches in authors_dates.values() for author, _ in touches}
    authors_colors = assign_author_colors(all_authors, colormap)

    # Plot the scatter points for each filename and author
    for filename, touches in authors_dates.items():
        weeks = calculate_weeks(touches)
        authors = [author for author, _ in touches]

        for author in set(authors):
            author_touch_weeks = [weeks[i] for i, auth in enumerate(authors) if auth == author]
            plt.scatter(
                [filename_to_num[filename]] * len(author_touch_weeks),
                author_touch_weeks,
                color=authors_colors[author],
                alpha=1,
                edgecolors='w',
                linewidth=0.5
            )

    plt.xlabel('Files')
    plt.ylabel('Weeks')
    plt.title('File Touches Over Time by Authors')
    plt.xticks(ticks=range(1, len(filenames) + 1), labels=range(1, len(filenames) + 1))

    # Add a legend for the authors
    author_handles = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=authors_colors[author], markersize=10)
        for author in authors_colors
    ]
    plt.legend(author_handles, list(authors_colors.keys()), loc='upper right', bbox_to_anchor=(1.15, 1))

    plt.savefig(output_path)

    # Save a separate legend for filenames
    create_filename_legend(filenames, legend_path)

    plt.show()

def create_filename_legend(filenames, legend_path):
    """Creates and saves a separate legend mapping filenames to numbers."""
    legend_fig = plt.figure(figsize=(12, 8))
    legend_fig.legend(
        [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='k', markersize=10)] * len(filenames),
        [f"{i + 1}: {filename}" for i, filename in enumerate(filenames)],
        loc='center'
    )
    legend_fig.savefig(legend_path)

# File paths for the data and output
file_path = 'Brandon_data/authors_dates_rootbeer.csv'
output_path = 'Brandon_data/scatterplot.png'
legend_path = 'Brandon_data/filename_legend.png'

# Read and plot the data
authors_dates = read_authors_dates(file_path)
plot_scatter(authors_dates, output_path, legend_path)
