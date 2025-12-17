
from django.urls import path
from ..views.order_flow_view import OrderFlowAPIView

urlpatterns = [
    path("flow/", OrderFlowAPIView.as_view(), name="order-flow"),
]
