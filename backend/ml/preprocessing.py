import keras
from skimage import exposure
import numpy as np

def image_to_array(image):
    image_array = keras.preprocessing.image.img_to_array(image)
    image_array = image_array.reshape((1,) + image_array.shape)
    return image_array
# resizing

def green_channel_extraction(image):
    # requires image_to_array
    green_channel_image = image[:, :, 1]
    return green_channel_image

def normalisation(image):
    datagen = keras.preprocessing.image.ImageDataGenerator(rescale=1./255, preprocessing_function=keras.applications.inception_v3.preprocess_input)
    normalised_image = datagen.flow(image).next()[0]
    return normalised_image

def histogram_equalisation(image):
    img_array_uint8 = image.astype(np.uint8)
    histogram_equalised_array = exposure.equalize_hist(img_array_uint8)
    return histogram_equalised_array

# data augmentation