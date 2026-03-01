import os
import cv2
import numpy as np

# Lazy import TensorFlow to prevent startup issues
_tf_available = False
_tf = None

def _get_tensorflow():
    """Get TensorFlow module, lazy loading on first use"""
    global _tf, _tf_available
    if _tf is not None:
        return _tf
    
    try:
        import tensorflow as tf
        _tf = tf
        _tf_available = True
        return tf
    except ImportError:
        _tf_available = False
        raise ImportError("TensorFlow not installed. Install with: pip install tensorflow")

def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    """Generate Grad-CAM heatmap for model interpretability"""
    tf = _get_tensorflow()
    
    # Create a model that maps the input image to the activations
    # of the last conv layer as well as the output predictions
    grad_model = tf.keras.models.Model(
        [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
    )

    # Compute the gradient of the top predicted class for our input image
    # with respect to the activations of the last conv layer
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(predictions[0])
        class_channel = predictions[:, pred_index]

    # This is the gradient of the output neuron (top predicted or chosen)
    # with regard to the output feature map of the last conv layer
    grads = tape.gradient(class_channel, conv_outputs)

    # Pool the gradients over all the axes leaving out the channel dimension
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # We multiply each channel in the feature map array by
    # "how important this channel is" with regard to the top predicted class
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # For visualization purpose, normalize the heatmap between 0 & 1
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()


def save_and_overlay_heatmap(img_path, heatmap, output_path, alpha=0.4):
    """Overlay Grad-CAM heatmap on original image and save"""
    try:
        # Load the original image
        img = cv2.imread(img_path)
        if img is None:
            raise FileNotFoundError(f"Could not read image: {img_path}")
            
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)

        # resize to match
        heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))

        superimposed = heatmap * alpha + img
        superimposed = np.uint8(superimposed)

        # Create output directory if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save to disk
        cv2.imwrite(output_path, cv2.cvtColor(superimposed, cv2.COLOR_RGB2BGR))
    except Exception as e:
        print(f"Error saving heatmap: {e}")
        raise


def generate_gradcam(image_path, model, last_conv_layer_name='Conv_1'):
    """Generate and return Grad-CAM heatmap for given image"""
    from .preprocessing import load_and_preprocess, prepare_for_model
    img = load_and_preprocess(image_path)
    batch = prepare_for_model(img)
    heatmap = make_gradcam_heatmap(batch, model, last_conv_layer_name)
    return heatmap
