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

# Return an array with every user listing
# who they are friends with.
def generateFriendships():
	edges = loadEdges()
	users = loadUsers()
	friendships = loadTraining()

	userRelationships = {}
	for friendship in friendships:
		if friendships[friendship] == 1:
			user1, user2 = edges[friendship]

			# print("Edge {} between {} and {} is {}".format(friendship, user1, user2, friendships[friendship]))

			if user1 not in userRelationships: userRelationships[user1] = []
			if user2 not in userRelationships: userRelationships[user2] = []

			userRelationships[user1].append(user2)
			userRelationships[user2].append(user1)

	# print(json.dumps(userRelationships, indent=4, sort_keys=True))
	return userRelationships

# Compare two users' groups and known friends
def compareUsers(user1, user2, users = None, friendships = None):
	if users == None:
		users = loadUsers()

	if friendships == None:
		friendships = generateFriendships()

	groups = compareUsersGroups(user1, user2, users)
	friendships = compareUsersFriendships(user1, user2, friendships)

	comparision = {
		"groups": groups,
		"friendships": friendships
	}

	# print(json.dumps(comparision, indent=4, sort_keys=True))
	return comparision

def compareUsersGroups(user1, user2, users = None):
	if users == None:
		users = loadUsers()

	user1_groups = users[user1]
	user2_groups = users[user2]

	shared = []
	not_shared = []

	for key in user1_groups:
		if key in user2_groups:
			shared.append(key)
		else:
			not_shared.append(key)

	for key in user2_groups:
		if key not in user1_groups:
			not_shared.append(key)

	# Total number of groups between
	# the two users
	total = len(shared) + len(not_shared)

	return {
		"shared": {
			"list": shared,
			"total": len(shared) / total * 100 if total > 0 else 0
		},
		"not_shared": {
			"list": not_shared,
			"total": len(not_shared) / total * 100 if total > 0 else 0
		},
		"user1_group_total": len(user1_groups),
		"user2_group_total": len(user2_groups)
	}

def compareUsersFriendships(user1, user2, friendships = None):
	if friendships == None:
		friendships = generateFriendships()

	user1_friendships = []
	user2_friendships = []

	if user1 in friendships: user1_friendships = friendships[user1]
	if user2 in friendships: user2_friendships = friendships[user2]

	shared = []
	not_shared = []

	for key in user1_friendships:
		if key in user2_friendships:
			shared.append(key)
		else:
			not_shared.append(key)

	for key in user2_friendships:
		if key not in user1_friendships:
			not_shared.append(key)

	# Total number of groups between
	# the two users
	total = len(shared) + len(not_shared)

	return {
		"shared": {
			"list": shared,
			"total": len(shared) / total * 100 if total > 0 else 0
		},
		"not_shared": {
			"list": not_shared,
			"total": len(not_shared) / total * 100 if total > 0 else 0
		}
	}

def analyzeEdge(edge_id, edges = None, users = None, friendships = None):
	if edges == None:
		edges = loadEdges()

	edge = edges[str(edge_id)]
	user1 = edge[0]
	user2 = edge[1]

	return compareUsers(user1, user2, users, friendships)

def analyzeEdges():
	edges = loadEdges()
	users = loadUsers()
	friendships = generateFriendships()

	prediction = {}
	for edge in edges:
		# Don't try to predict the first 5000 edges.
		# We were given them already to test against.
		if int(edge) > 5000:
			data = analyzeEdge(edge, edges, users, friendships)

			# Basic prediction.
			# If users are members of more than
			# 15% of the total groups between
			# them, they are friends.
			if data["groups"]["not_shared"]["total"] >= 20:
				friendship = 1
			else:
				friendship = 0

			prediction[edge] = friendship

	return prediction

