import cv2
import numpy as np

def crop_image_by_percentage(image_content, output_path, left_percent, top_percent, right_percent, bottom_percent):

    if type(image_content) == bytes:
        # Decode the image content using cv2.imdecode
        nparr = np.frombuffer(image_content, np.uint8)
        image_content = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Get the image dimensions
    height, width, _ = image_content.shape

    # Convert percentage values to pixel coordinates
    left = int(left_percent * width / 100)
    top = int(top_percent * height / 100)
    right = int(right_percent * width / 100)
    bottom = int(bottom_percent * height / 100)

    # Crop the image
    cropped_image = image_content[top:bottom, left:right]

    # Save the cropped image
    #cv2.imwrite(output_path, cropped_image)

    return cropped_image