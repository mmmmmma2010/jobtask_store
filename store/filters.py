from django_filters.rest_framework import FilterSet
from .models.item_models import Item

class ItemFilter(FilterSet):
  class Meta:
    model = Item
    fields = {
      'category_id': ['exact'],
      'unit_price': ['gt', 'lt']
    }