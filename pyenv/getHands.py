import cv2
#TODO: Check if this shit is causing a memory leak:
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time
from PIL import Image
import json
import base64
from io import BytesIO
import tensorflow as tf
import tracemalloc
import gc

def getHands(img):
    gc.enable()
    np.set_printoptions(suppress=True)

    interpreter = tf.lite.Interpreter(model_path="./asl_model.tflite")
    interpreter.allocate_tensors()

    with open('debug.txt', '+a') as FO:
        FO.write("----------------------------- New Run -----------------------------\n")
    
    decoded_bytes = base64.b64decode(img)
    image_array = np.frombuffer(decoded_bytes, dtype=np.uint8)
    decoded_bytes = ""

    cap = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    image_array = ""
    # cap = cv2.imread('a1.jpg') #id number
    detector = HandDetector(maxHands=2) #for now single hand (data collection)

    offset = 0
    imgSize = 300

    tracemalloc.start()

    

    with open('./class_names.txt', 'r') as FO:
        class_names = FO.readlines()
        FO.close()

    # while cap.isOpened():
    hands,img = detector.findHands(cap)
    if hands:
        for i, hand in enumerate(hands):
            print("Run")
            with open('debug.txt', '+a') as FO:
                FO.write('-----------------------------')
            x,y,w,h = hand['bbox'] #get the bounding box
            backgroundImage = np.ones((imgSize, imgSize, 3),np.uint8)*255
            predictionBackgroundImage = np.ones((imgSize, imgSize, 3),np.uint8)*255
            
            croppedImage = img[y-offset:y+h+offset, x-offset:x+w+offset]
            # print(hand['bbox'], y-offset, x+h+offset, x-offset, x+w+offset)
            croppedPredictionImage = cap[y-offset:y+h+offset, x-offset:x+w+offset]
            
            aspectRatio = h/w
            if croppedImage.size > 0:
                newW = w
                newH = h
                wGap = 0
                hGap = 0

                if aspectRatio > 1:
                    newW = math.floor(imgSize/aspectRatio)
                    newH = imgSize
                    wGap = wGap = math.floor((imgSize-newW)/2)
                else:
                    newH = math.floor(imgSize*aspectRatio)
                    newW = imgSize
                    hGap = math.floor((imgSize-newH)/2)
                

                resizedImg = cv2.resize(croppedImage, (newW, newH))
                backgroundImage[hGap:newH+hGap, wGap:newW+wGap] = resizedImg

                resizedPredictImg = cv2.resize(croppedPredictionImage, (newW, newH))
                predictionBackgroundImage[hGap:newH+hGap, wGap:newW+wGap] = resizedPredictImg
                
                image = predictionBackgroundImage.reshape(1, 300, 300, 3)

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
                # (Your existing code for displaying text)
                cv2.putText(img, f'ASL Sign: {class_name[2:-1]} ({str(np.round(confidence_score * 100))[:-2]}%)',(x, y+h+50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,255), 2)

                # Print prediction and confidence score
                # print("Class:", class_name[2:], end="")
                # print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

                snapshot = tracemalloc.take_snapshot()
                stats = snapshot.statistics('lineno')
                with open('debug.txt', '+a') as FO:
                    for i in stats[:10]:
                        FO.write(str(i))
                        FO.write('\n\n')
                snapshot = None
                stats = None
                # class_name = None
                # confidence_score = None
                cap = None
                index = None
                output_data = None
                output_details = None
                detector = None
                interpreter = None
                image = None
                newH = None
                newW = None
                wGap = None
                hGap = None
                resizedImg = None
                image_array = None
                imgSize = None
                img = None
                image = None
                predictionBackgroundImage = None
                croppedPredictionImage = None
                resizedPredictImg = None
                input_data = None
                input_details = None
                aspectRatio = None
                decoded_bytes = None
                offset = None
                imgSize = None

                
                return (class_name, confidence_score)
    # print(hands)
    # cv2.imshow("Image", img)
    # cv2.imshow(cap)
    # cv2.waitKey(0)

