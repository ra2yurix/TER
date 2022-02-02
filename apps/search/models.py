from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex
from pathlib import Path


class SearchEngine:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client.TER
        self.collection = self.db.movie_details
        self.kw_collection = self.db.all_keywords

        movie_keywords_index_path = Path(__file__).resolve().parent.parent.parent.joinpath(
            "data/all_keywords_index.ann")
        self.movie_keywords_index = AnnoyIndex(768, "angular")
        self.movie_keywords_index.load(str(movie_keywords_index_path))

        self.bert_model = SentenceTransformer("bert-base-nli-mean-tokens")

        self.movie_keyword_ids = []
        for detail in self.collection.find():
            if len(detail["keywords"]) > 0:
                keyword_ids = []
                for keyword in detail["keywords"]:
                    keyword_ids.append(keyword["id"])
                self.movie_keyword_ids.append([detail["id"], keyword_ids])

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

        # query = text.lower()
        # query = query.translate(str.maketrans("", "", string.punctuation))
        # query = query.split()

        query_keywords = text.split(",")
        query_keyword_vectors = self.bert_model.encode(query_keywords)

        nearest_keyword_ids = set()
        for vector in query_keyword_vectors:
            nearest_keyword_ids = nearest_keyword_ids | set(self.movie_keywords_index.get_nns_by_vector(vector, 15))

        for kw in nearest_keyword_ids:
            print(self.kw_collection.find_one({"id": int(kw)}))

        common_keyword_nums = []
        for movie in self.movie_keyword_ids:
            num = len(nearest_keyword_ids.intersection(movie[1]))
            common_keyword_nums.append([movie[0], num])
        common_keyword_nums.sort(key=lambda k: k[1], reverse=True)

        for i in range(10):
            results.append(self.collection.find_one({"id": int(common_keyword_nums[i][0])}))
        return results


# test
if __name__ == "__main__":
    se = SearchEngine()
    for res in se.text_query("magic, friendship"):
        print(res['title'])
    # # se.text_query("super power,spider,marvel comic")
    #
    # for res in se.text_query("vietnam war, anti war, river, jungle"):
    #     print(res)
