import time
import numpy as np
import json
import requests
from io import BytesIO
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from PIL import Image

IMAGE_BASE_PATH = 'https://www.themoviedb.org/t/p/w500'


def load_train(start, end):
    with open("movie_details.json", 'r', encoding='UTF-8') as f:
        load_dict = json.load(f)
    X = []
    Y = []
    id = []
    for i in range(start, end):
        if load_dict[i]['poster_path'] is not None:
            image_path = IMAGE_BASE_PATH + load_dict[i]['poster_path']
            time.sleep(0.01)
            html = requests.get(image_path, verify=False)
            try:
                img = Image.open(BytesIO(html.content)).crop()
                img = img.resize((224, 224))
                img = image.img_to_array(img)
                if np.shape(img)[2] == 1:
                    img = np.stack((img[:, :, 0],) * 3, axis=-1)
                img = np.expand_dims(img, axis=0)

                if len(X) > 0:
                    X = np.concatenate((X, img))
                else:
                    X = img
                Y.append(i)
                id.append(load_dict[i]['id'])
            except Exception:
                print("exception")
    return X, Y, id


def train_data():
    x_train = np.load('X_train.npy')
    input_tensor = Input((224, 224, 3))
    inputs = input_tensor

    x = Lambda(preprocess_input)(inputs)
    base_model = ResNet50(input_tensor=x, weights='imagenet', include_top=False)
    x = base_model(x)
    outputs = GlobalAveragePooling2D()(x)
    model = Model(inputs, outputs)

    features = model.predict(x_train)

    print(features.shape)
    np.save('features.npy', features, allow_pickle=True)


if __name__ == "__main__":
    # because the number of data is too big,
    # it is recommended to divide into multiple saves, and then combine them
    X_train, Y_train, id_train = load_train(0, 299832)
    np.save('X_train.npy', X_train, allow_pickle=True)
    np.save('Y_train.npy', Y_train, allow_pickle=True)
    np.save('id_train.npy', id_train, allow_pickle=True)
    train_data()
