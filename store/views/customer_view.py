from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from store.permissions import IsAdmin, IsCustomer
from store.serializers.customer_serializer import CustomerSerializer, Customer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdmin]

    @action(detail=False,
            methods=['GET', 'PUT'],
            permission_classes=[IsCustomer])
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)