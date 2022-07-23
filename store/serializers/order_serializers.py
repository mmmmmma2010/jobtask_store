from rest_framework import serializers
from store.models.order_models import Order,OrderItem

from django.db import transaction
from rest_framework import serializers

from store.models.item_models import Cart, CartItem
from store.models.users_models import  Customer
from store.models.order_models import   Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
  

    class Meta:
        model = OrderItem
        fields = ['id', 'item', 'unit_price', 'quantity','shipping_state']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']



class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError(
                'No cart with the given ID was found.')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty.')
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']

            customer = Customer.objects.get(
                user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)

            cart_items = CartItem.objects \
                .select_related('item') \
                .filter(cart_id=cart_id)
            order_items = [
                OrderItem(
                    order=order,
                    item=cart_item.item,
                    unit_price=cart_item.item.unit_price,
                    quantity=cart_item.quantity
                    
                ) for cart_item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(pk=cart_id).delete()

        
            return order