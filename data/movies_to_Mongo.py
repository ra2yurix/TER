from pymongo import MongoClient
import json


client = MongoClient("localhost", 27017)
db = client.TER


def movies_to_mongo():
    with open("movie_details.json") as f:
        movies = json.load(f)
        db.movies.insert_many(movies)
    print("Done.")


if __name__ == "__main__":
    movies_to_mongo()
