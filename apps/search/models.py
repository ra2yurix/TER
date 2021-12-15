from django.db import models
from pymongo import MongoClient, TEXT


class SearchEngine:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client.TER
        self.collection = self.db.movies

    def text_search(self, text):
        return self.collection.find({
            "$or": [
                {"title": {"$regex": text, "$options": "i"}},
                {"original_title": {"$regex": text, "$options": "i"}},
                {"overview": {"$regex": text, "$options": "i"}},
                {"release_date": {"$regex": text, "$options": "i"}},
            ]})


if __name__ == "__main__":
    a = SearchEngine()
    for i in a.text_search("father"):
        print(i)
