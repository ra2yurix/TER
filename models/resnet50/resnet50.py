from pathlib import Path
import numpy as np
import time, faiss
from faiss import normalize_L2
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from PIL import Image
import tensorflow as tf
from tensorflow.python.keras.backend import set_session


class Resnet50:
    def __init__(self):

        features_path = Path(__file__).resolve().parent.parent.parent.joinpath("data/features.npy")
        y_train_path = Path(__file__).resolve().parent.parent.parent.joinpath("data/id_train.npy")
        self.features = np.load(str(features_path))
        self.y_train = np.load(str(y_train_path))

        train_features = self.features
        d = 2048  # dimension
        nb = train_features.shape[0]  # database size         # make reproducible
        normalize_L2(train_features)

        nlist = 100  # the number of cluster centers
        quantizer = faiss.IndexFlatIP(d)  # the other index

        index = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_INNER_PRODUCT)
        # by default it performs inner-product search
        assert not index.is_trained
        index.train(train_features)
        assert index.is_trained
        index.nprobe = 500  # default nprobe is 1, try a few more
        index.add(train_features)  # add may be a bit slower as well
        self.index = index
        input_tensor = Input((224, 224, 3))
        inputs = input_tensor

        global graph, sess
        graph = tf.compat.v1.get_default_graph()
        sess = tf.Session(graph=graph)
        set_session(sess)
        x = Lambda(preprocess_input)(inputs)  # the preprocess_input function varies depending on the pretrained model
        base_model = ResNet50(input_tensor=x, weights='imagenet', include_top=False)
        x = base_model(x)
        outputs = GlobalAveragePooling2D()(x)
        self.model = Model(inputs, outputs)

    def image_search(self, load_image):
        X_train = []
        img = Image.open(load_image)
        img = img.resize((224, 224))
        img = image.img_to_array(img)
        if np.shape(img)[2] == 1:
            img = np.stack((img[:, :, 0],) * 3, axis=-1)
        img = np.expand_dims(img, axis=0)
        X_train.append(img)
        with sess.as_default():
            with graph.as_default():
                set_session(sess)
                img_feature = self.model.predict(X_train)

        result = []
        k = 10
        D, I = self.index.search(img_feature, k)  # actual search

        # used to output the corresponding index and similarity
        # index is used to find the corresponding image name in y_train
        for i, d in zip(I[0], D[0]):
            print(self.y_train[i], d)
            result.append(int(self.y_train[i]))
        return result
