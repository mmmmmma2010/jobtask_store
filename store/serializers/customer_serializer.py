from rest_framework import serializers
from store.models.users_models import Customer



class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'first_name','last_name', 'birth_date']