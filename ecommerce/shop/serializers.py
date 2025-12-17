
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["email"], password=data["password"])

        if not user: 
            raise serializers.ValidationError("Invalid email or password")

        if not user.is_admin:
            raise serializers.ValidationError("Only admin users can login here")

        data["user"] = user
        return data


class RequestOtpSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=32)


class CustomerLoginSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=32)
    otp = serializers.CharField(max_length=6)
 
    def validate(self, data):
        user = authenticate(mobile_number=data["mobile_number"], otp=data["otp"])

        if not user:
            raise serializers.ValidationError("Invalid mobile or OTP")

        if not user.is_customer:
            raise serializers.ValidationError("Only customers can login")

        data["user"] = user
        return data
    
 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id", "email", "mobile_number",
            "is_customer", "is_active", "cdate", "mdate"
        ]


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)



class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Invoice
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField(read_only=True)

    order_items = OrderItemInputSerializer(many=True, write_only=True, required=False)

    action = serializers.ChoiceField(
        choices=["update_cart", "place_order"], 
        write_only=True,
        required=False
    )

    class Meta:
        model = Order
        fields = "__all__"

    def get_items(self, obj):
        details = OrderDetail.objects.filter(order=obj)
        return [
            {
                "product_id": str(i.product.id),
                "sku": i.sku,
                "quantity": i.quantity,
                "unit_price": float(i.unit_price),
                "line_total": float(i.line_total)
            }
            for i in details
        ]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = "__all__"
