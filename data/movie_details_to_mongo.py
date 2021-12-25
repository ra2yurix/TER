from pymongo import MongoClient
import json


client = MongoClient("localhost", 27017)
db = client.TER


def movie_details_to_mongo():
    with open("movie_details.json") as f:
        movie_details = json.load(f)
        db.movies.insert_many(movie_details)
    print("Done.")


if __name__ == "__main__":
    movie_details_to_mongo()
