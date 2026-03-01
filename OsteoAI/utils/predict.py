import os
import numpy as np
from .preprocessing import load_and_preprocess, prepare_for_model

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'best_model.h5')
_cached_model = None


def load_trained_model():
    """Lazy load model to avoid TensorFlow import at startup"""
    global _cached_model
    if _cached_model is not None:
        return _cached_model
    
    try:
        from tensorflow.keras.models import load_model
    except ImportError as e:
        raise ImportError(f"TensorFlow not installed. Install with: pip install tensorflow\nError: {e}")
    
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f'Trained model not found at: {MODEL_PATH}')
    
    _cached_model = load_model(MODEL_PATH)
    return _cached_model


def predict_image(model, image_path):
    """Predict bone density category from X-ray image"""
    img = load_and_preprocess(image_path)
    batch = prepare_for_model(img)
    preds = model.predict(batch)[0]
    classes = ['Normal', 'Osteopenia', 'Osteoporosis']
    idx = np.argmax(preds)
    return classes[idx], float(preds[idx]), preds
