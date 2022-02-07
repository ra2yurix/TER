from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex
from pathlib import Path
import numpy as np
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from PIL import Image
import time, faiss
from faiss import normalize_L2


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

        y_train_path = Path(__file__).resolve().parent.parent.parent.joinpath("data/id_train.npy")
        features_path = Path(__file__).resolve().parent.parent.parent.joinpath("data/features.npy")

        self.y_train = np.load(str(y_train_path))
        self.features = np.load(str(features_path))

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

    def image_query(self, load_image):
        print("image")
        results = []
        X_train = []
        img = Image.open(load_image)
        img = img.resize((224, 224))
        img = image.img_to_array(img)
        if np.shape(img)[2] == 1:
            img = np.stack((img[:, :, 0],) * 3, axis=-1)
        img = np.expand_dims(img, axis=0)
        X_train.append(img)
        input_tensor = Input((224, 224, 3))
        inputs = input_tensor

        x = Lambda(preprocess_input)(inputs)  # preprocess_input函数因预训练模型而异
        base_model = ResNet50(input_tensor=x, weights='imagenet', include_top=False)
        x = base_model(x)
        outputs = GlobalAveragePooling2D()(x)
        model = Model(inputs, outputs)

        img_feature = model.predict(X_train)

        d = 2048  # dimension
        print(self.features.shape)
        nb = self.features.shape[0]  # database size         # make reproducible
        normalize_L2(self.features)
        print(1)

        nlist = 100  # 聚类中心的个数
        k = 10  # 邻居个数  就是你想输出top几个
        quantizer = faiss.IndexFlatIP(d)  # the other index，需要以其他index作为基础
        print(2)

        index = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_INNER_PRODUCT)
        print(3)
        # by default it performs inner-product search
        assert not index.is_trained
        index.train(self.features)
        assert index.is_trained
        index.nprobe = 500  # default nprobe is 1, try a few more
        index.add(self.features)  # add may be a bit slower as well
        print(4)
        t1 = time.time()

        D, I = index.search(img_feature, k)  # actual search
        t2 = time.time()
        print('faiss kmeans result times {}'.format(t2 - t1))

        # 用来输出对应的index 和 相似度；index用来寻找 y_train中对应的 图片名称
        for i, d in zip(I[0], D[0]):
            print(self.y_train[i], d)
            results.append(self.collection.find_one({"id": int(self.y_train[i])}))

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
