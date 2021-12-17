from pymongo import MongoClient


class SearchEngine:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client.TER
        self.collection = self.db.movies

    def text_query(self, text):
        result = []
        for res in self.collection.find({
            "$or": [
                {"title": {"$regex": text, "$options": "i"}},
                {"original_title": {"$regex": text, "$options": "i"}},
                {"overview": {"$regex": text, "$options": "i"}}]}):
            result.append(res)
        return result


# test
if __name__ == "__main__":
    se = SearchEngine()
    for i in se.text_query("star wars"):
        print(i)
