from rest_framework import serializers
from store.models.item_models import Cart, CartItem, Item,Category



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'items_count']

    items_count = serializers.IntegerField(read_only=True)


class ItemSerializer (serializers.ModelSerializer):
    class Meta:
        model=Item
        fields=['id', 'title', 'description', 'slug', 'inventory',
                  'unit_price', 'category']


class SimpleItemSerializer (serializers.ModelSerializer):
    class Meta:
        model=Item
        fields=['id', 'title','unit_price']



class CartItemSerializer(serializers.ModelSerializer):
    item = SimpleItemSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.item.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'item', 'quantity', 'total_price']



class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
class AddCartItemSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField()

    def validate_item_id(self, value):
        if not Item.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                'No item with the given ID was found.')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        item_id = self.validated_data['item_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, item_id=item_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'item_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
