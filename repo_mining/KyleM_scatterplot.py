import csv
import numpy as np
import random
from datetime import datetime
import dateutil.parser
import matplotlib.pyplot as plt
from collections import OrderedDict


filenames = []
authors = []
dates = []


def draw_scatterplot(filename, author, date):
	np.random.seed(843)

	first_commit_date = datetime.now()

	with open('KyleM_data/authorsTouches.csv', mode='r') as datafile:
		data_csv = csv.reader(datafile)
		
		header_row = next(data_csv) # skip the first line of the file, just contains header
		for line in data_csv:
			filename.append(line[0])
			author.append(line[1])
			date.append(datetime.strptime(line[2], "%Y-%m-%dT%H:%M:%SZ"))
			
			if ((datetime.strptime(line[2], "%Y-%m-%dT%H:%M:%SZ") < first_commit_date)):
				first_commit_date = datetime.strptime(line[2], "%Y-%m-%dT%H:%M:%SZ")
			
	print("first commit date: ")
	print(first_commit_date)
	
	individual_authors = []
	individual_author_colors = []
	individual_files = []
	
	for current_author in author:
		if current_author not in individual_authors:
			individual_authors.append(current_author)
			individual_author_colors.append(np.random.rand(3,))
			
	for current_file in filename:
		if current_file not in individual_files:
			individual_files.append(current_file)
	
	
	for f_idx in range(0, len(filename)):
		weeks_since_origin = int((date[f_idx] - first_commit_date).days / 7)
		file_number = individual_files.index(filename[f_idx])
		color_idx = individual_authors.index(author[f_idx])
		color = individual_author_colors[color_idx]
		plt.scatter(file_number, weeks_since_origin, c=color)
		
	ax = plt.gca()
	ax.set_xlim([0,35])
	ax.set_ylim([0, 500])
	ax.set_xlabel("File")
	ax.set_ylabel("Weeks")
	plt.savefig('KyleM_data/scatterplot.png')
	plt.show()
	plt.close()
	return
	
draw_scatterplot(filenames, authors, dates)
