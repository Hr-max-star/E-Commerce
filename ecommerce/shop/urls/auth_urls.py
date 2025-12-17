from django.urls import path
from ..views.auth_views import AdminLoginAPIView,  RequestOtpAPIView,CustomerLoginAPIView
    
urlpatterns = [
    path("admin/login/", AdminLoginAPIView.as_view(), name="admin-login"),
    path("customer/request-otp/", RequestOtpAPIView.as_view(), name="customer-request-otp"),
    path("customer/login/", CustomerLoginAPIView.as_view(), name="customer-login"),
]
