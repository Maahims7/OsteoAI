import cv2
import numpy as np

IMG_SIZE = (224, 224)


def load_and_preprocess(image_path):
    """Read image from path, convert to RGB, resize and scale to [0,1]"""
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, IMG_SIZE)
    img = img.astype('float32') / 255.0
    return img


def prepare_for_model(img_array):
    """Expand dims to form batch"""
    return np.expand_dims(img_array, axis=0)
