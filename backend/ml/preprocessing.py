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

def data_augmentation(img):
    image = cv2.imread(img)
    if image is None:
        print(img)
        print(f"Error: UNable to read the image at {img}")
    else:
        rows, cols, _ = image.shape

    rotation_angle = np.random.uniform(low=-20, high=20)
    rotation_matrix = cv2.getRotationMatrix2D((cols/2, rows/2), rotation_angle, 1)
    augmented_image = cv2.warpAffine(image, rotation_matrix, (cols, rows), borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))

    horizontal_shift = np.random.uniform(low=-0.2*cols, high=0.2*cols)
    horizontal_shift_matrix = np.float32([[1,0,horizontal_shift], [0,1,0]])
    augmented_image = cv2.warpAffine(augmented_image, horizontal_shift_matrix, (cols, rows), borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))

    vertical_shift = np.random.uniform(low=-0.2*rows, high=0.2*rows)
    vertical_shift_matrix = np.float32([[1,0,0], [0,1,vertical_shift]])
    augmented_image = cv2.warpAffine(augmented_image, vertical_shift_matrix, (cols, rows), borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))

    shear_angle = np.random.uniform(low=-20, high=20)
    shear_matrix = np.float32([[1, np.tan(np.radians(shear_angle)), 0], [0,1,0]])
    augmented_image = cv2.warpAffine(augmented_image, shear_matrix, (cols, rows), borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))

    zoom_factor = np.random.uniform(low=0.8, high=1.2)
    zoom_matrix = np.float32([[zoom_factor,0,0], [0,zoom_factor,0]])
    augmented_image = cv2.warpAffine(augmented_image, zoom_matrix, (cols, rows), borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))

    if np.random.rand() < 0.5:
        augmented_image = cv2.flip(augmented_image, 1)
    
    return augmented_image

