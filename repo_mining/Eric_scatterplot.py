import matplotlib.pyplot as plt
import csv
from datetime import datetime
import os
import random

# Function to read authors and dates from a CSV file
def read_authors_dates(file):
    authors_dates = {}
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 
        for row in reader:
            filename, author, date = row
            date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
            if filename not in authors_dates:
                authors_dates[filename] = []
            authors_dates[filename].append((author, date))
    return authors_dates

# Function to create a scatter plot
def create_plot(data, output_file):
    unique_files = list(set([item[0] for item in data]))
    file_numbering = {file: i + 1 for i, file in enumerate(unique_files)}

    unique_authors = list(set([item[1] for item in data]))

    author_colors = {}
    color_palette = ['red', 'blue', 'green', 'purple', 'black', 'orange', 'brown', 'pink', 'gray', 'yellow']

    def assign_color(author):
        if author not in author_colors:
            if len(author_colors) < len(color_palette):
                author_colors[author] = color_palette[len(author_colors) % len(color_palette)]
            else:
                # If out of predefined colors, generate random colors
                author_colors[author] = (random.random(), random.random(), random.random())
        return author_colors[author]

    x = []
    y = []
    colors = []
    start_date = min([entry[2] for entry in data])

    for filename, author, date in data:
        file_num = file_numbering[filename]
        x.append(file_num)
        week_number = (date - start_date).days // 7
        y.append(week_number)
        colors.append(assign_color(author))

    fig, ax = plt.subplots()
    scatter = ax.scatter(x, y, c=colors, marker='o', edgecolors='w', linewidth=0.5)

    # Add legend for authors
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=author_colors[author], markersize=8, label=author) for author in author_colors]
    ax.legend(handles=handles, title="Authors", bbox_to_anchor=(1, 1.1), loc='upper left')

    ax.set_xlabel('Files')
    ax.set_ylabel('Weeks')
    ax.set_title('Files touched by Authors')
    plt.tight_layout()

    plt.savefig(output_file)
    plt.show()

if __name__ == "__main__":
    csv_file = 'Eric_data/authors_dates_rootbeer.csv'
    data = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            filename, author, date = row
            data.append([filename, author, datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')])

    output_dir = 'Eric_data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, 'Eric_authorTouchesPlot.png')
    create_plot(data, output_file)
