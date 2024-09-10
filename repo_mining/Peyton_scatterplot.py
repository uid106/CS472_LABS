import csv
import matplotlib.pyplot as plt
from datetime import datetime
import random

# Start Reading in Data
def readIn(path):
    # Initialize Variable
    data = []
    with open(path, 'r') as csvfile:
        # Start Reader
        reader = csv.reader(csvfile)
        # Skip Line 1
        next(reader)
        for row in reader:
            filename, author, date = row
            # String to Date & Time for "Weeks" Y axis
            data.append([filename, author, datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')])
    return data

def createPlot(data):
    # Gives Each File a Number to Reduce Plot Clutter
    totalUniqueFile = list(set([item[0] for item in data]))
    fileNumbering = {file: i + 1 for i, file in enumerate(totalUniqueFile)}

    # Find all Authors without Duplicates
    authors = list(set([item[1] for item in data]))

    # Give Unique Authors graph Coloring, Random on RGB Values
    author_colors = {author: (random.random(), random.random(), random.random()) for author in authors}

    # Prepare data for plotting
    x = []; y= []; colors = []
    startDate = min([entry[2] for entry in data])

    for filename, author, date in data:
        currFileNumber = fileNumbering[filename]
        x.append(currFileNumber)
        currWeekNumber = ((date-startDate).days // 7)
        y.append(currWeekNumber)
        currAuthor = author_colors[author]
        colors.append(currAuthor)

    # Setting Plot Parameters
    fig, ax = plt.subplots()
    scatter = ax.scatter(x, y, c=colors, marker='o')
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=author_colors[author], markersize=8, label=author) for author in authors]
    ax.legend(handles=handles, title="Authors", bbox_to_anchor=(1, 1.1), loc='upper left')
    ax.set_xlabel('File #')
    ax.set_ylabel('Weeks')
    ax.set_title('Weeks vs Unique Files by Author')
    plt.tight_layout()

    # Saving Plot
    plt.savefig('data/Peyton_authorTouchesPlot.png')
    
# Location of CSV
path = 'data/Peyton_authorsTouches.csv'

# Call function to Read Data and Process
data = readIn(path)
createPlot(data)







