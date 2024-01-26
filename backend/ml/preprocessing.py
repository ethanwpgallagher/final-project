from typing import Any
import numpy as np
import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import tensorflow as tf
import keras
import tensorflow_addons as tfa

class PreprocessingLayer(keras.layers.Layer):
    def call(self, xin):
        xout = self.preprocessing(xin)
        return xout
    
    def preprocessing(self, img):
        img = self.green_channel_extraction(img)
        img = self.normalisation(img)
        img = self.histogram_equalisation(img)
        img = self.resize_image_array(img)
        return img
    
    def green_channel_extraction(self, image):
        # image[:,:,0] = 0
        # image[:,:,2] = 0
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # return image
        green_channel = image[:, :, 1:2]
        zeros = tf.zeros_like(green_channel)
        modified_image = tf.concat([zeros, green_channel, zeros], axis=-1)
        return modified_image

# def normalisation(image):
#     image = image.numpy()
#     normalised_image = cv2.normalize(image, None, 0, 1.0, cv2.NORM_MINMAX, dtype=cv2.CV_32F)
#     return normalised_image

    def normalisation(self, image):
        return tf.image.per_image_standardization(image)

# def histogram_equalisation(image):
#     if image.dtype != np.uint8:
#         image = (image * 255).astype(np.uint8)
#     equalised_image = cv2.equalizeHist(image)
#     return equalised_image

    def histogram_equalisation(self, image):
        image_uint8 = tf.image.convert_image_dtype(image, tf.uint8)
        hist_equalised = tfa.image.equalize(image_uint8)
        return hist_equalised

    def resize_image_array(self, img_array, target_size=(224, 224)):
        return tf.image.resize(img_array, target_size)
        # return cv2.resize(img_array, target_size)


def display_image(img, title):
    plt.imshow(img, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()

def get_class_balance(directory):
    folder_counts = {}

    for folder_name in os.listdir(directory):
        folder_path = os.path.join(directory, folder_name)

        if os.path.isdir(folder_path):
            num_images = len([file for file in os.listdir(folder_path)])
            folder_counts[folder_name] = num_images
    labels = list(folder_counts.keys())
    counts = list(folder_counts.values())

    plt.bar(labels, counts)
    plt.xlabel('Classes')
    plt.ylabel('Num. Images')
    plt.show()
