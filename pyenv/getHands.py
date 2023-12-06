import cv2
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

class Hands():
    def __init__(self):
        np.set_printoptions(suppress=True)
        with open('./class_names.txt', 'r') as FO:
            self.class_names = FO.readlines()
            FO.close()

        with open('debug.txt', '+a') as FO:
            FO.write("----------------------------- New Run -----------------------------\n")

        self.interpreter = tf.lite.Interpreter(model_path="./asl_model.tflite")
        self.interpreter.allocate_tensors()


        self.offset = 0
        self.imgSize = 300

        self.detector = HandDetector(maxHands=2)
    



    def getHands(self, img):
        #for now single hand (data collection)

        decoded_bytes = base64.b64decode(img)
        image_array = np.frombuffer(decoded_bytes, dtype=np.uint8)
        decoded_bytes = "" 

        cap = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        image_array = ""
        # cap = cv2.imread('a1.jpg') #id number

        tracemalloc.start()

        # while cap.isOpened():
        hands,img = self.detector.findHands(cap)
        if hands:
            for i, hand in enumerate(hands):
                print("Run")
                with open('debug.txt', '+a') as FO:
                    FO.write('-----------------------------')
                x,y,w,h = hand['bbox'] #get the bounding box
                backgroundImage = np.ones((self.imgSize, self.imgSize, 3),np.uint8)*255
                predictionBackgroundImage = np.ones((self.imgSize, self.imgSize, 3),np.uint8)*255
                
                croppedImage = img[y-self.offset:y+h+self.offset, x-self.offset:x+w+self.offset]
                # print(hand['bbox'], y-offset, x+h+offset, x-offset, x+w+offset)
                croppedPredictionImage = cap[y-self.offset:y+h+self.offset, x-self.offset:x+w+self.offset]
                
                aspectRatio = h/w
                if croppedImage.size > 0:
                    newW = w
                    newH = h
                    wGap = 0
                    hGap = 0

                    if aspectRatio > 1:
                        newW = math.floor(self.imgSize/aspectRatio)
                        newH = self.imgSize
                        wGap = wGap = math.floor((self.imgSize-newW)/2)
                    else:
                        newH = math.floor(self.imgSize*aspectRatio)
                        newW = self.imgSize
                        hGap = math.floor((self.imgSize-newH)/2)
                    

                    resizedImg = cv2.resize(croppedImage, (newW, newH))
                    backgroundImage[hGap:newH+hGap, wGap:newW+wGap] = resizedImg

                    resizedPredictImg = cv2.resize(croppedPredictionImage, (newW, newH))
                    predictionBackgroundImage[hGap:newH+hGap, wGap:newW+wGap] = resizedPredictImg
                    
                    image = predictionBackgroundImage.reshape(1, 300, 300, 3)

                    # Prepare input tensor for inference
                    input_data = (image.astype(np.float32) / 255.0)  # Normalize if necessary

                    # Set input tensor
                    input_details = self.interpreter.get_input_details()
                    self.interpreter.set_tensor(input_details[0]['index'], input_data)

                    # Run inference
                    self.interpreter.invoke()

                    # Get output tensor
                    output_details = self.interpreter.get_output_details()
                    output_data = self.interpreter.get_tensor(output_details[0]['index'])

                    # Process output
                    index = np.argmax(output_data)
                    # print(f"found: {index}")
                    class_name = self.class_names[index]
                    confidence_score = output_data[0][index]
                    # (Your existing code for displaying text)
                    cv2.putText(img, f'ASL Sign: {class_name[2:-1]} ({str(np.round(confidence_score * 100))[:-2]}%)',(x, y+h+50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,255), 2)

                    # Print prediction and confidence score
                    # print("Class:", class_name[2:], end="")
                    # print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

                    snapshot = tracemalloc.take_snapshot()

                    traces = snapshot.statistics('traceback')
                    multi_allocated = [stat for stat in traces if stat.count == 1]

                    # Print information about objects allocated multiple times
                    
                    stats = snapshot.statistics('lineno')
                    with open('debug.txt', '+a') as FO:
                        for stat in multi_allocated:
                            if stat.count > 1:
                                FO.write(f"Traceback: {stat.traceback[0]} | Objects allocated: {stat.count}")
                                FO.write('-----------\n\n')
                  
                    tracemalloc.stop()

                    
                    return (class_name, confidence_score)
    # print(hands)
    # cv2.imshow("Image", img)
    # cv2.imshow(cap)
    # cv2.waitKey(0)

