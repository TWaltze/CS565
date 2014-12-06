####
# Tyler Waltze
# 12/6/14
# CS 565
####

import re
import json

# Index ratings by user
def userRatings(input_file = "train.csv", output_file = "user-ratings.json"):
    processed = {}
    lineNumber = 0
    with open(input_file, "r") as raw:
        for line in raw:
            lineNumber += 1
            print("line {}".format(lineNumber))

            # Remove ":" characters
            clean = line.replace(":", "")
            clean = clean.replace("  ", " ")

            # Break string into ratings
            ratings = clean.split(" ")

            # First word is always user
            user = ratings.pop(0)

            movies = {}
            for rating in ratings:
                # Remove ranking wrapper
                stripped = rating.replace("(", "")
                stripped = stripped.replace(")", "")

                movie, score = stripped.split(",")


                movies[movie] = score

            # Add to list of users
            processed[user] = movies

    # Encode as json for writing to new file
    encoded = json.dumps(processed)

    # Write to new file
    with open(output_file, "w") as output:
        output.write(encoded)

# Index ratings by movie
def movieRatings(input_file = "train.csv", output_file = "movie-ratings.json"):
    processed = {}
    lineNumber = 0
    with open(input_file, "r") as raw:
        for line in raw:
            lineNumber += 1
            print("line {}".format(lineNumber))

            # Remove ":" characters
            clean = line.replace(":", "")
            clean = clean.replace("  ", " ")

            # Break string into ratings
            ratings = clean.split(" ")

            # First word is always user
            user = ratings.pop(0)

            for rating in ratings:
                # Remove ranking wrapper
                stripped = rating.replace("(", "")
                stripped = stripped.replace(")", "")

                movie, score = stripped.split(",")

                # Add the user's score to movie's total list of ratings
                if movie in processed:
                    processed[movie][user] = score
                else:
                    processed[movie] = {user: score}

    # Encode as json for writing to new file
    encoded = json.dumps(processed)

    # Write to new file
    with open(output_file, "w") as output:
        output.write(encoded)
