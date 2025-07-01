from django.shortcuts import render
import json
import traceback
# import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import  TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer
from .models import  Contact, CustomUser, Contact
from .serializers import  LoginSerializer, RegisterSerializer, ContactSerializer, UserSerializer
from django.db import IntegrityError
from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes


def index(request):
    return HttpResponse("4i page wetov !")

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
class VerifyEmailView(APIView):
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        try:
            user = CustomUser.objects.get(email=email, verification_code=code)
            user.is_verified = True
            user.verification_code = None  
            user.save()
            return Response({"message": "4AK RAW SLA7."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "email or code moh sale7."}, status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token ray required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  
            return Response(
                {"message": "4AK RAW SLA7."}, 
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(
                {"error": "Invalid wala expired token"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class ContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = []