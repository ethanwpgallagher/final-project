# a collation of different preprocessing techniques used over the development stages of the project

import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import numpy as np
    
# original steps
def preprocessing(img, img_size, path_needed):
    if path_needed:
        original_img = cv2.imread(img)
        img_path = "path/to/save/processed_image.jpg"
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
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

def normalisation(image):
    normalised_image = (
        image - np.min(image)) / (np.max(image) - np.min(image))
    normalised_image_uint8 = (normalised_image * 255).astype('uint8')
    return normalised_image_uint8

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

# hopeful fix using image thresholding
def hopeful_fix(img):
    picture = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blurred_picture = cv2.GaussianBlur(picture, (15,15), cv2.BORDER_DEFAULT)
    
    ret, thresh = cv2.threshold(blurred_picture, 0, 255, cv2.THRESH_OTSU)
    
    ret, markers = cv2.connectedComponents(thresh)

    marker_area = [np.sum(markers == m) for m in range(np.max(markers)+1) if m != 0]
    largest_comp = np.argmax(marker_area)+1
    mask = markers == largest_comp

    out = img.copy()
    out[mask == False] = 0

    # Enhance parts of the image where mask is True
    norm_img = normalisation(img)
    enhanced_img = cv2.addWeighted(norm_img, 4, cv2.GaussianBlur(norm_img, (0,0), 10), -4, 128)
    # Apply mask to the enhanced image
    final_img = np.where(mask[..., None], enhanced_img, out)

    return final_img
    
#all the functions below were for end of stage 1 and stage 2 of development
def kaggle_bloke_preprocessing(img_path, scale=300):
    try:
        img = cv2.imread(img_path)
        img = green_channel_extraction(img)
        img = scaleRadius(img, scale)
        img = hopeful_fix(img)
        img = cv2.GaussianBlur(img, (3,3), 0)
        img = cv2.resize(img, (224, 224))
        cv2.imwrite(img_path, img)
    except Exception as e:
        print(img_path)
        print(f'{e}')
        input()
        pass

def scaleRadius(img, scale):
    x=img[img.shape[0]//2 ,:, :].sum(1) 
    r=(x>x.mean()/10).sum()/2
    s=scale * 1.0/ r
    img = cv2.resize(img,(0,0),fx=s,fy=s)
    return img

def subtract_local_mean_colour(img, scale):
    img = cv2.addWeighted(img, 4, cv2.GaussianBlur(img, (0,0), scale/30), -4, 128)
    return img

def remove_outer_10_percent(img, scale):
    mask = np.zeros(img.shape)
    cv2.circle(mask, (img.shape[1]//2, img.shape[0]//2), int(scale*0.9), (1,1,1), -1, 8, 0)
    img = img * mask + 128 * (1-mask)
    return img

def kaggle_augment_training_image(image):
    if image is None or image.size == 0:
        return None
    # Random scaling by ±10%
    scale_factor = np.random.uniform(0.9, 1.1)
    image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)

    # Random rotation by between 0° and 360°
    angle = np.random.randint(0, 360)
    height, width = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    image = cv2.warpAffine(image, rotation_matrix, (width, height))

    # Random skewing by ±0.2
    skew_factor = np.random.uniform(-0.2, 0.2)
    skew_matrix = np.float32([[1, skew_factor, 0], [0, 1, 0]])
    image = cv2.warpAffine(image, skew_matrix, (width, height))

    if np.random.choice([True, False]):
        image = cv2.flip(image, 1)

    return image

def kaggle_augment_testing_image(image):
    # Random rotation by between 0° and 360°
    angle = np.random.randint(0, 360)
    height, width = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    image = cv2.warpAffine(image, rotation_matrix, (width, height))

    return image

# the eventual steps used for the aptos dataset, now in the notebook
def hopeful_preprocessing(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = cv2.medianBlur(img, 5)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img = clahe.apply(img)
    img = cv2.resize(img, (224,224))
    cv2.imwrite(img_path, img)