####
# Tyler Waltze
# 10/8/14
# CS 565
####

import re
import json

#input_file = "features.txt"
#output_file = "features_json.txt"

def features(input_file = "features.txt", output_file = "features_json.txt"):
	processed = {}
	with open(input_file, "r") as raw:
		for line in raw:
			# Remove extra "," characters
			clean = line.replace(",", "")
			clean = clean.replace("  ", " ")

			# Break string into words
			words = clean.split(" ")
			# First word is always author
			author = words.pop(0)
			terms = {}

			for word in words:
				term, freq = word.split(":", 1)

				# Normalize term formatting
				term = term.lower()
				term = re.sub(r"[^a-z0-9]", "", term)

				# Clean frequency
				freq = re.sub(r"[^0-9]", "", freq)
				freq = int(freq)

				# Check for empty strings
				if term:
					if term in terms:
						# Increment if duplicate term
						terms[term] += freq
					else:
						# Add term to terms list
						terms[term] = freq

			# Add to list of authors
			processed[author] = terms

	# parsed = json.loads(processed)
	# print(json.dumps(processed, indent=4, sort_keys=True))

	# Encode as json for writing to new file
	encoded = json.dumps(processed)

	# Write to new file
	with open(output_file, "w") as output:
		output.write(encoded)

def edges(input_file = "edges_names.csv", output_file = "edges_names_json.txt"):
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