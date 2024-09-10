import matplotlib.pyplot as plt
import csv
from datetime import datetime
import os
import matplotlib.colors as mcolors

def read_authors_dates(file):
    authors_dates = {}
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            # Skip empty rows
            if not row or all(cell == '' for cell in row):
                continue
            
            # Skip rows that don't have the required number of columns
            if len(row) != 3:
                continue
            
            filename, author, date = row
            date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
            if filename not in authors_dates:
                authors_dates[filename] = []
            authors_dates[filename].append((author, date))
    return authors_dates

def plot_scatter(authors_dates, output_path, legend_path):
    plt.figure(figsize=(12, 8))
    
    # Use a colormap with a distinct set of colors (20)
    colormap = plt.get_cmap('tab20')

    num_colors = len(colormap.colors)
    authors_colors = {}
    color_idx = 0
    
    # Create a mapping of filenames to numbers
    filenames = list(authors_dates.keys())
    filename_to_num = {filename: i+1 for i, filename in enumerate(filenames)}
    
    for filename, touches in authors_dates.items():
        weeks = [(date - min(date for _, date in touches)).days // 7 for _, date in touches]
        authors = [author for author, _ in touches]
        
        for author in set(authors):
            if author not in authors_colors:
                authors_colors[author] = colormap(color_idx % num_colors)
                color_idx += 1
        
        colors = [authors_colors[author] for author in authors]
        plt.scatter([filename_to_num[filename]] * len(weeks), weeks, c=colors, label=[author]*len(weeks), alpha=1, edgecolors='w', linewidth=0.5)

    plt.xlabel('Files')
    plt.ylabel('Weeks')
    plt.title('File Touches Over Time by Authors')
    plt.xticks(ticks=range(1, len(filenames) + 1), labels=range(1, len(filenames) + 1), rotation=0)  # Start X-axis at 1
    
    # Create a custom legend for authors
    author_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=authors_colors[author], markersize=10) for author in authors_colors]
    author_labels = list(authors_colors.keys())
    plt.legend(author_handles, author_labels, loc='upper right', bbox_to_anchor=(1.15, 1))
    
    # Save the plot as a PNG file
    plt.savefig(output_path)
    #plt.show()
    
    # Create a legend for filenames
    filename_legend = plt.figure(figsize=(12, 8))
    filename_legend.legend([plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='k', markersize=10) for _ in filenames],
                           [f"{i+1}: {filename}" for i, filename in enumerate(filenames)],
                           loc='center')
    filename_legend.savefig(legend_path)
    plt.show()

file = 'Brandon_data/authors_dates_rootbeer.csv'
authors_dates = read_authors_dates(file)

# Define the output paths for the PNG files
output_path = 'Brandon_data/scatterplot.png'
legend_path = 'Brandon_data/filename_legend.png'
plot_scatter(authors_dates, output_path, legend_path)