import gensim
from gensim.models import Word2Vec, KeyedVectors
from gensim.models.word2vec import LineSentence
import multiprocessing


def train_word2vec():
    keywords_dir = "../data/movie_keywords_preprocessed.txt"
    model_output = "word2vec.model"
    vector_output = "word2vec.vector"

    model = Word2Vec(LineSentence(keywords_dir), window=5,
                     min_count=1, workers=multiprocessing.cpu_count())
    model.save(model_output)
    model.wv.save_word2vec_format(vector_output, binary=False)

    print("Done.")


if __name__ == "__main__":
    train_word2vec()

    # model = KeyedVectors.load_word2vec_format('word2vec.vector')
    # # testwords = ["war", "harry", "spider-man"]
    # # for i in testwords:
    # #     res = model.most_similar(i)
    # #     print(i)
    # #     print(res)
    # import numpy as np
    # words=["harry", "potter"]
    # print(np.mean(model[words], axis=0))
