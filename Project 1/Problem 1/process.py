import json

with open("_json.txt", "r") as encoded:
	authors = json.loads(encoded.read())

	test = authors['4e3cdde62d59f8f60cf84d011f4c4f9f']

	print(json.dumps(test, indent=4, sort_keys=True))