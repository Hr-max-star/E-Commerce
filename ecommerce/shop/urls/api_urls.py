
from rest_framework.routers import DefaultRouter
from django.urls import path, include

from ..views.api_views import (
    StoreViewSet,
    CategoryViewSet,
    SubcategoryViewSet,
    ProductViewSet,
    ProductImageViewSet,
    OrderViewSet,
    OrderDetailViewSet,
    PaymentViewSet,
    InvoiceViewSet,
    AddressViewSet,
    CouponViewSet,
    AuditLogViewSet,
)

from ..views.auth_views import (
    AdminLoginAPIView,
    RequestOtpAPIView,
    CustomerLoginAPIView,
)

from ..views.order_flow_view import OrderFlowAPIView

router = DefaultRouter()
router.register("stores", StoreViewSet)
router.register("categories", CategoryViewSet)
router.register("subcategories", SubcategoryViewSet)
router.register("products", ProductViewSet)
router.register("product-images", ProductImageViewSet)
router.register("orders", OrderViewSet)
router.register("order-items", OrderDetailViewSet)
router.register("payments", PaymentViewSet)
router.register(" invoices ", InvoiceViewSet)
router.register("addresses", AddressViewSet)
router.register("coupons", CouponViewSet)
router.register("audit-logs", AuditLogViewSet)


urlpatterns = [
    path("admin/login/", AdminLoginAPIView.as_view(), name="admin-login"),
    path("customer/request-otp/", RequestOtpAPIView.as_view(), name="customer-request-otp"),
    path("customer/login/", CustomerLoginAPIView.as_view(), name="customer-login"),

]

urlpatterns += router.urls
