import ast
from pathlib import Path
from pymongo import MongoClient

MOVIES_DIR = Path.cwd().joinpath('movies')
COMMENTS_DIR = Path.cwd().joinpath('comments')


client = MongoClient('localhost', 27017)
db = client.TER


def movies_to_mongo():
    for path in MOVIES_DIR.iterdir():
        f = open(path)
        movie = ast.literal_eval(f.read())
        db.movies.find_one_and_update({'title': movie['title']},
                                      {'$set': movie},
                                      upsert=True)


if __name__ == "__main__":
    movies_to_mongo()
