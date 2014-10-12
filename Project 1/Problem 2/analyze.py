import json

def loadUsers(input_file = "features_json.txt"):
	with open(input_file, "r") as encoded:
		users = json.loads(encoded.read())

		return users

def loadEdges(input_file = "edge_names_json.txt"):
	with open(input_file, "r") as encoded:
		edges = json.loads(encoded.read())

		return edges

def loadTraining(input_file = "train_json.txt"):
	with open(input_file, "r") as encoded:
		friendship = json.loads(encoded.read())

		return friendship

def generatePrediction(output_file = "prediction.csv"):
	with open(output_file, "w") as output:
		# Generate csv headers
		output.write("id,friends\n")

		# Generate coauthorship predictions
		predictions = analyzeEdges()

		for prediction in predictions:
			output.write("{},{}\n".format(prediction, predictions[prediction]))

def compareUsers(user1, user2, users = None):
	if users == None:
		users = loadUsers()

	user1 = users[user1]
	user2 = users[user2]

	shared = []
	total = 0

	for key in user1:
		# Keep count of total terms found
		total += 1

		if key in user2:
			if key not in shared:
				shared.append(key)

	for key in user2:
		if key in user1:
			if key not in shared:
				shared.append(key)
		else:
			# If a new term that isn't in author1
			# is found, increase the total count
			# of terms.
			total += 1

	return {
		"user1": len(user1),
		"user2": len(user2),
		"shared": len(shared) / total * 100 if (total > 0) else 0
	}

def analyzeEdge(edge_id, edges = None, users = None):
	if edges == None:
		edges = loadEdges()

	edge = edges[str(edge_id)]
	user1 = edge[0]
	user2 = edge[1]

	return compareUsers(user1, user2, users)

def analyzeEdges():
	edges = loadEdges()
	users = loadUsers()

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
			# 4% of the total terms between
			# them, they are coauthors
			if data["shared"] >= 4:
				friendship = 1
			else:
				friendship = 0

			prediction[edge] = friendship

	return prediction

def analyzeTest():
	edges = loadEdges()
	users = loadUsers()
	friendships = loadTraining()

	prediction = {}
	correct = 0
	incorrect = 0
	for edge in friendships:
		data = analyzeEdge(edge, edges, users)

		# Basic prediction.
		# If users are members of more than
		# 10% of the total groups between
		# them, they are friends
		if data["shared"] >= 10:
			friendship = 1
		else:
			friendship = 0

		prediction[edge] = friendship

		# Compare prediction to training
		# file with correct answer
		if friendships[edge] == friendship:
			correct += 1
		else:
			incorrect += 1

	print("Correct: {}".format(correct))
	print("Incorrect: {}".format(incorrect))

	# return prediction