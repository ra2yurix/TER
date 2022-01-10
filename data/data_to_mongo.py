from pymongo import MongoClient
import json


client = MongoClient("localhost", 27017)
db = client.TER


def movie_details_to_mongo():
    with open("movie_details.json") as f:
        movie_details = json.load(f)
        db.movie_details.insert_many(movie_details)
    print("Done.")


def movie_keywords_to_mongo():
    with open("movie_keywords.json") as f:
        movie_keywords = json.load(f)
        db.movie_keywords.insert_many(movie_keywords)
    print("Done.")


if __name__ == "__main__":
    movie_details_to_mongo()
    movie_keywords_to_mongo()
