import numpy as np
import tensorflow as tf
from keras._tf_keras.keras.preprocessing.image import load_img, img_to_array
from app.core.config import MODEL_PATH

class MalwareDetectionModel:
    """Encapsulates model loading and prediction."""

    def __init__(self):
        self.model = tf.keras.models.load_model(MODEL_PATH)
        self.img_size = (256, 256)

    def predict_image(self, image_path: str) -> dict:
        img = load_img(image_path, target_size=self.img_size)
        img_array = img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        prediction = self.model.predict(img_array)

        predicted_class = int(prediction > 0.5) 
        label = "Malware Detected" if predicted_class== 0 else "Malware Not Detected"
        return {
            "prediction": float(prediction[0][0]),
            "predicted_class_name": label
        }
