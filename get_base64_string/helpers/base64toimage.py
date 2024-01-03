import cv2
import numpy as np
import base64
from PIL import Image
from io import BytesIO

def easy_ocr_readable_image(base64_string, save_path='visa_doc.png'):
    # Decode the Base64 string to bytes
    image_bytes = base64.b64decode(base64_string)
    # image = Image.open(BytesIO(image_bytes))
    # image.save(save_path)

    # Convert the bytes to a NumPy array
    nparr = np.frombuffer(image_bytes, np.uint8)

    # Decode the image using cv2.imdecode
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image