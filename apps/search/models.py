from pymongo import MongoClient
import urllib.parse
import urllib.request
import json
from gensim.models import KeyedVectors
import numpy as np
import string
from sklearn.metrics.pairwise import cosine_similarity

API_KEY = "26b756fc787e114571f0efbb2e62817a"


class SearchEngine:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client.TER
        self.collection = self.db.movies

        self.model = KeyedVectors.load_word2vec_format("../../models/word2vec.vector")
        self.movie_ids_vectors = []

        with open("../../data/movie_titles_preprocessed.txt", "r", encoding="utf-8") as f:
            movie_ids_titles = f.read().splitlines()
            for id_title in movie_ids_titles:
                movie_id, movie_title = id_title.split(":")
                try:
                    movie_vector = np.mean(self.model[movie_title.split()], axis=0)
                except Exception:
                    continue
                else:
                    self.movie_ids_vectors.append([movie_id, movie_vector])

    def text_query(self, text):
        results = []
        # for res in self.collection.find({
        #     "$or": [
        #         {"title": {"$regex": text, "$options": "i"}},
        #         # {"original_title": {"$regex": text, "$options": "i"}},
        #         # {"overview": {"$regex": text, "$options": "i"}}
        #         ]}):
        #     results.append(res)
        # return results
        query = text.lower()
        query = query.translate(str.maketrans("", "", string.punctuation))
        query = query.split()
        query_vector = np.mean(self.model[query],axis=0)
        cosines = []
        for id_vector in self.movie_ids_vectors:
            cosine = cosine_similarity(np.atleast_2d(query_vector), np.atleast_2d(id_vector[1]))
            cosines.append([id_vector[0], cosine])
        cosines.sort(key=lambda k: k[1], reverse=True)
        for i in range(10):
            results.append(self.collection.find_one({"id": int(cosines[i][0])}))
        return results


# test
if __name__ == "__main__":
    se = SearchEngine()
    for m in se.text_query("harry potter:"):
        print(m)
