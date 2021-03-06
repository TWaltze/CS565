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
            user = int(ratings.pop(0).replace("U", ""))

            movies = {}
            for rating in ratings:
                # Remove ranking wrapper
                stripped = rating.replace("(", "")
                stripped = stripped.replace(")", "")

                movie, score = stripped.split(",")

                # Remove "M" indicator to just leave int id
                movie = int(movie.replace("M", ""))


                movies[movie] = float(score)

            # Add to list of users
            processed[user] = movies

    # Encode as json for writing to new file
    encoded = json.dumps(processed)

    # Write to new file
    with open(output_file, "w") as output:
        output.write(encoded)

# Index ratings by user
def userRatingsAsCSV(input_file = "train.csv", output_file = "user-ratings.data"):
    processed = ""
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
            user = ratings.pop(0).replace("U", "")

            for rating in ratings:
                # Remove ranking wrapper
                stripped = rating.replace("(", "")
                stripped = stripped.replace(")", "")

                movie, score = stripped.split(",")

                # Remove "M" indicator to just leave int id
                movie = movie.replace("M", "")


                processed += "{}\t{}\t{}\n".format(user, movie, score)

    # Fix for weird bug that adds an extra newline between users
    processed = text = "\n".join([ll.rstrip() for ll in processed.splitlines() if ll.strip()])

    # Write to new file
    with open(output_file, "w") as output:
        output.write(processed)

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
            user = int(ratings.pop(0).replace("U", ""))

            for rating in ratings:
                # Remove ranking wrapper
                stripped = rating.replace("(", "")
                stripped = stripped.replace(")", "")

                movie, score = stripped.split(",")

                # Remove "M" indicator to just leave int id
                movie = int(movie.replace("M", ""))

                # Add the user's score to movie's total list of ratings
                if movie in processed:
                    processed[movie][user] = float(score)
                else:
                    processed[movie] = {user: score}

    # Encode as json for writing to new file
    encoded = json.dumps(processed)

    # Write to new file
    with open(output_file, "w") as output:
        output.write(encoded)

# Convert mapping to a more manageable data structure
def mapping(input_file = "mapping.csv", output_file = "mapping.json"):
    processed = {}
    with open(input_file, "r") as raw:
        # Skip first line, contains column names
        next(raw)

        for line in raw:
            # Remove extra characters
            clean = line.strip()

            # Break string into column data
            data = clean.split(",")
            # First word is an edge id
            edge_id = int(data.pop(0))
            # Second is user
            user = data.pop(0)
            # Third is movie
            movie = data.pop(0)

            # Add to list of edges.
            processed[edge_id] = [user, movie]

    # Encode as json for writing to new file
    encoded = json.dumps(processed)

    # Write to new file
    with open(output_file, "w") as output:
        output.write(encoded)

# Convert test to a more manageable data structure
def test(input_file = "test.csv", output_file = "test.json"):
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

            # Add to list of edges.
            processed[edge_id] = edge_id

    # Encode as json for writing to new file
    encoded = json.dumps(processed)

    # Write to new file
    with open(output_file, "w") as output:
        output.write(encoded)

# Convert test to a more manageable data structure
def nearest(input_file = "nearestNeighbors.data", output_file = "nearestNeighbors.json"):
    processed = {}
    with open(input_file, "r") as raw:
        for line in raw:
            # Break string into column data
            data = line.split(",")

            # First word is a user
            user = data.pop(0)
            # Second is that user's neighbor
            neighbor = data.pop(0)
            # Third is the similarity
            similarity = float(data.pop(0))

            # Add to list of edges.
            processed[user] = [neighbor, similarity]

    # Encode as json for writing to new file
    encoded = json.dumps(processed)

    # Write to new file
    with open(output_file, "w") as output:
        output.write(encoded)
