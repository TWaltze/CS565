####
# Tyler Waltze
# 12/6/14
# CS 565
####

import json
import time

MAX_RATING = 15
MIN_RATING = 1

def startTimer():
    return time.time()

def endTimer(start, task):
    print("--- {} seconds {} ---".format(time.time() - start, task))

def loadMovieIndex(input_file = "movie-ratings.json"):
    with open(input_file, "r") as encoded:
        movies = json.loads(encoded.read())

        return movies

def loadUserIndex(input_file = "user-ratings.json"):
    startTime = startTimer()

    with open(input_file, "r") as encoded:
        users = json.loads(encoded.read())

        endTimer(startTime, "to load from json")

        return users

def loadMapping(input_file = "mapping.json"):
    with open(input_file, "r") as encoded:
        edges = json.loads(encoded.read())

        return edges

def compareUsers(u1, u2, users = None):
    # If user database isn't already loaded into memory,
    # load it now.
    if users == None:
        users = loadUserIndex()

    # All movie scores from user1 and user2
    user1Movies = users[u1]
    user2Movies = users[u2]

    # Base measurement for how similar two users are.
    # The lower the number (0 to 1), the less similar.
    similarity = 1.0

    base = MAX_RATING * min(len(user1Movies), len(user2Movies))
    normalize = similarity / base

    difference = sum([
        abs(float(user1Movies[movie]) - float(user2Movies[movie])) * normalize
        for movie in user1Movies if movie in user2Movies
    ])

    similarity -= difference

    return similarity

def nearestNeighborTo(u1, users = None):
    # If user database isn't already loaded into memory,
    # load it now.
    if users == None:
        users = loadUserIndex()

    # startTime = startTimer()

    best = max([
        (compareUsers(u1, user, users), user)
        for user in users if user != u1
    ])

    # endTimer(startTime, "to find nearest neighbor with list")

    return best # (similarity, nearestUser)

def calculateNearestNeighbors(output_file = "nearestNeighbors.data"):
    users = loadUserIndex()

    startTime = startTimer()

    nearest = [(user, nearestNeighborTo(user, users)) for user in users]

    endTimer(startTime, "to find nearest neighbors")

    with open(output_file, "w") as output:
        for pair in nearest:
            user = pair[0]
            neighbor = pair[1][1]
            distance = pair[1][0]

            output.write("{},{},{}\n".format(user, neighbor, distance))

def nearestNeighborFromSubsetTo(u1, subset, users = None):
    # If user database isn't already loaded into memory,
    # load it now.
    if users == None:
        users = loadUserIndex()

    # startTime = startTimer()

    best = max([
        (compareUsers(u1, user, users), user)
        for user in subset if user != u1
    ])

    # endTimer(startTime, "to find nearest neighbor with list")

    return best # (similarity, nearestUser)

def calculateNearestNeighborsFromMapping(output_file = "nearestNeighborsSubset.data"):
    users = loadUserIndex()
    movies = loadMovieIndex()
    edges = loadMapping()

    startTime = startTimer()

    nearest = {}
    for edge in edges:
        user, movie = edges[edge]

        neighbor = nearestNeighborFromSubsetTo(user, movies[movie], users)[1]

        data = {
            user: neighbor
        }

        if movie in nearest:
            nearest[movie].update(data)
        else:
            nearest[movie] = data

    endTimer(startTime, "to find nearest neighbors")

    # Encode as json for writing to new file
    encoded = json.dumps(nearest)

    # Write to new file
    with open(output_file, "w") as output:
        output.write(encoded)




# exec(open("analyze.py").read())

# eof
