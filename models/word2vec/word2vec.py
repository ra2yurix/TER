from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import multiprocessing

#
# def train_word2vec():
#     keywords_dir = "../../data/movie_ids_preprocessed.txt"
#     model_output = "word2vec.model"
#     vector_output = "word2vec.vector"
#
#     model = Word2Vec(LineSentence(keywords_dir), window=5,
#                      min_count=1, workers=multiprocessing.cpu_count(),
#                      vector_size=400, epochs=1000)
#     model.save(model_output)
#     model.wv.save_word2vec_format(vector_output, binary=False)
#
#     print("Done.")
#
#
# if __name__ == "__main__":
#     train_word2vec()


