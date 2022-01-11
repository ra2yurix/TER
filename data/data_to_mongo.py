from pymongo import MongoClient
import json


client = MongoClient("localhost", 27017)
db = client.TER


def movie_details_to_mongo():
    with open("movie_details.json") as f:
        movie_details = json.load(f)
        db.movie_details.insert_many(movie_details)
    print("Done.")


def all_keywords_to_mongo():
    with open("all_keywords.json") as f:
        all_keywords = json.load(f)
        db.all_keywords.insert_many(all_keywords)
    print("Done.")


if __name__ == "__main__":
    movie_details_to_mongo()
    all_keywords_to_mongo()
