####
# Tyler Waltze
# 10/8/14
# CS 565
####

import re
import json

def features(input_file = "features.txt", output_file = "features_json.txt"):
	processed = {}
	with open(input_file, "r") as raw:
		for line in raw:
			# Remove extra "," characters
			clean = line.replace(",", "")
			clean = clean.replace("  ", " ")
			clean = clean.strip()

			# Break string into words
			words = clean.split(" ")
			# First word is always user
			user = words.pop(0)
			groups = {}

			for word in words:
				# Remove quotation marks around group id's
				group_id = word.replace('"', "")

				# Add term to terms list
				groups[group_id] = group_id

			# Add to list of authors
			processed[user] = groups

	# Encode as json for writing to new file
	encoded = json.dumps(processed)

	# Write to new file
	with open(output_file, "w") as output:
		output.write(encoded)

def edges(input_file = "edge_names.csv", output_file = "edge_names_json.txt"):
	processed = {}
	with open(input_file, "r") as raw:
		# Skip first line, contains column names
		next(raw)

		for line in raw:
			# Remove extra "," characters
			clean = line.replace(",", "")
			clean = clean.replace("  ", " ")
			clean = clean.strip()

			# Break string into column data
			data = clean.split(" ")
			# First word is an edge id
			edge_id = int(data.pop(0))
			# Second is first author
			author1 = data.pop(0)
			# Third is second author
			author2 = data.pop(0)

			# Add to list of edges.
			processed[edge_id] = [author1, author2]

	# Encode as json for writing to new file
	encoded = json.dumps(processed)

	# Write to new file
	with open(output_file, "w") as output:
		output.write(encoded)


def train(input_file = "train.csv", output_file = "train_json.txt"):
	processed = {}
	with open(input_file, "r") as raw:
		# Skip first line, contains column names
		next(raw)

		for line in raw:
			# Remove newline character
			clean = line.strip()

			# Break string into column data
			data = clean.split(",")
			# First word is an edge id
			edge_id = int(data.pop(0))
			# Second is whether or not edge
			# represents coauthors
			coauthors = int(data.pop(0))

			# Add to list of edges.
			processed[edge_id] = coauthors

	# Encode as json for writing to new file
	encoded = json.dumps(processed)

	# Write to new file
	with open(output_file, "w") as output:
		output.write(encoded)