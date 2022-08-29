import matplotlib.pyplot as plt
# import seaborn as sns
import keras
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Conv2D , MaxPool2D , Flatten , Dropout , BatchNormalization
from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix
from keras.callbacks import ReduceLROnPlateau
import cv2
import os
myModel = keras.models.load_model('models/history')

labels = ["new"]
img_size = 150
def get_training_data(data_dir):
    data = []
    for label in labels:
        path = os.path.join(data_dir, label)
        class_num = labels.index(label)
        for img in os.listdir(path):
            try:
                img_arr = cv2.imread(os.path.join(path, img))
                resized_arr = cv2.resize(img_arr, (img_size, img_size)) # Reshaping images to preferred size
                data.append([resized_arr, class_num])
            except Exception as e:
                print(e)
    return np.array(data)


def predict(path):
    test= get_training_data(path)

    l = []
    for i in test:
        if (i[1] == 0): l.append("Safe")
        else: l.append("Unsafe")




    x_test = []


    for feature, label in test:
        x_test.append(feature)

    x_test = np.array(x_test) / 255

    x_test = x_test.reshape(-1, img_size, img_size, 3)


    prediction = myModel.predict(x_test)
    if prediction[0][0] >= .05:
        return "Proper"
    else:
        return "Wrong" 
# print(prediction)
# if prediction[0][0] >= .7:
#   print("Proper")
# else:
#   print("Wrong")