####
# Tyler Waltze
# 12/6/14
# CS 565
####

import json

highestRating = 15
lowestRating = 1

allUsers = loadUserIndex()

def loadMovieIndex(input_file = "movie-ratings.json"):
    with open(input_file, "r") as encoded:
        movies = json.loads(encoded.read())

        return movies

def loadUserIndex(input_file = "user-ratings.json"):
    with open(input_file, "r") as encoded:
        users = json.loads(encoded.read())

        return users

def compareUsers(u1, u2, users = None):
    # If user database isn't already loaded into memory,
    # load it now.
    if users == None:
        users = loadUserIndex()

    # All movie scores from user1 and user2
    user1Movies = users[u1]
    user2Movies = users[u2]

    # print("movies seen by user1: {}".format(len(user1Movies)))
    # print("movies seen by user2: {}".format(len(user2Movies)))

    # Movies seen only by user1 or user2
    seenByUser1 = {}
    seenByUser2 = {}

    # Base measurement for how similar two users are.
    # The lower the number (0 to 1), the less similar.
    similarity = 1.0

    base = highestRating * min(len(user1Movies), len(user2Movies))
    normalize = similarity / base

    for movie in user1Movies:
        user1Score = float(user1Movies[movie])

        if movie in user2Movies:
            user2Score = float(user2Movies[movie])

            difference = abs(user1Score - user2Score)
            similarity -= (difference * normalize)
        else:
            seenByUser1.update({movie: user1Score})

    for movie in user2Movies:
        user2Score = float(user2Movies[movie])

        if movie not in user1Movies:
            seenByUser2.update({movie: user2Score})

    return {
        "similarity": similarity,
        "seenByUser1": len(seenByUser1),
        "seenByUser2": len(seenByUser2)
    }

def nearestNeighborTo(u1, users = None):
    # If user database isn't already loaded into memory,
    # load it now.
    if users == None:
        users = loadUserIndex()

    best = ("U0", -1.0)
    for user in users:
        if user != u1:
            results = compareUsers(u1, user, users)

            if results["similarity"] > best[1]:
                best = (user, results["similarity"])

    return best


# eof