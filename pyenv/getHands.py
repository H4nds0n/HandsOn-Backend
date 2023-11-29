import tensorflow as tf
from PIL import Image
import numpy as np
import math
import time
import io, base64


offset = 50
imgSize = 300


#@img: String, base64
def getHands(img): 
# Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the TensorFlow Lite model
    interpreter = tf.lite.Interpreter(model_path="./asl_model.tflite")
    interpreter.allocate_tensors()
    # Load the labels
    with open('./class_names.txt', 'r') as FO:
        class_names = FO.readlines()
    

    # print("classes: ", class_names)

    predictionBackroundImage = np.ones((imgSize, imgSize, 3), np.uint8) * 255

    # Load and resize the image
    img_data = base64.b64decode(img)
    image_stream = io.BytesIO(img_data)    
    img = Image.open(image_stream)
    img = img.resize((imgSize-1, imgSize-1))

    # Convert image to numpy array
    predictionBackroundImage[0:imgSize-1, 0:imgSize-1] = np.array(img)
    image = predictionBackroundImage.reshape(1, imgSize, imgSize, 3)

    # Prepare input tensor for inference
    input_data = (image.astype(np.float32) / 255.0)  # Normalize if necessary

    # Set input tensor
    input_details = interpreter.get_input_details()
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Run inference
    interpreter.invoke()

    # Get output tensor
    output_details = interpreter.get_output_details()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # Process output
    index = np.argmax(output_data)
    # print(f"found: {index}")
    class_name = class_names[index]
    confidence_score = output_data[0][index]

    return (class_name, confidence_score)
