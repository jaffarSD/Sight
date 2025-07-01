
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import Contact
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "phone_number", "email"]
        extra_kwargs = {
            'email': {'read_only': True},
        }



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "email", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = True  
        user.verification_code = get_random_string(length=6, allowed_chars='0123456789')
        user.save()

        send_mail(
            subject="Your Verification Code",
            message=f"CODAK RA3IH: {user.verification_code}",
            from_email="noreply@iscae.com",
            recipient_list=[user.email],
        )

        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = User.objects.filter(email=data["email"]).first()
        if user and user.check_password(data["password"]):
            refresh = RefreshToken.for_user(user)
            return {"access": str(refresh.access_token), "refresh": str(refresh)}
        raise serializers.ValidationError("4AK Moh Sale7")
    
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ["id", "created_at"]