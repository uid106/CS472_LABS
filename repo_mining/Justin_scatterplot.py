import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.colors import to_rgba
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

# Define the path to the CSV file
CSV_FILE = 'Justin_data/Justin_authorsTouches.csv'

# Load data from CSV
data = pd.read_csv(CSV_FILE)

# Ensure the 'Date' column is in datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Extract the week number from the date
data['Week'] = data['Date'].dt.to_period('W').apply(lambda r: r.start_time)
data['Week'] = (data['Week'] - data['Week'].min()).dt.days // 7  # Convert to weeks since the start

# Map authors to colors
authors = data['Author'].unique()
colors = plt.cm.get_cmap('tab20', len(authors))  # Use a colormap with distinct colors
color_map = {author: colors(i) for i, author in enumerate(authors)}

# Create a scatter plot
plt.figure(figsize=(12, 8))

for author, color in color_map.items():
    author_data = data[data['Author'] == author]
    plt.scatter(author_data['Week'], author_data['Filename'], color=color, label=author, alpha=0.6)

# Set x-axis limits and ticks
plt.xlim(0, 250)
plt.xticks(range(0, 251, 10))  # Show ticks every 10 weeks

# Add legend
legend_elements = [Line2D([0], [0], marker='o', color='w', label=author, 
                        markerfacecolor=color_map[author], markersize=10) 
                   for author in authors]
plt.legend(handles=legend_elements, title='Authors', bbox_to_anchor=(1.05, 1), loc='upper left')

# Add labels and title
plt.xlabel('Week')
plt.ylabel('Filename')
plt.title('File Touches by Week and Author')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot
plt.savefig('Justin_data/Justin_scatterplot.png')
plt.show()

