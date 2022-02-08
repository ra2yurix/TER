from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex
from pathlib import Path
from models.resnet50.resnet50 import Resnet50
from collections import Counter


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
        self.resnet50 = Resnet50()

    def text_index(self, text):
        results = []

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
            results.append(int(common_keyword_nums[i][0]))
        return results

    def text_query(self, text):
        results = []
        index = self.text_index(text)
        for i in range(10):
            results.append(self.collection.find_one({"id": index[i]}))
        return results

    def image_query(self, load_image):
        results = []
        index = self.resnet50.image_search(load_image)
        for i in range(10):
            results.append(self.collection.find_one({"id": index[i]}))
        return results

    def text_image(self, text, load_image):
        results = []
        text_dic = {}
        image_dic = {}
        index_text = self.text_index(text)
        index_image = self.resnet50.image_search(load_image)
        for i in range(10):
            text_dic.update({str(index_text[i]): 10 - i})
            image_dic.update({str(index_image[i]): (10 - i) * 0.4})
        X, Y = Counter(text_dic), Counter(image_dic)
        z = dict(X + Y)
        index_res = sorted(z.items(), key=lambda x: x[1], reverse=True)
        print(index_res)
        for i in range(10):
            results.append(self.collection.find_one({"id": int(index_res[i][0])}))
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
