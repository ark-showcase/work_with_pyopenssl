import cv2
import numpy as np
from pyzbar.pyzbar import decode

def extract_qr_code(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use the pyzbar library to decode QR codes
    qr_codes = decode(gray)

    # Iterate through the detected QR codes
    for qr_code in qr_codes:
        # Extract the data from the QR code
        data = qr_code.data.decode("utf-8")

        # Draw a rectangle around the QR code
        rect_points = qr_code.polygon
        if rect_points is not None and len(rect_points) == 4:
            rect_points = [(int(point.x), int(point.y)) for point in rect_points]
            cv2.polylines(image, [np.array(rect_points)], isClosed=True, color=(0, 255, 0), thickness=2)


        return data