from django.contrib import admin,messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.admin import  ModelAdmin
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from .models.item_models import Category, Item
from .models.order_models import Order,OrderItem
from.models.users_models import Customer,Vendor

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user_name','first_name', 'last_name', 'orders']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            }))
        return format_html('<a href="{}">{} Orders</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )
    def has_add_permission(self, request) -> bool:
        return False
    def has_module_permission(self, request) -> bool:      
        if not   isinstance(request.user,AnonymousUser) :
            if request.user.type=='V':
                return False



        return super().has_module_permission(request)

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):

    
    list_display = ['user_name','first_name', 'last_name', 'items']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='items_count')
    def items(self, vendor):
        url = (
            reverse('admin:store_item_changelist')
            + '?'
            + urlencode({
                'customer__id': str(vendor.id)
            }))
        return format_html('<a href="{}">{} items</a>', url, vendor.items_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            items_count=Count('item')
        )


    def has_add_permission(self, request) -> bool:

        return False


@admin.register(Item)
class ItemAdmin(ModelAdmin):
    exclude=['vendor']

    autocomplete_fields = ['category']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price',
                    'inventory_status', 'category_title']
    list_editable = ['unit_price']
    list_filter = ['category', 'last_update']
    list_per_page = 10
    list_select_related = ['category']
    search_fields = ['title']

    def category_title(self, item):
        return item.category.title

    @admin.display(ordering='inventory')
    def inventory_status(self, item):
        if item.inventory < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} items were successfully updated.',
            messages.ERROR
        )
    def get_queryset(self, request) :
        if request.user.is_superuser==True:
            return Item.objects.all()
        else:
            return Item.objects.filter(vendor_id=request.user.id)
    
    
    def save_model(self, request, obj, form, change) -> None:
        vendor_id = Vendor.objects.only(
            'id').get(user_id=request.user.id)
        obj.vendor=vendor_id
        return super().save_model(request, obj, form, change)

    def has_add_permission(self, request) -> bool:
        if request.user.type=='V':
            return True
        return False


@admin.register(Category)
class CategoryAdmin(ModelAdmin):

    list_display = ['title', 'items_count']
    search_fields = ['title']

    @admin.display(ordering='items_count')
    def items_count(self, category):
        url = (
            reverse('admin:item_item_changelist')
            + '?'
            + urlencode({
                'category__id': str(category.id)
            }))
        return format_html('<a href="{}">{} Items</a>', url, category.items_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            items_count=Count('items')
        )




class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['item']
    min_num = 1
    max_num = 10
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'customer']

    
    def has_add_permission(self, request) -> bool:

        return False