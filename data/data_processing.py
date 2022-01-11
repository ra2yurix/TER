import json
import string
import random
from sentence_transformers import SentenceTransformer
from gensim.models import KeyedVectors
from annoy import AnnoyIndex

# def preprocess_keywords():
#     with open("movie_keywords.txt", "r", encoding="utf-8") as f:
#         keywords_lines = f.read().splitlines()
#
#     with open("movie_details.json", "r", encoding="utf-8") as f:
#         movie_details = json.load(f)
#     # with open("stopwords.txt", "r", encoding="utf-8") as f:
#     #     stopwords = set(f.read().splitlines())
#
#     # new_keywords_lines = []
#     # for line in keywords_lines:
#     #     keywords = set(line.lower().split(" ")) - stopwords
#     #     new_keywords_lines.append(" ".join(keywords) + "\n")
#
#     new_keywords_lines = []
#     for line in keywords_lines:
#         line = line.lower()
#         line = line.translate(str.maketrans("", "", string.punctuation))
#         line = " ".join(line.split()) + "\n"
#         new_keywords_lines.append(line)
#
#     # for detail in movie_details:
#     #     title = detail["title"].lower()
#     #     title = title.translate(str.maketrans("", "", string.punctuation))
#     #     title = " ".join(title.split()) + "\n"
#     #     new_keywords_lines.append(title)
#
#     with open("movie_keywords_preprocessed.txt", "w", newline="", encoding="utf-8") as f1:
#         for _ in range(40):
#             for i in range(len(new_keywords_lines)):
#                 words = new_keywords_lines[i].split()
#                 random.shuffle(words)
#                 new_keywords_lines[i] = " ".join(words) + "\n"
#             random.shuffle(new_keywords_lines)
#             f1.writelines(new_keywords_lines)
# #     print("Done.")

def keywords_output():
    all_keywords = []
    all_ids = set()
    with open("movie_details.json") as f:
        movie_details = json.load(f)
        for detail in movie_details:
            keywords = detail["keywords"]
            for keyword in keywords:
                if keyword["id"] not in all_ids:
                    all_keywords.append(keyword)
                    all_ids.add(keyword["id"])

    with open("movie_keywords.json", "w", newline="", encoding="utf-8") as f:
        json.dump(all_keywords, f, indent=4)

    print("Done.")


def ids_preprocessing():
    all_ids = []
    with open("movie_details.json") as f:
        movie_details = json.load(f)
        for detail in movie_details:
            if len(detail["keywords"]) > 0:
                ids = str(detail["id"] * 1000000)
                for keyword in detail["keywords"]:
                    ids = ids + " " + str(keyword["id"])
                ids = ids + "\n"
                all_ids.append(ids)

    with open("movie_ids_preprocessed.txt", "w", newline="", encoding="utf-8") as f:
        f.writelines(all_ids)

    print("Done.")





def movie_keyword_embedding():
    bert_model = SentenceTransformer("bert-base-nli-mean-tokens")
    annoy_movie_keywords = AnnoyIndex(768, "angular")

    with open("movie_keywords.json", "r", encoding="utf-8") as f:
        movie_keywords = json.load(f)
        for keyword in movie_keywords:
            vector = bert_model.encode(keyword["name"])
            annoy_movie_keywords.add_item(keyword["id"], vector)
    annoy_movie_keywords.build(10)
    annoy_movie_keywords.save("movie_keywords.ann")

    print("Done.")

# After training word2vec model

def movie_id_embedding():
    word2vec_model = KeyedVectors.load_word2vec_format("../models/word2vec/word2vec.vector")
    annoy_movie_ids = AnnoyIndex(100, "angular")

    with open("movie_details.json") as f:
        movie_details = json.load(f)
        for detail in movie_details:
            if len(detail["keywords"]) > 0:
                vector = word2vec_model[str(detail["id"] * 1000000)]
                annoy_movie_ids.add_item(detail["id"], vector)
    annoy_movie_ids.build(10)
    annoy_movie_ids.save("movie_ids.ann")

    print("Done.")


if __name__ == "__main__":
    # keywords_output()
    # ids_preprocessing()
    # movie_keyword_embedding()
    movie_id_embedding()

