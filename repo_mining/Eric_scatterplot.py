import matplotlib.pyplot as plt
import csv
from datetime import datetime
import os
import random

# Function to read authors and dates from a CSV file
def read_authors_dates(file):
    """Reads author, filename, and date from the provided CSV file."""
    authors_dates = []
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header
        for row in reader:
            filename, author, date_str = row
            date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            authors_dates.append([filename, author, date])
    return authors_dates

# Function to assign colors to authors
def assign_colors_to_authors(authors):
    """Assigns colors to each unique author from a predefined color palette or randomly if needed."""
    author_colors = {}
    color_palette = ['red', 'blue', 'green', 'purple', 'black', 'orange', 'brown', 'pink', 'gray', 'yellow']
    
    for author in authors:
        if len(author_colors) < len(color_palette):
            author_colors[author] = color_palette[len(author_colors)]
        else:
            # If out of predefined colors, generate random colors
            author_colors[author] = (random.random(), random.random(), random.random())
    
    return author_colors

# Function to prepare scatter plot data
def prepare_scatter_data(data, start_date, file_numbering, author_colors):
    """Prepares x, y coordinates and colors for the scatter plot based on file and author data."""
    x = []
    y = []
    colors = []
    
    for filename, author, date in data:
        file_num = file_numbering[filename]
        week_number = (date - start_date).days // 7
        x.append(file_num)
        y.append(week_number)
        colors.append(author_colors[author])
    
    return x, y, colors

# Function to create and save the scatter plot
def create_plot(data, output_file):
    """Generates a scatter plot of files touched by authors over time."""
    # Extract unique files and authors
    unique_files = list(set(item[0] for item in data))
    unique_authors = list(set(item[1] for item in data))
    
    # Map each file to a unique number
    file_numbering = {file: i + 1 for i, file in enumerate(unique_files)}
    
    # Assign colors to each author
    author_colors = assign_colors_to_authors(unique_authors)
    
    # Get the earliest date in the dataset
    start_date = min([entry[2] for entry in data])
    
    # Prepare data for the scatter plot
    x, y, colors = prepare_scatter_data(data, start_date, file_numbering, author_colors)
    
    # Create the plot
    fig, ax = plt.subplots()
    scatter = ax.scatter(x, y, c=colors, marker='o', edgecolors='w', linewidth=0.5)
    
    # Add a legend for authors
    legend_handles = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=author_colors[author], markersize=8, label=author)
        for author in author_colors
    ]
    ax.legend(handles=legend_handles, title="Authors", bbox_to_anchor=(1, 1.1), loc='upper left')
    
    # Set labels and title
    ax.set_xlabel('Files')
    ax.set_ylabel('Weeks')
    ax.set_title('Files Touched by Authors Over Time')
    
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(output_file)
    plt.show()

# Main execution
if __name__ == "__main__":
    csv_file = 'Eric_data/authors_dates_rootbeer.csv'
    
    # Read data from the CSV file
    data = read_authors_dates(csv_file)
    
    # Set the output directory and filename for the plot
    output_dir = 'Eric_data'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'Eric_authorTouchesPlot.png')
    
    # Create and save the scatter plot
    create_plot(data, output_file)
