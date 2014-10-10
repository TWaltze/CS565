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
	total = 0

	for key in author1:
		# Don't count common words
		if not isCommonWord(key):
			# Keep count of total terms found
			total += 1

			if key in author2:
				if key not in shared:
					shared.append(key)

	for key in author2:
		# Don't count common words
		if not isCommonWord(key):
			if key in author1:
				if key not in shared:
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
			if data["shared"] >= 4:
				coauthored = 1
			else:
				coauthored = 0

			prediction[edge] = coauthored

	return prediction

def isCommonWord(word):
	common_words = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount", "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as", "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]

	return word in common_words