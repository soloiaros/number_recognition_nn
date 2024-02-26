import cv2
import numpy as np
import keras


def predict_number():
    # Определение объекта нейронной сети, обученной ранее
    model = keras.models.load_model('number_reco')

    img = cv2.imread('data/image.png')[:, :, 0]
    img = np.invert(np.array([img]))
    prediction = model.predict(img)
    return np.argmax(prediction)
