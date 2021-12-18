from pymongo import MongoClient
import urllib.parse
import urllib.request
import json

API_KEY = "26b756fc787e114571f0efbb2e62817a"


class SearchEngine:
    def __init__(self, source):
        self.source = source
        if self.source == "mongo":
            self.client = MongoClient("localhost", 27017)
            self.db = self.client.TER
            self.collection = self.db.movies

    def text_query(self, text):
        if self.source == "mongo":
            results = []
            for res in self.collection.find({
                "$or": [
                    {"title": {"$regex": text, "$options": "i"}},
                    {"original_title": {"$regex": text, "$options": "i"}},
                    {"overview": {"$regex": text, "$options": "i"}}]}):
                results.append(res)
            return results

        elif self.source == "tmdb":
            query = urllib.parse.quote(text)
            url = "https://api.themoviedb.org/3/search/movie?api_key=" + API_KEY + "&query=" + query + "&page=1"
            response = urllib.request.urlopen(url).read()
            response = json.loads(response.decode('utf-8'))
            return response["results"]


# test
if __name__ == "__main__":
    se = SearchEngine("mongo")
    for i in se.text_query("spider-man"):
        print(i)
    # text = """
    #          Peter Parker is an outcast high schooler abandoned by his parents as a boy, leaving him to be raised by his Uncle Ben and Aunt May. Like most teenagers, Peter is trying to figure out who he is and how he got to be the person he is today. As Peter discovers a mysterious briefcase that belonged to his father, he begins a quest to understand his parents' disappearance – leading him directly to Oscorp and the lab of Dr. Curt Connors, his father's former partner. As Spider-Man is set on a collision course with Connors' alter ego, The Lizard, Peter will make life-altering choices to use his powers and shape his destiny to become a hero.
    #       """
    # from sklearn.feature_extraction.text import CountVectorizer
    # import spacy
    #
    # n_gram_range = (1, 2)
    # stop_words = "english"
    #
    # # Extract candidate words/phrases
    # count = CountVectorizer(ngram_range=n_gram_range, stop_words=stop_words).fit([text])
    # all_candidates = count.get_feature_names_out()
    #
    #
    # nlp = spacy.load('en_core_web_sm')
    # doc = nlp(text)
    # noun_phrases = set(chunk.text.strip().lower() for chunk in doc.noun_chunks)
    # print(noun_phrases)
    # nouns = set()
    # for token in doc:
    #     if token.pos_ == "NOUN":
    #         nouns.add(token.text)
    # print(nouns)
    #
    # all_nouns = nouns.union(noun_phrases)
    # print(all_nouns)
    #
    # candidates = list(filter(lambda candidate: candidate in all_nouns, all_candidates))
    # print(candidates[:10])
    # print(all_candidates[:10])

