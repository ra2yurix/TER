import json
import string
import random

"""preprocess_keywords() -> train_word2vec() -> preprocess_titles()"""

def preprocess_keywords():
    with open("movie_keywords.txt", "r", encoding="utf-8") as f:
        keywords_lines = f.read().splitlines()

    with open("movie_details.json", "r", encoding="utf-8") as f:
        movie_details = json.load(f)
    # with open("stopwords.txt", "r", encoding="utf-8") as f:
    #     stopwords = set(f.read().splitlines())

    # new_keywords_lines = []
    # for line in keywords_lines:
    #     keywords = set(line.lower().split(" ")) - stopwords
    #     new_keywords_lines.append(" ".join(keywords) + "\n")

    new_keywords_lines = []
    for line in keywords_lines:
        line = line.lower()
        line = line.translate(str.maketrans("", "", string.punctuation))
        line = " ".join(line.split()) + "\n"
        new_keywords_lines.append(line)

    # for detail in movie_details:
    #     title = detail["title"].lower()
    #     title = title.translate(str.maketrans("", "", string.punctuation))
    #     title = " ".join(title.split()) + "\n"
    #     new_keywords_lines.append(title)

    with open("movie_keywords_preprocessed.txt", "w", newline="", encoding="utf-8") as f1:
        for _ in range(40):
            for i in range(len(new_keywords_lines)):
                words = new_keywords_lines[i].split()
                random.shuffle(words)
                new_keywords_lines[i] = " ".join(words) + "\n"
            random.shuffle(new_keywords_lines)
            f1.writelines(new_keywords_lines)
    print("Done.")


def preprocess_titles():
    with open("movie_details.json") as f:
        movie_details = json.load(f)

    with open("movie_titles_preprocessed.txt", "w", newline="", encoding="utf-8") as f:
        for detail in movie_details:
            title = detail["title"].lower()
            title = title.translate(str.maketrans("", "", string.punctuation))
            title = " ".join(title.split())
            f.write(str(detail["id"]) + ":" + title + "\n")
    print("Done.")


if __name__ == "__main__":
    # preprocess_keywords()
    preprocess_titles()
