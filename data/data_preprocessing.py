import json
import string
import random


def preprocess_keywords():
    with open("movie_keywords.txt", "r", encoding="utf-8") as f:
        keywords_lines = f.read().splitlines()

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

    with open("movie_keywords_preprocessed.txt", "w", newline="", encoding="utf-8") as f:
        for _ in range(50):
            for i in range(len(new_keywords_lines)):
                words = new_keywords_lines[i].split()
                random.shuffle(words)
                new_keywords_lines[i] = " ".join(words)
            random.shuffle(new_keywords_lines)
            f.writelines(new_keywords_lines)
    print("Done.")


def preprocess_titles():
    with open("movie_details.json") as f:
        movie_details = json.load(f)

    with open("movie_titles_preprocessed.txt", "w", newline="", encoding="utf-8") as f:
        for detail in movie_details:
            title = detail["title"].lower()
            title = title.translate(str.maketrans("", "", string.punctuation))
            f.write(str(detail["id"]) + ":" + title + "\n")
    print("Done.")


if __name__ == "__main__":
    """preprocess_keywords() -> train_word2vec() -> preprocess_titles()"""
    # preprocess_keywords()
    preprocess_titles()
