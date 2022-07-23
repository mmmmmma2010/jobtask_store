from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin
from rest_framework.response import Response
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework import status
from store.filters import ItemFilter
from store.models.order_models import OrderItem
from store.pagination import DefaultPagination
from store.permissions import IsAdminOrReadOnly,ReadOnly
from store.serializers.item_serializers import AddCartItemSerializer,CartSerializer, CartItemSerializer, CategorySerializer, ItemSerializer, UpdateCartItemSerializer

from store.models.item_models import Cart, CartItem, Category, Item

# Create your views here.
class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ItemFilter
    pagination_class = DefaultPagination
    permission_classes = [ReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(item_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Item cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(
        products_count=Count('items')).all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Item.objects.filter(category_id=kwargs['pk']):
            return Response({'error': 'Category cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects \
            .filter(cart_id=self.kwargs['cart_pk']) \
            .select_related('item')

