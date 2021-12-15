from pymongo import MongoClient
import ast
from pathlib import Path

MOVIES_DIR = Path.cwd().joinpath('movies')
COMMENTS_DIR = Path.cwd().joinpath('comments')

host = '127.0.0.1'  # or localhost
port = 27017
client = MongoClient(host, port)
db = client.TER


def movies_to_mongo():
    for path in MOVIES_DIR.iterdir():
        f = open(path)
        movie = ast.literal_eval(f.read())
        db.movies.insert_one(movie)


if __name__ == "__main__":
    movies_to_mongo()
