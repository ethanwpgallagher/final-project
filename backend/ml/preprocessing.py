import numpy as np
import matplotlib.pyplot as plt
import cv2
    
def preprocessing(img_path, img_size):
    img = cv2.imread(img_path)
    img = green_channel_extraction(img)
    img = normalisation(img)
    img = histogram_equalisation(img)
    img = resize_image_array(img, img_size)
    cv2.imwrite(img_path, img)

def green_channel_extraction(image):
    image[:,:,0] = 0
    image[:,:,2] = 0
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

def normalisation(image):
    normalised_image = cv2.normalize(image, None, 0, 1.0, cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    return normalised_image

def histogram_equalisation(image):
    if image.dtype != np.uint8:
        image = (image * 255).astype(np.uint8)
    equalised_image = cv2.equalizeHist(image)
    return equalised_image

def resize_image_array(img_array, target_size=(224, 224)):
    return cv2.resize(img_array, target_size)

def display_image(img, title):
    plt.imshow(img, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()

