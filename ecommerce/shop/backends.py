from django.contrib.auth.backends import ModelBackend, BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = kwargs.get("email") or username

        if email is None or password is None:
            return None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None



class MobileOTPBackend(BaseBackend):
    def authenticate(self, request, mobile_number=None, otp=None, **kwargs):
        if mobile_number is None or otp is None:
            return None
        
        try:
            user = User.objects.get(mobile_number=mobile_number)
        except User.DoesNotExist:
            return None
        if user.otp == otp:  
            return user
        
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
