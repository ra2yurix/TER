from pymongo import MongoClient
import urllib.parse
import urllib.request
import json

API_KEY = "26b756fc787e114571f0efbb2e62817a"


class SearchEngine:
    def __init__(self, source):
        self.source = source
        if self.source == "mongo":
            self.client = MongoClient("localhost", 27017)
            self.db = self.client.TER
            self.collection = self.db.movies

    def text_query(self, text):
        if self.source == "mongo":
            results = []
            for res in self.collection.find({
                "$or": [
                    {"title": {"$regex": text, "$options": "i"}},
                    {"original_title": {"$regex": text, "$options": "i"}},
                    {"overview": {"$regex": text, "$options": "i"}}]}):
                results.append(res)
            return results

        elif self.source == "tmdb":
            query = urllib.parse.quote(text)
            url = "https://api.themoviedb.org/3/search/movie?api_key=" + API_KEY + "&query=" + query + "&page=1"
            response = urllib.request.urlopen(url).read()
            response = json.loads(response.decode('utf-8'))
            return response["results"]


# test
if __name__ == "__main__":
    se = SearchEngine("mongo")
    for i in se.text_query("star wars"):
        print(i)

