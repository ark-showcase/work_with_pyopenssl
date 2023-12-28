import pytz
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from django.db.models import Q, Count, Value, Sum, Case, When, IntegerField, FloatField, ExpressionWrapper, F, CharField

import requests


import cv2
import numpy as np
from pyzbar.pyzbar import decode

from OpenSSL import SSL
import socket
from bs4 import BeautifulSoup
import base64
from PIL import Image
from io import BytesIO

import easyocr
# Create your views here.

class ExtractText(APIView):
    output_image_path = "Extract_data_from_qr_code\qr_code_images"

    def crop_image(self, image_content, output_path, left, top, right, bottom):
        # Decode the image content using cv2.imdecode
        nparr = np.frombuffer(image_content, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Crop the image
        cropped_image = image[top:bottom, left:right]

        # Save the cropped image
        cv2.imwrite(output_path, cropped_image)

        return cropped_image

    def extract_qr_code(self, image):
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

            # new data
            new_data = data.replace("ContractLanguage", "JobOfferViewer")
            # Display the data
            print(f"QR Code Data: {data}")
            print(f"QR Code Data: {new_data}")
            return data, new_data

    def get_b64_string(self, host, path):
        context = SSL.Context(SSL.TLSv1_2_METHOD)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection = SSL.Connection(context, sock)
        connection.connect((host, 443))

        html_response = ''
        try:
            request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
            connection.sendall(request.encode())

            while True:
                response = connection.recv(4096)
                if not response:
                    break
                html_response_in_line = response.decode()
                html_response = html_response + html_response_in_line

        except SSL.ZeroReturnError:
            pass
        finally:
            connection.close()

            soup = BeautifulSoup(html_response, 'html.parser')

            visa_doc_element = soup.find(id='imgLastPage')
            if visa_doc_element:
                visa_doc_b64 = visa_doc_element.get('src').replace('data:image/png;base64, ', '')
                return visa_doc_b64

        return None

    def base64_to_image(self, base64_string, save_path='visa_doc.png'):
        try:
            image_data = base64.b64decode(base64_string)

            image = Image.open(BytesIO(image_data))

            image.save(save_path)

            return image

        except Exception as e:
            print(f"Error converting Base64 to image: {e}")
            return None

    def readtext_from_base64(self, b64_string):
        # Decode the Base64 string to bytes
        image_bytes = base64.b64decode(b64_string)

        # Convert the bytes to a NumPy array
        nparr = np.frombuffer(image_bytes, np.uint8)

        # Decode the image using cv2.imdecode
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Use easyocr to read text from the image
        reader = easyocr.Reader(['en'])
        result = reader.readtext(image, detail=0)

        return result

    def post(self, request, *args, **kwargs):
        # Assuming the image is sent as part of the POST request
        image = request.FILES.get('img')  # 'img' should be the name attribute in your HTML form

        if image:
            # Read the image content from the file
            image_content = image.read()

            # Use easyocr to read text from the image
            # reader = easyocr.Reader(['en'])
            # result = reader.readtext(image_content, detail=0)
            # print(result)

            # Specify the output path for the cropped image
            output_image_path = "cropped_image.jpg"

            # Specify crop coordinates
            crop_coordinates = (0, 0, 800, 800)

            # Call the crop_image function
            cropped_img = self.crop_image(image_content, output_image_path, *crop_coordinates)

            extracted_links=self.extract_qr_code(cropped_img)

            visa_doc_b64 = self.get_b64_string("185.54.18.111", path=extracted_links[1])
            visa_doc_img = self.base64_to_image(visa_doc_b64)
            print(visa_doc_img)

            extratced_texts = self.readtext_from_base64(visa_doc_b64)

            context = {
                "visa_doc_b64": visa_doc_b64,
                "extratced_texts": extratced_texts
            }

            # return JsonResponse({'extratced_texts': extratced_texts})
            return render(request, "visa_doc_upload.html", context=context)
        else:
            return JsonResponse({'error': 'No image file provided'})

    def get(self, request):
        context = {}
        # return Response(context, status=status.HTTP_200_OK)
        return render(request, "visa_doc_upload.html", context=context)

class GetBase64String(APIView):

    def get(self, request):

        # Specify the URL you want to scrape
        url0 = 'https://www.amiprobashi.com/'
        url1 = 'https://eservices.mohre.gov.ae/molforms/JobOfferViewer.aspx?id=%2bbd42fXbhO%2bnepU%2bXYPBhQ%3d%3d'
        url2 = 'https://google.com'

        response = requests.get(url2)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the HTML element(s) you are interested in
            # For example, let's extract all the links (a elements) on the page
            links = soup.find_all('img')

            # Print or process the extracted elements
            for link in links:
                print(link)
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")

        return Response({}, status=status.HTTP_200_OK)