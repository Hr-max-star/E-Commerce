from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
import random

from ..serializers import *
from ..models import CustomUser


class AdminLoginAPIView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "message": "Admin login successful",
            "token": token.key,
            "email": user.email,
        }, status=status.HTTP_200_OK)


class RequestOtpAPIView(APIView):
    def post(self, request):
        serializer = RequestOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile_number"]
        user, created = CustomUser.objects.get_or_create(
            mobile_number=mobile,
            defaults={
                "email": f"{mobile}@temp.com",
                "is_customer": True,
                "is_active": True
            }
        )

        otp = str(random.randint(1000, 9999))
        user.otp = otp
        user.save(update_fields=["otp"])

        return Response({
            "message": "OTP sent successfully",
            "mobile_number": mobile, 
            "otp": otp, 
        }, status=status.HTTP_200_OK)


class CustomerLoginAPIView(APIView):
    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        user.otp = ""
        user.save(update_fields=["otp"])

        return Response({
            "message": "Customer login successful",
            "token": token.key,
            "user_id": str(user.id),
            "mobile_number": user.mobile_number,
        }, status=status.HTTP_200_OK)
