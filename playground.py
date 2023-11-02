import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Load a pre-trained object detection model from TensorFlow Hub
model_url = "https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2"
model = hub.load(model_url).signatures['default']

# Load and preprocess the input image
image_path = 'streets.jpg'
image = Image.open(image_path)
image = np.array(image)
input_image = image[np.newaxis, ...]

# Perform object detection
result = model(tf.convert_to_tensor(input_image))

# Get the detected objects and their scores
boxes = result['detection_boxes'][0].numpy()
scores = result['detection_scores'][0].numpy()

# Threshold for considering a detection as valid
threshold = 0.5
detected_boxes = boxes[scores >= threshold]

# Draw bounding boxes on the original image
for box in detected_boxes:
    ymin, xmin, ymax, xmax = box
    xmin = int(xmin * image.shape[1])
    xmax = int(xmax * image.shape[1])
    ymin = int(ymin * image.shape[0])
    ymax = int(ymax * image.shape[0])
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)

# Display the resulting image with bounding boxes
plt.imshow(image)
plt.show()
