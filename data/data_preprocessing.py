def preprocess_keywords():
    with open("movie_keywords.txt", "r", encoding="utf-8") as f:
        keywords_lines = f.read().splitlines()

    # with open("stopwords.txt", "r", encoding="utf-8") as f:
    #     stopwords = set(f.read().splitlines())

    # new_keywords_lines = []
    # for line in keywords_lines:
    #     keywords = set(line.lower().split(" ")) - stopwords
    #     new_keywords_lines.append(" ".join(keywords) + "\n")

    new_keywords_lines = [line.lower() + "\n" for line in keywords_lines]

    with open('movie_keywords_preprocessed.txt', 'w', newline='', encoding='utf-8') as f:
        f.writelines(new_keywords_lines)


if __name__ == "__main__":
    preprocess_keywords()
