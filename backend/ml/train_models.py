import keras

DATASET_DIRECTORY = "/Users/ethan/Downloads/diabetic-retinopathy-detection/train"

def load_dataset():
    dataset = keras.utils.image_dataset_from_directory(
        DATASET_DIRECTORY,
        labels='inferred',
        label_mode='int',
        class_names=None,
        color_mode='rgb',
        batch_size=None,
        image_size=(256, 256),
        shuffle=True
    )
    return dataset

if __name__ == "__main__":
    dataset = load_dataset()
    print(dataset)