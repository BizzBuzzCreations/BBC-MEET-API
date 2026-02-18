from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def user_create(request):
    """
    Create a new user
    Endpoint: /api/auth/create/
    Method: POST
    Body: {"username": "username", "email": "email", "password": "password"}
    Response: {"status": "201", "message": "User created successfully", "refresh": "token", "access": "token",
               "data": {
               "id": 1,
               "full_name": "full_name", 
               "username": "username", 
               "email": "email",
               "role": "role"
                }
            }
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "status": status.HTTP_201_CREATED,
            "message": "User created successfully",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "data": serializer.data
            })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """
    User login
    Endpoint: /api/auth/login/
    Method: POST
    Body: {"username": "username", "password": "password"}
    Response: {"status": "200", "message": "Login successful", "refresh": "token", "access": "token",
               "data": {"id": 1, "full_name": "full_name", "username": "username", "email": "email", "role": "role"}}
    """
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            "status": status.HTTP_200_OK,
            "message": "Login successful",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "data": UserSerializer(user).data
            })
    
    return Response({
        "status": status.HTTP_401_UNAUTHORIZED,
        "message": "Invalid credentials"
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    User profile
    Endpoint: /api/auth/profile/
    Method: GET
    Response: {"status": status.HTTP_200_OK, "message": "User profile", "data": {"id": 1, "full_name": "full_name", "username": "username", "email": "email", "role": "role"}}
    """
    return Response({
        "status": status.HTTP_200_OK,
        "message": "User profile",
        "data": UserSerializer(request.user).data
        })