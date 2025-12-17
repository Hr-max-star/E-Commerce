from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import uuid
from ..models import *
from ..serializers import *
from ..permissions import IsAdmin


class StoreViewSet(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin()]


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin()]


class SubcategoryViewSet(ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin()]


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]


class ProductImageViewSet(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            return [AllowAny()]  
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        items = request.data.get("order_items", [])
        store_id = request.data.get("store_id")

        user = request.user if request.user.is_authenticated else None

        order = Order.objects.create(
            user=user,
            store_id=store_id,
            status="CART",
        )

        total = self._build_items(order, items)
        order.total_amount = total
        order.save()

        return Response(OrderSerializer(order).data, status=201)

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        items = request.data.get("order_items", [])
        action = request.data.get("action")

        total = self._build_items(order, items)

        order.total_amount = total
        order.save()

        if action == "place_order":
            order.status = "PLACED"
            order.save()

            invoice = Invoice.objects.create(
                order=order,
                invoice_number=f"INV-{uuid.uuid4().hex[:10].upper()}",
                amount=total, 
            )

            order.invoice = invoice
            order.save()

        return Response(OrderSerializer(order).data, status=200)

    def _build_items(self, order, items):   
        order.items.all().delete()    

        total = 0
        for item in items:
            product = get_object_or_404(Product, id=item["product_id"])
            qty = item["quantity"]
            line_total = product.price * qty
            total += line_total

            OrderDetail.objects.create(
                order=order,
                product=product,
                sku=product.sku,
                quantity=qty,
                unit_price=product.price,
                line_total=line_total,
                metadata={"name": product.name},
            )

        return total


class OrderDetailViewSet(ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]


class CouponViewSet(ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class AuditLogViewSet(ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
