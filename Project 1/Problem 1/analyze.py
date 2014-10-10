import json

def loadAuthors(input_file = "features_json.txt"):
	with open(input_file, "r") as encoded:
		authors = json.loads(encoded.read())

		return authors

def loadEdges(input_file = "edges_names_json.txt"):
	with open(input_file, "r") as encoded:
		edges = json.loads(encoded.read())

		return edges

def loadTraining(input_file = "train_json.txt"):
	with open(input_file, "r") as encoded:
		coauthors = json.loads(encoded.read())

		return coauthors

def generatePrediction(output_file = "prediction.csv"):
	with open(output_file, "w") as output:
		# Generate csv headers
		output.write("id,coauthors\n")

		# Generate coauthorship predictions
		predictions = analyzeEdges()

		for prediction in predictions:
			output.write("{},{}\n".format(prediction, predictions[prediction]))

def compareAuthors(author1, author2, authors = None):
	if authors == None:
		authors = loadAuthors()

	author1 = authors[author1]
	author2 = authors[author2]

	shared = []
	total = len(author1)

	for key in author1:
		if key in author2:
			if not key in shared:
				shared.append(key)

	for key in author2:
		if key in author1:
			if not key in shared:
				shared.append(key)
		else:
			# If a new term that isn't in author1
			# is found, increase the total count
			# of terms.
			total += 1

	return {
		"author1": len(author1),
		"author2": len(author2),
		"shared": len(shared) / total * 100
	}

def analyzeEdge(edge_id, edges = None, authors = None):
	if edges == None:
		edges = loadEdges()

	edge = edges[str(edge_id)]
	author1 = edge[0]
	author2 = edge[1]

	return compareAuthors(author1, author2, authors)

def analyzeEdges():
	edges = loadEdges()
	authors = loadAuthors()

	prediction = {}
	correct = 0
	incorrect = 0
	for edge in edges:
		# Don't try to predict the first 5000 edges.
		# We were given them already to test against.
		if int(edge) > 5000:
			data = analyzeEdge(edge, edges, authors)

			# Basic prediction.
			# If authors share more than
			# 10% of the total terms between
			# them, they are coauthors
			if data["shared"] >= 10:
				coauthored = 1
			else:
				coauthored = 0

			prediction[edge] = coauthored

	return prediction

