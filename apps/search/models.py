from pymongo import MongoClient
from gensim.models import KeyedVectors
import numpy as np
import string
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex


class SearchEngine:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client.TER

        self.movie_keywords_index = AnnoyIndex(768, "angular")
        self.movie_keywords_index.load("../../data/movie_keywords.ann")

        self.movie_ids_index = AnnoyIndex(100, "angular")
        self.movie_ids_index.load("../../data/movie_ids.ann")

        self.bert_model = SentenceTransformer("bert-base-nli-mean-tokens")
        self.word2vec_model = KeyedVectors.load_word2vec_format("../../models/word2vec/word2vec.vector")

        # self.movie_keyword_embeddings = []
        # for keyword in self.db.movie_keywords.find():
        #     embedding = self.bert_model.encode(keyword["name"])
        #     self.movie_keyword_embeddings.append([keyword["id"], embedding])
        # print("movie_keyword_embeddings ready.")
        #
        # self.movie_id_embeddings = []
        # for detail in self.db.movie_details.find():
        #     if len(detail["keywords"]) > 0:
        #         embedding = self.word2vec_model["M" + str(detail["id"])]
        #         self.movie_id_embeddings.append([detail["id"], embedding])
        # print("movie_id_embeddings ready.")

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

        query_keywords = text.split(",")
        query_keyword_vectors = self.bert_model.encode(query_keywords)

        nearest_keyword_ids = []
        for vector in query_keyword_vectors:
            nearest_keyword_ids.append(str(self.movie_keywords_index.get_nns_by_vector(vector, 1)[0]))
            # keyword_cosines = []
            # for mke in self.movie_keyword_embeddings:
            #     cosine = cosine_similarity(np.atleast_2d(qke), np.atleast_2d(mke[1]))
            #     keyword_cosines.append([mke[0], cosine])
            # keyword_cosines.sort(key=lambda k: k[1], reverse=True)
            # top_keyword_ids.append(str(keyword_cosines[0][0]))
            print(self.db.movie_keywords.find_one({"id": self.movie_keywords_index.get_nns_by_vector(vector, 1)[0]}))
        print(nearest_keyword_ids)

        nearest_keyword_ids_vector = np.mean(self.word2vec_model[nearest_keyword_ids], axis=0)
        nearest_movie_ids = self.movie_ids_index.get_nns_by_vector(nearest_keyword_ids_vector, 10)
        #
        # movie_id_cosines = []
        # for embedding in self.movie_id_embeddings:
        #     cosine = cosine_similarity(np.atleast_2d(top_keyword_id_embedding), np.atleast_2d(embedding[1]))
        #     movie_id_cosines.append([embedding[0], cosine])
        # movie_id_cosines.sort(key=lambda k: k[1], reverse=True)
        #
        for i in nearest_movie_ids:
            results.append(self.db.movie_details.find_one({"id": int(i)}))
        return results


# test
if __name__ == "__main__":
    se = SearchEngine()
    for m in se.text_query("super power,spider,marvel comics"):
        print(m)
    # se.text_query("super power,spider,marvel comic")