def analyzeTest():
	edges = loadEdges()
	users = loadUsers()
	training = loadTraining()
	friendships = generateFriendships()

	# Input to step through and test.
	#
	# Generally will be either:
	#	training = edges from train with known values
	#	edges = all edges between users
	objects_to_step_through = training

	prediction = {}
	groupless = {}
	correct = 0
	incorrect = 0
	guessed_as_friends = 0
	for edge in objects_to_step_through:
		data = analyzeEdge(edge, edges, users, friendships)

		# Basic prediction.
		# If users are members of more than
		# 15% of the total groups between
		# them, they are friends.
		#
		# OR
		#
		# Users are known friends with more
		# than 0% of the same people, they
		# are friends.
		if data["groups"]["not_shared"]["total"] > 0 and data["groups"]["not_shared"]["total"] <= 100:
			u1, u2 = edges[str(edge)]
			 # print("Users {} and {} have abnormal sharing at {}%".format(u1, u2, data["groups"]["not_shared"]["total"]))

		if data["groups"]["not_shared"]["total"] >= 15:
			friendship = 1
		else:
			friendship = 0

		prediction[edge] = friendship

		# Compare prediction to training
		# file with correct answer
		if edge in training and training[edge] == friendship:
			correct += 1
		else:
			incorrect += 1

			if friendship == 1:
				guessed_as_friends += 1

	print("Correct: {}".format(correct))
	print("Incorrect: {}".format(incorrect))
	print("Incorrectly guessed as friends: {}".format(guessed_as_friends))
	print("Incorrectly guessed as not friends: {}".format(incorrect - guessed_as_friends))

	# return prediction

def usersWhoShareFriends():
	edges = loadEdges()
	users = loadUsers()
	training = loadTraining()
	friendships = generateFriendships()

	for edge in edges:
		user1 = edges[edge][0]
		user2 = edges[edge][1]

		comparision = compareUsersFriendships(user1, user2, friendships)

		if len(comparision["shared"]) > 0: print("Users {} and {} share a friend.".format(user1, user2))

def analyzeFriendships():
	edges = loadEdges()
	users = loadUsers()
	friendships = loadTraining()

	count = 0
	groupless = {}
	grouped = {}
	for edge in friendships:
		# Edge represents a friendship
		if friendships[edge] == 1:
			# Keep a running total of how
			# many friendships exist
			count += 1

			# Get users of a friendship
			user1, user2 = edges[edge]

			user1_data = users[user1]
			user2_data = users[user2]

			if len(user1_data) == 0:
				if user1 in groupless:
					groupless[user1] += 1
				else:
					groupless[user1] = 1
			else:
				if user1 in grouped:
					grouped[user1] += 1
				else:
					grouped[user1] = 1

			if len(user2_data) == 0:
				if user2 in groupless:
					groupless[user2] += 1
				else:
					groupless[user2] = 1
			else:
				if user2 in grouped:
					grouped[user2] += 1
				else:
					grouped[user2] = 1

	print("Total friendships: {}\nTotal Groupless: {}".format(count, len(groupless)))
	return (grouped, groupless)

def analyzeNonFriendships():
	edges = loadEdges()
	users = loadUsers()
	friendships = loadTraining()

	count = 0
	groupless = {}
	grouped = {}
	for edge in friendships:
		# Edge represents a non-friendship
		if friendships[edge] == 0:
			# Keep a running total of how
			# many non-friendships exist
			count += 1

			# Get users of a non-friendship
			user1, user2 = edges[edge]

			user1_data = users[user1]
			user2_data = users[user2]

			if len(user1_data) == 0:
				if user1 in groupless:
					groupless[user1] += 1
				else:
					groupless[user1] = 1
			else:
				if user1 in grouped:
					grouped[user1] += 1
				else:
					grouped[user1] = 1

			if len(user2_data) == 0:
				if user2 in groupless:
					groupless[user2] += 1
				else:
					groupless[user2] = 1
			else:
				if user2 in grouped:
					grouped[user2] += 1
				else:
					grouped[user2] = 1

	print("Total non-friendships: {}\nTotal Groupless: {}".format(count, len(groupless)))
	return (grouped, groupless)

