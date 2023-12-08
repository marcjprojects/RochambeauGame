import cv2
# Load the pre-trained neural network for object detection
net = cv2.dnn.readNetFromTensorflow('frozen_inference_graph.pb', 'graph.pbtxt')

# Read the input image
image = cv2.imread('marc.jpg')

# Load the background image
background = cv2.imread('streets.jpg')

# Prepare the input image for the neural network
blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104, 177, 123))

# Set the input for the neural network
net.setInput(blob)

# Run object detection to find the persons in the image
detections = net.forward()

# Loop through the detections
for i in range(detections.shape[2]):
    confidence = detections[0, 0, i, 2]
    if confidence > 0.5:  # If the confidence is high enough
        # Get the coordinates of the detected person
        box = detections[0, 0, i, 3:7] * [image.shape[1], image.shape[0], image.shape[1], image.shape[0]]
        (startX, startY, endX, endY) = box.astype("int")
        
        # Extract the person from the image
        person = image[startY:endY, startX:endX]

        # Resize the background to match the size of the person
        background_resized = cv2.resize(background, (endX - startX, endY - startY))

        # Replace the background with the new background
        image[startY:endY, startX:endX] = background_resized

# Display the modified image
cv2.imshow('Modified Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
