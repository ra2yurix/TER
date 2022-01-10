from pymongo import MongoClient
import json
from gensim.models import KeyedVectors
import numpy as np
import string
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

API_KEY = "26b756fc787e114571f0efbb2e62817a"


class SearchEngine:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client.TER
        # self.collection = self.db.movie_details

        self.bert_model = SentenceTransformer('bert-base-nli-mean-tokens')
        self.word2vec_model = KeyedVectors.load_word2vec_format("../../models/word2vec.vector")

        self.all_keywords = []
        self.keyword_ids = []
        for keyword in self.db.movie_keywords.find():
            self.all_keywords.append(keyword["name"])
            self.keyword_ids.append(keyword["id"])
        self.keyword_embeddings = self.bert_model.encode(self.all_keywords)
        #
        self.movie_ids_embeddings = []
        #
        # with open("../../data/movie_titles_preprocessed.txt", "r", encoding="utf-8") as f:
        #     movie_ids_titles = f.read().splitlines()
        #     for id_title in movie_ids_titles:
        #         movie_id, movie_title = id_title.split(":")
        #         try:
        #             movie_vector = np.mean(self.model[movie_title.split()], axis=0)
        #         except Exception:
        #             continue
        #         else:
        #             self.movie_ids_vectors.append([movie_id, movie_vector])

    def text_query(self, text):
        results = []

        # for res in self.db.movie_details.find({
        #     "$or": [
        #         {"title": {"$regex": text, "$options": "i"}},
        #         # {"original_title": {"$regex": text, "$options": "i"}},
        #         # {"overview": {"$regex": text, "$options": "i"}}
        #         ]}):
        #     results.append(res)
        # return results

        # query = text.lower()
        # query = query.translate(str.maketrans("", "", string.punctuation))
        # query = query.split()

        query_embedding = self.bert_model.encode(text)
        ids_cosines = []
        cosines = []
        for i in range(len(self.keyword_embeddings)):
            cosine = cosine_similarity(np.atleast_2d(query_embedding), np.atleast_2d(self.keyword_embeddings[i]))
            ids_cosines.append([self.keyword_ids[i], cosine])
        ids_cosines.sort(key=lambda k: k[1], reverse=True)
        return ids_cosines[:10]
        # query_vector = np.mean(self.model[query], axis=0)
        # cosines = []
        # for id_vector in self.movie_ids_vectors:
        #     cosine = cosine_similarity(np.atleast_2d(query_vector), np.atleast_2d(id_vector[1]))
        #     cosines.append([id_vector[0], cosine])
        # cosines.sort(key=lambda k: k[1], reverse=True)
        # for i in range(10):
        #     results.append(self.collection.find_one({"id": int(cosines[i][0])}))
        # return results


# test
if __name__ == "__main__":
    # se = SearchEngine()
    # # se.text_query("wizard magic school")
    # for m in se.text_query("wizard magic school"):
    #     print(m)


    client = MongoClient("localhost", 27017)
    c = client.TER.movie_keywords
    print(c.find_one({"id":283250}))
    # sen = [
    #     "Harry Potter and the Philosopher's Stone",
    #     "spider-man",
    #     "marvel",
    #     "magic"
    # ]
    # model = SentenceTransformer('bert-base-nli-mean-tokens')
    # # Encoding:
    # sentence_embeddings = model.encode(sen)
    # a = cosine_similarity(
    #     [sentence_embeddings[0]],
    #     sentence_embeddings[1:]
    # )
    #
    # print(a)
