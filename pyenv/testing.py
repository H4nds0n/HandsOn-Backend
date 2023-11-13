import cv2
import numpy as np
import base64
from io import BytesIO
import json
from getHands import getHands

# Your base64-encoded JPEG string
with open("./out.txt", "r") as FO:
    base64_jpeg_string = FO.read()

x = json.loads(base64_jpeg_string)['base64Img']
print(x.split(',')[-1])
x = x.split(',')[-1]
# # base64_jpeg_string = "your_base64_encoded_string_here"
print(getHands(x))

# # Decode base64 string to bytes
decoded_bytes = base64.b64decode(x)

# # Convert bytes to NumPy array
image_array = np.frombuffer(decoded_bytes, dtype=np.uint8)

# # Decode the image using OpenCV
image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
cv2.imshow('Decoded Image', image)
cv2.waitKey(0)



# # Now 'image' contains the decoded image, and you can use it as needed
