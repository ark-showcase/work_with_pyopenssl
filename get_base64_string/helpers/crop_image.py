import cv2
import numpy as np

def crop_image(image_content, output_path, left, top, right, bottom):
    # Decode the image content using cv2.imdecode
    nparr = np.frombuffer(image_content, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Crop the image
    cropped_image = image[top:bottom, left:right]

    # Save the cropped image
    #cv2.imwrite(output_path, cropped_image)

    return cropped_image