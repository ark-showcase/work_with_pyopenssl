import pytz
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from django.db.models import Q, Count, Value, Sum, Case, When, IntegerField, FloatField, ExpressionWrapper, F, CharField

import requests
import ssl

import easyocr
from bs4 import BeautifulSoup

# Create your views here.

class ExtractText(APIView):

    def post(self, request):
        image = request.FILES.get('img')
        image_content = image.read()
        reader = easyocr.Reader(['en'])
        result = reader.readtext(image_content, detail=0)
        context = {
            'hello_world': result
        }
        return Response(context, status=status.HTTP_200_OK)

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