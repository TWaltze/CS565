####
# Tyler Waltze
# 12/6/14
# CS 565
####

import json
import time

# from scikits.crab.models import MatrixPreferenceDataModel
# from scikits.crab.metrics import pearson_correlation
# from scikits.crab.similarities import UserSimilarity
# from scikits.crab.recommenders.knn import UserBasedRecommender

# import recsys.algorithm
# from recsys.algorithm.factorize import SVD
#
# recsys.algorithm.VERBOSE = True

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

# def loadData(input_file = "user-ratings.data"):
#     svd = SVD()
#     svd.load_data(filename=input_file,
#             sep='\t',
#             format={'col':0, 'row':1, 'value':2, 'ids': int})
#
#     return svd

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

    base = MAX_RATING * min(len(user1Movies), len(user2Movies))
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

    startTime = startTimer()

    best = ("U0", -1.0)
    for user in users:
        if user != u1:
            results = compareUsers(u1, user, users)

            if results["similarity"] > best[1]:
                best = (user, results["similarity"])

    endTimer(startTime, "to find nearest neighbor")

    return best

# def predict(movie, user, data = None):
#     # If database isn't already loaded into memory,
#     # load it now.
#     if data == None:
#         data = loadData()
#
#     prediction = data.predict(movie, user, MIN_RATING, MAX_RATING)
#
#     return prediction

# def recommendations(user, data = None):
#     # If user database isn't already loaded into memory,
#     # load it now.
#     if data == None:
#         data = loadUserIndex()
#
#     startTime = startTimer()
#     model = MatrixPreferenceDataModel(data)
#     endTimer(startTime, "for model")
#
#     startTime = startTimer()
#     similarity = UserSimilarity(model, pearson_correlation)
#     endTimer(startTime, "for similarity")
#
#     startTime = startTimer()
#     recommender = UserBasedRecommender(model, similarity, with_preference=True)
#     endTimer(startTime, "for recommender")
#
#     startTime = startTimer()
#     recs = recommender.recommend(user)
#     endTimer(startTime, "for recommendations")
#
#     return recs





# exec(open("analyze.py").read())

# eof
