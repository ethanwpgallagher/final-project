import numpy as np
import matplotlib.pyplot as plt
import cv2
    
def preprocessing(img, img_size, path_needed):
    if path_needed:
        original_img = cv2.imread(img)
        img_path = "path/to/save/processed_image.jpg"  # Modify the path as needed
        img = original_img.copy()
    else:
        img_path = None

    img = green_channel_extraction(img)
    img = normalisation(img)
    img = histogram_equalisation(img)
    img = resize_image_array(img, img_size)

    if path_needed:
        cv2.imwrite(img_path, img)
        return img_path

    return img

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

