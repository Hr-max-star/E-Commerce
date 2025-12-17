
from uuid import uuid4
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.urls import path
import uuid
from ..models import*
from ..serializers import*



class OrderFlowAPIView(APIView):

    def post(self, request):
        serializer = OrderFlowInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # support guest checkout
        user = request.user if request.user.is_authenticated else None

        if data.get("order_id"):
            order = get_object_or_404(Order, id=data["order_id"])
        else:
            order = Order.objects.create(
                user=user,
                store_id=data["store_id"],
                status="CART"
            )

      
        order.items.all().delete()

    
        from shop.models import Product

        total = 0

       
        for item in data["items"]:
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

        order.total_amount = total
        order.save()

        if data["action"] == "place_order":
            order.status = "PLACED"
            order.save()

            invoice = Invoice.objects.create(
                order=order,
                invoice_number=f"INV-{uuid.uuid4().hex[:10].upper()}",
                amount=total
            )

            order.invoice = invoice
            order.save()

        return Response(OrderSerializer(order).data, status=200)
