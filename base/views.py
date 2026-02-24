from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

# Create your views here.
@api_view(['GET'])
def home(request):
    return Response({"message": "Hello World"})
    