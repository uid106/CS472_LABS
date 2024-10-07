import csv
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from collections import OrderedDict


def draw_scatterplot(file_path):
    np.random.seed(843)

    # Read data and extract information from CSV
    with open(file_path, mode='r') as datafile:
        data_csv = csv.reader(datafile)
        next(data_csv)  # Skip header

        data = [(line[0], line[1], datetime.strptime(line[2], "%Y-%m-%dT%H:%M:%SZ")) for line in data_csv]

    # Extract unique authors and files
    filenames = list(OrderedDict.fromkeys([line[0] for line in data]))
    authors = list(OrderedDict.fromkeys([line[1] for line in data]))

    # Create color map for authors
    author_colors = {author: np.random.rand(3,) for author in authors}

    # Determine the date of the first commit
    first_commit_date = min(line[2] for line in data)

    # Create scatter plot
    for filename, author, commit_date in data:
        weeks_since_origin = (commit_date - first_commit_date).days // 7
        file_index = filenames.index(filename)
        plt.scatter(file_index, weeks_since_origin, c=[author_colors[author]])

    # Customize plot
    plt.xlim([0, len(filenames)])
    plt.ylim([0, 500])
    plt.xlabel("File")
    plt.ylabel("Weeks")
    
    # Save and show plot
    plt.savefig('KyleM_data/scatterplot.png')
    plt.show()
    plt.close()


# Call function with file path
draw_scatterplot('KyleM_data/authorsTouches.csv')
