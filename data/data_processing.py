import json
import string
import random
from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex


#
# def keywords_preprocessing():
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
#     print("Done.")


def all_keywords_output():
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

    with open("all_keywords.json", "w", newline="", encoding="utf-8") as f:
        json.dump(all_keywords, f, indent=4)

    print("Done.")


def all_keywords_embedding():
    bert_model = SentenceTransformer("bert-base-nli-mean-tokens")
    all_keywords_index = AnnoyIndex(768, "angular")
    with open("all_keywords.json", "r", encoding="utf-8") as f:
        all_keywords = json.load(f)
        for keyword in all_keywords:
            vector = bert_model.encode(keyword["name"])
            print(vector)
            all_keywords_index.add_item(keyword["id"], vector)
    all_keywords_index.build(10)
    all_keywords_index.save("all_keywords_index.ann")

    print("Done.")


if __name__ == "__main__":
    all_keywords_output()
    all_keywords_embedding()
